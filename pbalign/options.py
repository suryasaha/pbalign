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

# Author:Yuan Li
"""This scripts defines functions for parsing PBAlignRunner options."""

from __future__ import absolute_import
import argparse
from copy import copy

# The first candidate 'blasr' is the default.
ALGORITHM_CANDIDATES = ('blasr', 'bowtie', 'gmap')

# The first candidate 'randombest' is the default.
HITPOLICY_CANDIDATES = ('randombest', 'allbest', 'random', 'all', 'leftmost')

# The first candidate 'aligner' is the default.
SCOREFUNCTION_CANDIDATES = ('alignerscore', 'editdist',
                            #'blasrscore', 'userscore')
                            'blasrscore')
DEFAULT_METRICS = ("DeletionQV", "DeletionTag", "InsertionQV",
                   "MergeQV", "SubstitutionQV")

# Default values of arguments
DEFAULT_OPTIONS = {"regionTable": None,
                   "configFile": None,
                   # Choose an aligner
                   "algorithm": ALGORITHM_CANDIDATES[0],
                   # Aligner options
                   "maxHits": 10,
                   "minAnchorSize": 12,
                   "noSplitSubreads": False,
                   "concordant": False,
                   "algorithmOptions": None,
                   "useccs": None,
                   # Filter options
                   "maxDivergence": 30,
                   "minAccuracy": 70,
                   "minLength": 50,
                   "scoreFunction": SCOREFUNCTION_CANDIDATES[0],
                   "scoreCutoff": None,
                   "hitPolicy": HITPOLICY_CANDIDATES[0],
                   "filterAdapterOnly": False,
                   # Cmp.h5 writer options
                   "readType": "standard",
                   "forQuiver": False,
                   "loadQVs": False,
                   "byread": False,
                   "metrics": str(",".join(DEFAULT_METRICS)),
                   # Miscellaneous options
                   "nproc": 8,
                   "seed": 1,
                   "tmpDir": "/scratch"}


