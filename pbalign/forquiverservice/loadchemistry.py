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

from __future__ import absolute_import
import logging
from pbalign.service import Service

class LoadChemistryService(Service):
    @property
    def name(self):
        return "LoadChemistryService"

    @property
    def progName(self):
        return "loadChemistry.py"

    # Quiver only uses the following five metrics.

    def __init__(self, basFofnFile, cmpFile, options):
        """
        Input:
            basFofnFile: the input BASE.H5 (or fofn) files
            cmpFile    : an input CMP.H5 file
            options    : pbalign options
        """
        self.basFofnFile = basFofnFile
        self.cmpFile = cmpFile
        self.options = options

    @property
    def cmd(self):
        """String of a command-line to execute."""
        return self._toCmd(self.basFofnFile, self.cmpFile)

    def _toCmd(self, basFofnFile, cmpFile):
        """
        Generate a loadChemistry command line.
        """
        cmdStr = self.progName + \
            " {basFofnFile} {cmpFile} ".format(
                basFofnFile=basFofnFile, cmpFile=cmpFile)

        return cmdStr

    def run(self):
        """Run the loadChemistry service."""
        logging.info(self.name + ": Load pulses using {progName}.".
                    format(progName=self.progName))
        return self._execute()
