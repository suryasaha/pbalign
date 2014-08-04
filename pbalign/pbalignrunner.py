#!/usr/bin/env python
###############################################################################
# Copyright (c) 2011-2013, Pacific Biosciences of California, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of Pacific Biosciences nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY
# THIS LICENSE.  THIS SOFTWARE IS PROVIDED BY PACIFIC BIOSCIENCES AND ITS
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT
# NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL PACIFIC BIOSCIENCES OR
# ITS CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
# OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
###############################################################################

"""This script defines class PBAlignRunner.

PBAlignRunner uses AlignService to align PacBio reads in FASTA/BASE/PULSE/FOFN
formats to reference sequences, then uses FilterServices to filter out
alignments that do not satisfy filtering criteria, and finally generates a SAM
or CMP.H5 file.

"""

# Author: Yuan Li

import logging
import time
import sys
import shutil

from pbalign.__init__ import get_version
from pbalign.options import parseOptions, ALGORITHM_CANDIDATES
from pbalign.alignservice.blasr import BlasrService
from pbalign.alignservice.bowtie import BowtieService
from pbalign.alignservice.gmap import GMAPService
from pbalign.utils.fileutil import getFileFormat, FILE_FORMATS, real_ppath
from pbalign.utils.tempfileutil import TempFileManager
from pbalign.pbalignfiles import PBAlignFiles
from pbalign.filterservice import FilterService
from pbalign.forquiverservice.forquiver import ForQuiverService
from pbcore.util.Process import backticks
from pbcore.util.ToolRunner import PBToolRunner


class PBAlignRunner(PBToolRunner):
    """Tool runner."""

    def __init__(self, argumentList):
        """Initialize a PBAlignRunner object.
           argumentList is a list of arguments, such as:
           ['--debug', '--maxHits', '10', 'in.fasta', 'ref.fasta', 'out.sam']
        """
        desc = "Utilities for aligning PacBio reads to reference sequences."
        super(PBAlignRunner, self).__init__(desc)
        self._argumentList = argumentList
        self._alnService = None
        self._filterService = None
        self.fileNames = PBAlignFiles()
        self._tempFileManager = TempFileManager()

        self.parser, self.args, _infoMsg = parseOptions(
            argumentList=self._argumentList, parser=self.parser)
        # args.verbosity is computed by counting # of 'v's in '-vv...'.
        # However in parseOptions, arguments are parsed twice to import config
        # options and then overwrite them with argumentList (e.g. command-line)
        # options.
        self.args.verbosity = 0 if (self.args.verbosity is None) else \
            int(self.args.verbosity) / 2

    def getVersion(self):
        """Return version."""
        return get_version()

    def _createAlignService(self, name, args, fileNames, tempFileManager):
        """
        Create and return an AlignService by algorithm name.
        Input:
            name           : an algorithm name such as blasr
            fileNames      : an PBAlignFiles object
            args           : pbalign options
            tempFileManager: a temporary file manager
        Output:
            an object of AlignService subclass (such as BlasrService).
        """
        if name not in ALGORITHM_CANDIDATES:
            errMsg = "ERROR: unrecognized algorithm {algo}".format(algo=name)
            logging.error(errMsg)
            raise ValueError(errMsg)

        service = None
        if name == "blasr":
            service = BlasrService(args, fileNames, tempFileManager)
        elif name == "bowtie":
            service = BowtieService(args, fileNames, tempFileManager)
        elif name == "gmap":
            service = GMAPService(args, fileNames, tempFileManager)
        else:
            errMsg = "Service for {algo} is not implemented.".\
                     format(algo=name)
            logging.error(errMsg)
            raise ValueError(errMsg)

        service.checkAvailability()
        return service

    def _makeSane(self, args, fileNames):
        """
        Check whether the input arguments make sense or not.
        """
        errMsg = ""
        if args.useccs == "useccsdenovo":
            args.readType = "CCS"

        if fileNames.inputFileFormat == FILE_FORMATS.CCS:
            args.readType = "CCS"

        if args.forQuiver:
            if fileNames.pulseFileName is None:
                errMsg = "Neither the input file is in bas/pls/ccs.h5 " + \
                         "format, nor --pulseFile is specified, "
            if getFileFormat(fileNames.outputFileName) != FILE_FORMATS.CMP:
                errMsg = "The output file is not in cmp.h5 format, "
            if errMsg != "":
                errMsg += ", while --forQuiver is true."
                logging.error(errMsg)
                raise ValueError(errMsg)

    def _parseArgs(self):
        """Overwrite ToolRunner.parseArgs(self).
        Parse PBAlignRunner arguments considering both args in argumentList and
        args in a config file (specified by --configFile).
        """
        pass

    def _output(self, inSam, refFile, outFile, readType=None, smrtTitle=False):
        """Generate a sam or a cmp.h5 file.
        Input:
            inSam   : an input SAM file. (e.g. fileName.filteredSam)
            refFile : the reference file. (e.g. fileName.targetFileName)
            outFile : the output SAM or CMP.H5 file.
                      (i.e. fileName.outputFileName)
            readType: standard or cDNA or CCS (can be None if not specified)
        Output:
            output, errCode, errMsg
        """
        output, errCode, errMsg = "", 0, ""

        if getFileFormat(outFile) == FILE_FORMATS.SAM:
            #`mv inSam outFile`
            logging.info("OutputService: Genearte the output SAM file.")
            logging.debug("OutputService: Move {src} as {dst}".format(
                src=inSam, dst=outFile))
            try:
                shutil.move(real_ppath(inSam), real_ppath(outFile))
            except shutil.Error as e:
                output, errCode, errMsg = "", 1, str(e)
        elif getFileFormat(outFile) == FILE_FORMATS.CMP:
            #`samtoh5 inSam outFile -readType readType
            logging.info("OutputService: Genearte the output CMP.H5 " +
                         "file using samtoh5.")
            prog = "samtoh5"
            cmd = "samtoh5 {samFile} {refFile} {outFile}".format(
                samFile=inSam, refFile=refFile, outFile=outFile)
            if readType is not None:
                cmd += " -readType {0} ".format(readType)
            if smrtTitle:
                cmd += " -smrtTitle "
            # Execute the command line
            logging.debug("OutputService: Call \"{0}\"".format(cmd))
            output, errCode, errMsg = backticks(cmd)

        if errCode != 0:
            errMsg = prog + " returned a non-zero exit status." + errMsg
            logging.error(errMsg)
            raise RuntimeError(errMsg)
        return output, errCode, errMsg

    def _cleanUp(self, realDelete=False):
        """ Clean up temporary files and intermediate results. """
        logging.debug("Clean up temporary files and directories.")
        self._tempFileManager.CleanUp(realDelete)