def constructOptionParser(parser=None):
    """Constrct and return an argument parser.

    If a parser is specified, use it. Otherwise, create a parser instead.
    Add PBAlignRunner arguments to construct the parser, and finally
    return it.

    """
    desc = "Mapping PacBio sequences to references using an algorithm \n"
    desc += "selected from a selection of supported command-line alignment\n"
    desc += "algorithms. Input can be a fasta, pls.h5, bas.h5 or ccs.h5\n"
    desc += "file or a fofn (file of file names). Output is in either\n"
    desc += "cmp.h5 or sam format.\n"

    if (parser is None):
        parser = argparse.ArgumentParser()

    parser.description = desc
    parser.argument_default = argparse.SUPPRESS
    parser.formatter_class = argparse.RawTextHelpFormatter

    # Optional input.
    parser.add_argument("--regionTable",
                        dest="regionTable",
                        type=str,
                        default=None,
                        action="store",
                        help="Specify a region table for filtering reads.")

    parser.add_argument("--configFile",
                        dest="configFile",
                        default=None,
                        type=str,
                        action="store",
                        help="Specify a set of user-defined argument values.")

    helpstr = "When input reads are in fasta format and output is a cmp.h5\n" + \
              "this option can specify pls.h5 or bas.h5 or \n" + \
              "FOFN files from which pulse metrics can be loaded for Quiver."
    parser.add_argument("--pulseFile",
                        dest="pulseFile",
                        default=None,
                        type=str,
                        action="store",
                        help=helpstr)

    # Chose an aligner.
    helpstr = "Select an aligorithm from {0}.\n".format(ALGORITHM_CANDIDATES)
    helpstr += "Default algorithm is {0}.".format(DEFAULT_OPTIONS["algorithm"])
    parser.add_argument("--algorithm",
                        dest="algorithm",
                        type=str,
                        action="store",
                        choices=ALGORITHM_CANDIDATES,
                        default=ALGORITHM_CANDIDATES[0],
                        help=helpstr)

    # Aligner options.
    helpstr = "The maximum number of matches of each read to the \n" + \
              "reference sequence that will be evaluated. Default\n" + \
              "value is {0}.".format(DEFAULT_OPTIONS["maxHits"])
    parser.add_argument("--maxHits",
                        dest="maxHits",
                        type=int,
                        default=None,  # Set as None instead of a real number.
                        action="store",
                        help=helpstr)

    helpstr = "The minimum anchor size defines the length of the read\n" + \
              "that must match against the reference sequence. Default\n" + \
              "value is {0}.".format(DEFAULT_OPTIONS["minAnchorSize"])
    parser.add_argument("--minAnchorSize",
                        dest="minAnchorSize",
                        type=int,
                        default=None,  # Set as None to avoid conflicts with
                                       # --algorithmOptions
                        action="store",
                        help=helpstr)

    # Aligner options: Use ccs or not?
    helpstr = "Map the ccsSequence to the genome first, then align\n" + \
              "subreads to the interval that the CCS reads mapped to.\n" + \
              "  useccs: only maps subreads that span the length of\n" + \
              "          the template.\n" + \
              "  useccsall: maps all subreads.\n" + \
              "  useccsdenovo: maps ccs only."
    parser.add_argument("--useccs",
                        type=str,
                        choices=["useccs", "useccsall", "useccsdenovo"],
                        action="store",
                        default=None,
                        help=helpstr)

    helpstr = "Do not split reads into subreads even if subread \n" + \
              "regions are available. Default value is {0}."\
              .format(DEFAULT_OPTIONS["noSplitSubreads"])
    parser.add_argument("--noSplitSubreads",
                        dest="noSplitSubreads",
                        default=DEFAULT_OPTIONS["noSplitSubreads"],
                        action="store_true",
                        help=helpstr)

    helpstr = "Map subreads of a ZMW to the same genomic location.\n"
    parser.add_argument("--concordant",
                        dest="concordant",
                        default=DEFAULT_OPTIONS["concordant"],
                        action="store_true",
                        help=helpstr)

    helpstr = "Number of threads. Default value is {v}."\
              .format(v=DEFAULT_OPTIONS["nproc"])
    parser.add_argument("--nproc",
                        type=int,
                        dest="nproc",
                        default=DEFAULT_OPTIONS["nproc"],
                        #default=15,
                        action="store",
                        help=helpstr)

    parser.add_argument("--algorithmOptions",
                        type=str,
                        dest="algorithmOptions",
                        default=None,
                        action="append",
                        help="Pass alignment options through.")

    # Filtering criteria and hit policy.
    helpstr = "The maximum allowed percentage divergence of a read \n" + \
              "from the reference sequence. Default value is {0}." \
              .format(DEFAULT_OPTIONS["maxDivergence"])
    parser.add_argument("--maxDivergence",
                        dest="maxDivergence",
                        type=float,
                        default=DEFAULT_OPTIONS["maxDivergence"],
                        #default=30,
                        action="store",
                        help=helpstr)

    helpstr = "The minimum percentage accuracy of alignments that\n" + \
              "will be evaluated. Default value is {v}." \
              .format(v=DEFAULT_OPTIONS["minAccuracy"])
    parser.add_argument("--minAccuracy",
                        dest="minAccuracy",
                        type=float,
                        default=DEFAULT_OPTIONS["minAccuracy"],
                        #default=70,
                        action="store",
                        help=helpstr)

    helpstr = "The minimum aligned read length of alignments that\n" + \
              "will be evaluated. Default value is {v}." \
              .format(v=DEFAULT_OPTIONS["minLength"])
    parser.add_argument("--minLength",
                        dest="minLength",
                        type=int,
                        default=DEFAULT_OPTIONS["minLength"],
                        action="store",
                        help=helpstr)

    helpstr = "Specify a score function for evaluating alignments.\n"
    helpstr += "  alignerscore : aligner's score in the SAM tag 'as'.\n"
    helpstr += "  editdist     : edit distance between read and reference.\n"
    helpstr += "  blasrscore   : blasr's default score function.\n"
    helpstr += "Default value is {0}.".format(DEFAULT_OPTIONS["scoreFunction"])
    parser.add_argument("--scoreFunction",
                        dest="scoreFunction",
                        type=str,
                        choices=SCOREFUNCTION_CANDIDATES,
                        default=DEFAULT_OPTIONS["scoreFunction"],
                        action="store",
                        help=helpstr)
    #"  userscore    : user-defined score matrix (by -scoreMatrix).\n")
    #parser.add_argument("--scoreMatrix",
    #                    dest="scoreMatrix",
    #                    type=str,
    #                    default=None,
    #                    help=
    #                    "Specify a user-defined score matrix for "
    #                    "scoring reads.The matrix\n"+\
    #                    "is in the format\n"
    #                    "    ACGTN\n"
    #                    "  A abcde\n"
    #                    "  C fghij\n"
    #                    "  G klmno\n"
    #                    "  T pqrst\n"
    #                    "  N uvwxy\n"
    #                    ". The values a...y should be input as a "
    #                    "quoted space separated\n"
    #                    "string: "a b c ... y". Lower scores are better,"
    #                    "so matches\n"
    #                    "should be less than mismatches e.g. a,g,m,s "
    #                    "= -5 (match),\n"
    #                    "mismatch = 6.\n")

    parser.add_argument("--scoreCutoff",
                        dest="scoreCutoff",
                        type=int,
                        default=None,
                        action="store",
                        help="The worst score to output an alignment.\n")

    helpstr = "Specify a policy for how to treat multiple hit\n" + \
           "  random    : selects a random hit.\n" + \
           "  all       : selects all hits.\n" + \
           "  allbest   : selects all the best score hits.\n" + \
           "  randombest: selects a random hit from all best score hits.\n" + \
           "  leftmost  : selects a hit which has the best score and the\n" + \
           "              smallest mapping coordinate in any reference.\n" + \
           "Default value is {v}.".format(v=DEFAULT_OPTIONS["hitPolicy"])
    parser.add_argument("--hitPolicy",
                        dest="hitPolicy",
                        type=str,
                        choices=HITPOLICY_CANDIDATES,
                        default=DEFAULT_OPTIONS["hitPolicy"],
                        action="store",
                        help=helpstr)

    helpstr = "If specified, do not report adapter-only hits using\n" + \
              "annotations with the reference entry."
    parser.add_argument("--filterAdapterOnly",
                        dest="filterAdapterOnly",
                        default=DEFAULT_OPTIONS["filterAdapterOnly"],
                        action="store_true",
                        help=helpstr)

    # Output.
    helpstr = "Specify the ReadType attribute in the cmp.h5 output.\n" + \
              "Default value is {v}.".format(v=DEFAULT_OPTIONS["readType"])
    parser.add_argument("--readType",
                        dest="readType",
                        type=str,
                        action="store",
                        default=DEFAULT_OPTIONS["readType"],
                        help=argparse.SUPPRESS)
                        #help=helpstr)

    helpstr = "The output cmp.h5 file which will be sorted, loaded\n" + \
              "with pulse QV information, and repacked, so that it \n" + \
              "can be consumed by quiver directly. This requires\n" + \
              "the input file to be in PacBio bas/pls.h5 format,\n" + \
              "and --useccs must be None. Default value is False."
    parser.add_argument("--forQuiver",
                        dest="forQuiver",
                        action="store_true",
                        default=DEFAULT_OPTIONS["forQuiver"],
                        help=helpstr)

    helpstr = "Similar to --forQuiver, the only difference is that \n" + \
              "--useccs can be specified. Default value is False."
    parser.add_argument("--loadQVs",
                        dest="loadQVs",
                        action="store_true",
                        default=DEFAULT_OPTIONS["loadQVs"],
                        help=helpstr)

    helpstr = "Load pulse information using -byread option instead\n" + \
              "of -bymetric. Only works when --forQuiver or \n" + \
              "--loadQVs are set. Default value is False."
    parser.add_argument("--byread",
                        dest="byread",
                        action="store_true",
                        default=DEFAULT_OPTIONS["byread"],
                        help=helpstr)

    helpstr = "Load the specified (comma-delimited list of) metrics\n" + \
              "instead of the default metrics required by quiver.\n" + \
              "This option only works when --forQuiver  or \n" + \
              "--loadQVs are set. Default: {m}".\
              format(m=DEFAULT_OPTIONS["metrics"])
    parser.add_argument("--metrics",
                        dest="metrics",
                        type=str,
                        action="store",
                        default=DEFAULT_OPTIONS["metrics"],
                        help=helpstr)

    # Miscellaneous.
    helpstr = "Initialize the random number generator with a none-zero \n" + \
              "integer. Zero means that current system time is used.\n" + \
              "Default value is {v}.".format(v=DEFAULT_OPTIONS["seed"])
    parser.add_argument("--seed",
                        dest="seed",
                        type=int,
                        default=DEFAULT_OPTIONS["seed"],
                        action="store",
                        help=helpstr)

    helpstr = "Specify a directory for saving temporary files.\n" + \
              "Default is {v}.".format(v=DEFAULT_OPTIONS["tmpDir"])
    parser.add_argument("--tmpDir",
                        dest="tmpDir",
                        type=str,
                        action="store",
                        default=DEFAULT_OPTIONS["tmpDir"],
                        help=helpstr)

    # Keep all temporary & intermediate files.
    parser.add_argument("--keepTmpFiles",
                        dest="keepTmpFiles",
                        action="store_true",
                        default=False,
                        help=argparse.SUPPRESS)

    # Required options: inputs and outputs.
    helpstr = "The input file can be a fasta, plx.h5, bax.h5, ccs.h5\n" + \
              "file or a fofn."
    parser.add_argument("inputFileName",
                        type=str,
                        action="store",
                        help=helpstr)

    helpstr = "Either a reference fasta file or a reference repository."
    parser.add_argument("referencePath",
                        type=str,
                        action="store",
                        help=helpstr)

    parser.add_argument("outputFileName",
                        type=str,
                        action="store",
                        help="The output cmp.h5 or sam file.")

    return parser


