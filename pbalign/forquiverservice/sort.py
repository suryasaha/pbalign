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

"""This script defines SortService, which calls cmph5tools.py sort to sort a
cmp.h5 file."""

# Author: Yuan Li

from __future__ import absolute_import
import logging
from pbalign.service import Service


class SortService(Service):
    """Call cmph5tools.py sort to sort a PacBio cmp.h5 file."""
    @property
    def name(self):
        """Name of SortService."""
        return "SortService"

    @property
    def progName(self):
        """Program to call."""
        return "cmph5tools.py"

    def __init__(self, cmpFile, options):
        """Initialize a SortService object.
        Input:
            cmpFile : an input CMP.H5 file
            options : pbalign options
        """
        self.cmpFile = cmpFile
        self.options = options

    @property
    def cmd(self):
        """String of a command-line to execute."""
        return self._toCmd(self.cmpFile, self.options)

    def _toCmd(self, cmpFile, options):
        """Generate a cmph5tools.py sort command line.

        Input:
            cmpFile : an input CMP.H5 file
            options : pbalign options
        Output:
            a command-line string

        """
        cmdStr = self.progName
        if options.verbosity > 1:
            cmdStr += " -vv "

        cmdStr += " sort --deep --inPlace {cmpFile} ".format(cmpFile=cmpFile)
        return cmdStr

    def run(self):
        """Run the sort service."""
        logging.info(self.name + ": Sort a cmp.h5 file using {progName}.".
            format(progName=self.progName))
        return self._execute()
