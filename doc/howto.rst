How to install and run pbalign
==============================

pbalign is a tool for aligning PacBio reads to reference sequences. 
It is part of the PacBio Bioinformatics tools, and will
be bundled in the 2.1 release of SMRTanalysis. You may also follow the 
instructions below to install pbalign.

*Note: the pseudo namespace pbtools has been removed in version 0.2.0.*

*Note: program name has been changed from `pbalign.py` in version 0.1.0
to `pbalign` in version 0.2.0.*

*Note: please install this software on an isolated machine that does
not have SMRTanalysis installed.*

Background
----------
**pbalign** aligns PacBio reads to reference sequences, filters aligned
reads according to user-specific filtering criteria, and converts the
output to either the SAM format or PacBio Compare HDF5 (e.g., .cmp.h5) 
format. The output Compare HDF5 file will be compatible with Quiver if
``--forQuiver`` option is specified.

Required software
-----------------
pbalign is available through the ``pbalign`` script from the 
``pbalign`` package. To use pbalign, the following PacBio software is 
required, 

- ``pbalign``, containing ``pbalign``
- ``pbcore``, a package providing access to PacBio data files
- ``blasr``, a package of PacBio aligner blasr, containing c++ executables
  for processing PacBio data, such as ``blasr``, ``pls2fasta``, 
  ``samFilter``, ``samtoh5`` and ``loadPulses``

The following software is optionally required if ``--forQuiver`` option 
will be used to convert the output Compare HDF5 file to be compatible 
with Quiver.
- ``pbh5tools.cmph5tools``, a PacBio Bioinformatics tools that manipulates 
Compare HDF5 files. 
- ``h5repack``, a HDF5 tool to compress and repack HDF5 files.

The default aligner that pbalign uses is ``blasr``. If you want to use
bowtie2 as aligner, then the bowtie2 package also needs to be installed.

Required libraries and tools
----------------------------
- Python 2.7.3
- virtualenv    (builds isolated Python environments)
- numpy  1.6.1  (required by pbcore)
- h5py   2.0.1  (required by pbcore)

If you are within PacBio, these requirements are already installed
within the cluster environment.

Otherwise, you will need to install them yourself.

Data file requirements
----------------------
pbalign distinguishes input and output file formats by file extensions. 

The input PacBio reads can be in FASTA, Base HDF5, Pulse HDF5, Circular 
Consensus Sequence (CCS) HDF5 or file or file names (FOFN). The supported
input file extensions are as follows.

- FASTA              : .fa or .fasta
- PacBio BASE HDF5   : .bas.h5 or .bax.h5
- PacBio PULSE HDF5  : .pls.h5 or .plx.h5
- PacBio CCS HDF5    : .ccs.h5
- File of file names : .fofn 

The input reference sequences can be in a FASTA file or a reference deposit
directory created by referenceUploader (a PacBio tool for uploading
references to the server and data preprocessing).

The output file can either be a SAM file or a Compare HDF5 file. The output
Compare HDF5 file cannot be consumed by Quiver directly unleis ``--forQuiver``
option is specified. The supported output file extensions are as follows.

- SAM                : .sam
- PacBio Compare HDF5: .cmp.h5


Manual installation instructions
--------------------------------
Step 1: Set up your Python virtual environment
```````````````````````````````````````````````````
To install ``Python 2.7``, please visit ::

    http://www.python.org/

, or if you have root permission on Ubuntu, execute ::

    sudo apt-get install python

To install ``pip``, please visit ::

    https://pypi.python.org/pypi/pip

, or if you have root permission using Ubuntu, execute ::

    sudo apt-get install python-pip

To install ``virtualenv``, please visit ::

    https://pypi.python.org/pypi/virtualenv

, or execute ::

    pip install virtualenv 

To set up a new virtualenv, do ::

    $ cd; virtualenv -p python2.7 --no-site-packages my_env 

, and activate the virtualenv using ::

    $ source ~/my_env/bin/activate


To install ``git``, please visit ::

    http://git-scm.com/.

Step 2: Install required software and library
`````````````````````````````````````````````
To install blasr, please execute ::

    $ git clone https://github.com/PacificBiosciences/blasr