def importConfigOptions(options):
    """
    Import options from options.configFile if the file exists, and
    overwrite a copy of the incoming options with options imported
    from the config file. Finally, return the new options and an
    info message.
    """
    newOptions = copy(options)
    # No config file exists.
    if 'configFile' not in options or options.configFile is None:
        return newOptions, ""

    # There exists a config file
    optionsDictView = vars(newOptions)
    configFile = options.configFile
    infoMsg = "ConfigParser: Import options from a config file {0}: "\
              .format(configFile)
    # The following arguments are defined in PBToolRunner, and may
    # not exist in the input options (if the input options is parsed
    # by a parser created in constructOptionParser).
    specialArguments = ("--version", "--configFile", "--verbose",
                        "--debug", "--profile", "-v", "-vv", "-vvv",
                        "--keepTmpFiles")
    try:
        with open(configFile, 'r') as cf:
            for line in cf:
                line = line.strip()
                errMsg = ""
                # First parse special arguments and comments
                if (line.startswith("#") or line == "" or
                        line in specialArguments):
                    pass
                else:  # Parse binary arguments
                    try:
                        k, v = line.split("=")
                        k = k.lstrip().lstrip('-').strip()
                        v = v.strip().strip('\"').strip('\'')
                    except ValueError as e:
                        errMsg = "ConfigParser: could not find '=' when " + \
                                 "parsing {0}.".format(line)
                        raise ValueError(errMsg)
                    # Always use options' values from the configFile.
                    if k not in optionsDictView:
                        errMsg = "{k} is an invalid option.".format(k=k)
                        raise ValueError(errMsg)
                    else:
                        infoMsg += "{k}={v}, ".format(k=k, v=v)
                        optionsDictView[k] = v
    except IOError as e:
        errMsg = "ConfigParser: Could not open a config file {0}.\n".\
                 format(configFile)
        raise IOError(errMsg + str(e))
    return newOptions, infoMsg