#    def _setupLogging(self):
#        LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
#        if self.args.verbosity >= 2:
#            print "logLevel = debug"
#            logLevel = logging.DEBUG
#        elif self.args.verbosity == 1:
#            print "logLevel = info"
#            logLevel = logging.INFO
#        else:
#            print "logLevel = warn"
#            logLevel = logging.WARN
#        logging.basicConfig(level=logLevel, format=LOG_FORMAT)

    def run(self):
        """
        The main function, it is called by PBToolRunner.start().
        """
        startTime = time.time()
        logging.info("pbalign version: {version}".format(version=get_version()))
        logging.debug("Original arguments: " + str(self._argumentList))

        # Create an AlignService by algorithm name.
        self._alnService = self._createAlignService(self.args.algorithm,
                                                    self.args,
                                                    self.fileNames,
                                                    self._tempFileManager)

        # Make sane.
        self._makeSane(self.args, self.fileNames)

        # Run align service.
        try:
            self._alnService.run()
        except RuntimeError:
            return 1

        # Create a temporary filtered SAM file as output for FilterService.
        self.fileNames.filteredSam = self._tempFileManager.\
            RegisterNewTmpFile(suffix=".sam")

        # Call filter service.
        self._filterService = FilterService(self.fileNames.alignerSamOut,
                                            self.fileNames.targetFileName,
                                            self.fileNames.filteredSam,
                                            self._alnService.name,
                                            self._alnService.scoreSign,
                                            self.args,
                                            self.fileNames.adapterGffFileName)
        try:
            self._filterService.run()
        except RuntimeError:
            return 1

        # Output all hits either in SAM or CMP.H5.
        try:
            useSmrtTitle = False
            if (self.args.algorithm != "blasr" or
                self.fileNames.inputFileFormat == FILE_FORMATS.FASTA):
                useSmrtTitle = True

            self._output(
                self.fileNames.filteredSam,
                self.fileNames.targetFileName,
                self.fileNames.outputFileName,
                self.args.readType,
                useSmrtTitle)
        except RuntimeError:
            return 1

        # Call post service for quiver.
        if self.args.forQuiver:
            postService = ForQuiverService(self.fileNames,
                                           self.args)
            try:
                postService.run()
            except RuntimeError:
                return 1

        # Delete temporay files anyway to make
        self._cleanUp(False if (hasattr(self.args, "keepTmpFiles") and
                               self.args.keepTmpFiles is True) else True)

        endTime = time.time()
        logging.info("Total time: {:.2f} s.".format(float(endTime - startTime)))
        return 0


def main():
    pbobj = PBAlignRunner(sys.argv[1:])
    return pbobj.start()


if __name__ == "__main__":
    # For testing PBAlignRunner.
    # PBAlignRunner inherits PBToolRunner. So PBAlignRunner.start() parses args,
    # sets up logging and finally returns run().
    sys.exit(main())