, and follow instructions at ::

    https://github.com/PacificBiosciences/blasr/blob/master/README.md

Before installing pbcore, you may need to install numpy and h5py from ::

    http://www.numpy.org/
    https://code.google.com/p/h5py/

, or if you have root permission on Ubuntu, do ::

    $ pip install numpy
    $ sudo apt-get install libhdf5-serial-dev
    $ pip install h5py

To install pbcore, execute ::

    $ pip install git+https://github.com/PacificBiosciences/pbcore


Step 3: Install optionally required software and library
````````````````````````````````````````````````````````
To install pbh5tools, execute ::

    $ pip install git+https://github.com/PacificBiosciences/pbh5tools

To install ``HDF5 tools``, visit ::

    http://www.hdfgroup.org/products/hdf5_tools/

, or if you have root permission on Ubuntu, do ::

    $ sudo apt-get install hdf5-tools


Step 4: Install pbalign
```````````````````````
To *uninstall* pbalign, execute ::

    $ pip uninstall pbalign


To install pbalign, execute ::

    $ pip install git+https://github.com/PacificBiosciences/pbalign

, or to download the whole pbalign package with examples ::

    $ git clone https://github.com/PacificBiosciences/pbalign.git
    $ cd pbalign
    $ pip install . 


Examples
--------

(1) Basic usage of pbalign.

- Example (1.1) ::

    $ pbalign tests/data/example_read.fasta \
              tests/data/example_ref.fasta  \
              example.sam

- Example (1.2) ::

    $ pbalign tests/data/example_read.fasta \
              tests/data/example_ref.fasta  \
              example.cmp.h5

- Example (1.3) - with optional arguments ::

    $ pbalign --maxHits 10 --hitPolicy all  \
                 tests/data/example_read.fasta \
                 tests/data/example_ref.fasta  \
                 example.sam


(2) Advanced usage of pbalign.

- Example (2.1) - Import pre-defined options from a config File ::

    $ pbalign --configFile=tests/data/1.config \
                 tests/data/example_read.fasta    \
                 tests/data/example_ref.fasta     \
                 example.sam

- Example (2.2) - Pass options through to aligner :: 

    $ pbalign --algorithmOptions='-nCandidates 10 -sdpTupleSize 12' \
                 tests/data/example_read.fasta                         \
                 tests/data/example_ref.fasta                          \
                 example.sam


- Example (2.3) - Create a cmp.h5 file with --forQuiver option :: 

    # The output cmp.h5 file will loaded with quality values (pulses) 
    # from the input bas/bax.h5 file, sorted and repacked, and therefore
    # can be consumed by Quiver directly, (Note that in order to use 
    # --forQuiver option, cmph5tools and h5repack are required.)

    $ pbalign --forQuiver your_movie.bas.h5 your_reference.fasta out.cmp.h5



(3) Use pbalign as a library through Python API.

- Example (3.1) ::

    $ python
    >>> from pbalign.pbalignrunner import PBAlignRunner
    >>> # Specify arguments in a list.
    >>> args = ['--maxHits', '20', 'tests/data/example_read.fasta',\
    ...         'tests/data/example_ref.fasta', 'example.sam']
    >>> # Create a PBAlignRunner object.
    >>> a = PBAlignRunner(args)
    >>> # Execute.
    >>> exitCode = a.start()
    >>> # Show all files used.
    >>> print a.fileNames


Usage
-----
::

    usage: pbalign [-h] [--verbose] [--version] [--profile] [--debug]
                   [--regionTable REGIONTABLE] [--configFile CONFIGFILE]
                   [--algorithm {blasr,bowtie}] [--maxHits MAXHITS]
                   [--minAnchorSize MINANCHORSIZE]
                   [--useccs {useccs,useccsall,useccsdenovo}]
                   [--noSplitSubreads] [--nproc NPROC]
                   [--algorithmOptions ALGORITHMOPTIONS]
                   [--maxDivergence MAXDIVERGENCE] [--minAccuracy MINACCURACY]
                   [--minLength MINLENGTH]
                   [--scoreFunction {alignerscore,editdist,blasrscore}]
                   [--scoreCutoff SCORECUTOFF]
                   [--hitPolicy {randombest,allbest,random,all}] [--forQuiver]
                   [--seed SEED] [--tmpDir TMPDIR]
                   inputFileName referencePath outputFileName
    
    Mapping PacBio sequences to references using an algorithm
    selected from a selection of supported command-line alignment
    algorithms. Input can be a fasta, pls.h5, bas.h5 or ccs.h5
    file or a fofn (file of file names). Output is in either
    cmp.h5 or sam format.
    
    positional arguments:
      inputFileName         The input file can be a fasta, pls.h5, bas.h5, ccs.h5
                            file or a fofn.
      referencePath         Either a reference fasta file or a reference repository.
      outputFileName        The output cmp.h5 or sam file.
    
    optional arguments:
      -h, --help            show this help message and exit
      --verbose, -v         Set the verbosity level
      --version             show program's version number and exit
      --profile             Print runtime profile at exit
      --debug               Run within a debugger session
      --regionTable REGIONTABLE
                            Specify a region table for filtering reads.
      --configFile CONFIGFILE
                            Specify a set of user-defined argument values.
      --algorithm {blasr,bowtie}
                            Select an aligorithm from ('blasr', 'bowtie').
                            Default algorithm is blasr.
      --maxHits MAXHITS     The maximum number of matches of each read to the
                            reference sequence that will be evaluated. Default
                            value is 10.
      --minAnchorSize MINANCHORSIZE
                            The minimum anchor size defines the length of the read
                            that must match against the reference sequence. Default
                            value is 12.
      --useccs {useccs,useccsall,useccsdenovo}
                            Map the ccsSequence to the genome first, then align
                            subreads to the interval that the CCS reads mapped to.
                              useccs: only maps subreads that span the length of
                                      the template.
                              useccsall: maps all subreads.
                              useccsdenovo: maps ccs only.
      --noSplitSubreads     Do not split reads into subreads even if subread
                            regions are available.
                            Default value is False.
      --nproc NPROC         Number of threads. Default value is 8.
      --algorithmOptions ALGORITHMOPTIONS
                            Pass alignment options through.
      --maxDivergence MAXDIVERGENCE
                            The maximum allowed percentage divergence of a read
                            from the reference sequence. Default value is 30.
      --minAccuracy MINACCURACY
                            The minimum percentage accuracy of alignments that
                            will be evaluated. Default value is 70.
      --minLength MINLENGTH
                            The minimum aligned read length of alignments that
                            will be evaluated. Default value is 50.
      --scoreFunction {alignerscore,editdist,blasrscore}
                            Specify a score function for evaluating alignments.
                              alignerscore : aligner's score in the SAM tag 'as'.
                              editdist     : edit distance between read and reference.
                              blasrscore   : blasr's default score function.
                            Default value is alignerscore.
      --scoreCutoff SCORECUTOFF
                            The worst score to output an alignment.
      --hitPolicy {randombest,allbest,random,all}
                            Specify a policy for how to treat multiple hit
                              random    : selects a random hit.
                              all       : selects all hits.
                              allbest   : selects all the best score hits.
                              randombest: selects a random hit from all best
                                          alignment score hits.
                            Default value is randombest.
      --forQuiver           The output cmp.h5 file which will be sorted, loaded
                            with pulse information, and repacked, so that it
                            can be consumed by quiver directly. This requires
                            the input file to be in PacBio bas/pls.h5 format.
                            Default value is False.
      --seed SEED           Initialize the random number generator with a none-zero
                            integer. Zero means that current system time is used.
                            Default value is 1.
      --tmpDir TMPDIR       Specify a directory for saving temporary files.
                            Default is /scratch.