def importDefaultOptions(parsedOptions, additionalDefaults=DEFAULT_OPTIONS):
    """Import default options and return (update_options, an_info_message).

    After parsing the arguments and resolving algorithmOptions, we need
    to patch the default pbalign options, if they have not been overwritten
    on the command-line nor in the config file nor within algorithmOptions.

    """
    newOptions = copy(parsedOptions)
    infoMsg = "Importing default options: "
    optionsDictView = vars(newOptions)
    for k, v in additionalDefaults.iteritems():
        if (k not in optionsDictView) or (optionsDictView[k] is None):
            infoMsg += "{k}={v}, ".format(k=optionsDictView[k], v=v)
            optionsDictView[k] = v
    return newOptions, infoMsg.rstrip(', ')


def parseOptions(argumentList, parser=None):
    """Parse a list of arguments, return options and an info message.

    If a parser is not specified, create a new parser, otherwise, use
    the specifed parser. If there exists a config file, import options
    from the config file and finally overwrite these options with
    options from the argument list.

    """
    # Obtain a constructed argument parser.
    parser = constructOptionParser(parser)

    # Parse argumentList for the first time in order to
    # get a config file.
    options = parser.parse_args(args=argumentList)

    # Import options from the specified config file, if it exists.
    configOptions, infoMsg = importConfigOptions(options)

    # Parse argumentList for the second time in order to
    # overwrite config options with options in argumentList.
    newOptions = copy(configOptions)
    newOptions.algorithmOptions = None
    newOptions = parser.parse_args(namespace=newOptions, args=argumentList)

    # Overwrite config algorithmOptions if it is specified in argumentList
    if newOptions.algorithmOptions is None:
        if configOptions.algorithmOptions is not None:
            newOptions.algorithmOptions = configOptions.algorithmOptions
    else:
        newOptions.algorithmOptions = \
            " ".join(newOptions.algorithmOptions)

    # Return the updated options and an info message.
    return parser, newOptions, infoMsg

#if __name__ == "__main__":
#     import sys
#     parser = argparse.ArgumentParser()
#     parser, options, info = parseOptions(argumentList = sys.argv[1:],
#                                          parser=parser)
