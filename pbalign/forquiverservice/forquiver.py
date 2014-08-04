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

"""This script defines ForQuiverService, which post-processes a cmp.h5 file so
that it can be used by quiver directly. ForQuiverService sorts the file, loads
pulse information to it and finally repacks it.."""

# Author: Yuan Li

from __future__ import absolute_import
import logging
from pbalign.forquiverservice.sort import SortService
from pbalign.forquiverservice.loadpulses import LoadPulsesService
from pbalign.forquiverservice.loadchemistry import LoadChemistryService
from pbalign.forquiverservice.repack import RepackService


class ForQuiverService(object):
    """
    Uses SortService, LoadPulsesService, LoadChemistryService,
    RepackService to post process a cmp.h5 file so that the file can
    be used by quiver directly.
    """
    @property
    def name(self):
        """Name of ForQuiverService."""
        return "ForQuiverService"

    def __init__(self, fileNames, options):
        """Initialize a ForQuiverService object.

        Input:
            fileNames : pbalign file names
            options   : pbalign options

        """
        self.fileNames = fileNames
        self.options = options
        self._loadpulsesService = LoadPulsesService(
            self.fileNames.pulseFileName,
            self.fileNames.outputFileName,
            self.options)
        self._loadchemistryService = LoadChemistryService(
            self.fileNames.pulseFileName,
            self.fileNames.outputFileName,
            self.options)
        self._sortService = SortService(
            self.fileNames.outputFileName,
            self.options)
        self._repackService = RepackService(
            self.fileNames.outputFileName,
            self.fileNames.outputFileName + ".TMP")

    def run(self):
        """ Run the ForQuiver service."""
        logging.info(self.name + ": Sort.")

        self._sortService.checkAvailability()
        self._sortService.run()

        logging.info(self.name + ": LoadPulses.")
        self._loadpulsesService.checkAvailability()
        self._loadpulsesService.run()

        logging.info(self.name + ": LoadChemistry.")
        self._loadchemistryService.checkAvailability()
        self._loadchemistryService.run()

        logging.info(self.name + ": Repack.")
        self._repackService.checkAvailability()
        self._repackService.run()
