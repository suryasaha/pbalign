Note:
Program name has been changed from `pbalign.py` in version 0.1.0 
to `pbalign` in 0.2.0, pseudo namespace pbtools has been removed also.

Test pbalign
  $ CURDIR=$TESTDIR
  $ DATDIR=$CURDIR/../data
  $ OUTDIR=$CURDIR/../out
  $ STDDIR=$CURDIR/../stdout

#Test pbalign with all combinations of input & output formats
#input, reference and output formats are: fasta, fasta, and sam/cmp.h5
  $ READFILE=$DATDIR/lambda_query.fasta
  $ REFFILE="/mnt/secondary-siv/references/lambda/sequence/lambda.fasta"

  $ SAMOUT=$OUTDIR/lambda.sam
  $ CMPOUT=$OUTDIR/lambda.cmp.h5

  $ rm -f $SAMOUT $CMPOUT
  $ pbalign $READFILE $REFFILE $SAMOUT
  $ tail -n+6 $SAMOUT | cut -f 1-11 | sort | md5sum
  ea31763bc847a6c75d3ddb5fb6036489  -

  $ pbalign $READFILE $REFFILE $CMPOUT
  $ h5dump -g /ref000001 $CMPOUT > tmpfile 
  $ sed -n '2,11p' tmpfile
  GROUP "/ref000001" {
     GROUP "m120619_015854_42161_c100392070070000001523040811021231_s1_p0" {
        DATASET "AlnArray" {
           DATATYPE  H5T_STD_U8LE
           DATASPACE  SIMPLE { ( 48428 ) / ( H5S_UNLIMITED ) }
           DATA {
           (0): 34, 136, 17, 17, 34, 17, 136, 136, 136, 17, 136, 34, 136, 68,
           (14): 128, 34, 17, 136, 34, 17, 136, 17, 2, 34, 136, 136, 34, 34,
           (28): 68, 17, 68, 34, 17, 136, 136, 136, 17, 136, 136, 1, 17, 68,
           (42): 34, 17, 136, 136, 136, 34, 68, 34, 136, 17, 136, 17, 17, 68,
  $ rm tmpfile
 


#input, reference and output formats are: fasta, folder and sam/cmp.h5
  $ READFILE=$DATDIR/lambda_query.fasta
  $ REFFILE=/mnt/secondary-siv/references/lambda/

  $ SAMOUT=$OUTDIR/lambda2.sam
  $ CMPOUT=$OUTDIR/lambda2.cmp.h5

  $ rm -f $SAMOUT $CMPOUT
  $ pbalign $READFILE $REFFILE $SAMOUT
  $ tail -n+6 $SAMOUT  | cut -f 1-11 | sort | md5sum
  ea31763bc847a6c75d3ddb5fb6036489  -

  $ pbalign $READFILE $REFFILE $CMPOUT
  $ h5dump -g /ref000001 $CMPOUT > tmpfile 
  $ sed -n '2,11p' tmpfile
  GROUP "/ref000001" {
     GROUP "m120619_015854_42161_c100392070070000001523040811021231_s1_p0" {
        DATASET "AlnArray" {
           DATATYPE  H5T_STD_U8LE
           DATASPACE  SIMPLE { ( 48428 ) / ( H5S_UNLIMITED ) }
           DATA {
           (0): 34, 136, 17, 17, 34, 17, 136, 136, 136, 17, 136, 34, 136, 68,
           (14): 128, 34, 17, 136, 34, 17, 136, 17, 2, 34, 136, 136, 34, 34,
           (28): 68, 17, 68, 34, 17, 136, 136, 136, 17, 136, 136, 1, 17, 68,
           (42): 34, 17, 136, 136, 136, 34, 68, 34, 136, 17, 136, 17, 17, 68,
  $ rm -f tmpfile


#input, reference and output formats are: fofn, fasta and sam/cmp.h5
  $ READFILE=$DATDIR/lambda_bax.fofn
  $ REFFILE="/mnt/secondary-siv/references/lambda/sequence/lambda.fasta"

  $ SAMOUT=$OUTDIR/lambda3.sam
  $ CMPOUT=$OUTDIR/lambda3.cmp.h5

  $ rm -f $SAMOUT $CMPOUT
  $ pbalign $READFILE $REFFILE $SAMOUT
  $ tail -n+6 $SAMOUT  | cut -f 1-11 | sort | md5sum
  e5c29fba1efbbfbe164fa2797408dbf6  -

  $ pbalign $READFILE $REFFILE $CMPOUT
  $ h5dump -g /ref000001 $CMPOUT > tmpfile 
  $ sed -n '2,11p' tmpfile
  GROUP "/ref000001" {
     GROUP "m130220_114643_42129_c100471902550000001823071906131347_s1_p0" {
        DATASET "AlnArray" {
           DATATYPE  H5T_STD_U8LE
           DATASPACE  SIMPLE { ( 79904 ) / ( H5S_UNLIMITED ) }
           DATA {
           (0): 136, 34, 136, 34, 136, 68, 34, 68, 68, 68, 17, 68, 136, 68,
           (14): 136, 2, 34, 68, 68, 68, 17, 17, 136, 17, 17, 136, 136, 1, 17,
           (29): 17, 17, 34, 68, 17, 136, 68, 2, 17, 34, 17, 34, 17, 68, 68,
           (44): 68, 8, 136, 136, 17, 68, 34, 68, 34, 68, 136, 17, 2, 17, 130,
  $ rm -f tmpfile


#input, reference and output formats are: fofn, folder and sam/cmp.h5
  $ READFILE=$DATDIR/lambda_bax.fofn
  $ REFFILE=/mnt/secondary-siv/references/lambda/

  $ SAMOUT=$OUTDIR/lambda4.sam
  $ CMPOUT=$OUTDIR/lambda4.cmp.h5

  $ rm -f $SAMOUT $CMPOUT
  $ pbalign $READFILE $REFFILE $SAMOUT
  $ tail -n+6 $SAMOUT  | cut -f 1-11 | sort | md5sum
  e5c29fba1efbbfbe164fa2797408dbf6  -

  $ pbalign $READFILE $REFFILE $CMPOUT
  $ h5dump -g /ref000001 $CMPOUT > tmpfile 
  $ sed -n '2,11p' tmpfile
  GROUP "/ref000001" {
     GROUP "m130220_114643_42129_c100471902550000001823071906131347_s1_p0" {
        DATASET "AlnArray" {
           DATATYPE  H5T_STD_U8LE
           DATASPACE  SIMPLE { ( 79904 ) / ( H5S_UNLIMITED ) }
           DATA {
           (0): 136, 34, 136, 34, 136, 68, 34, 68, 68, 68, 17, 68, 136, 68,
           (14): 136, 2, 34, 68, 68, 68, 17, 17, 136, 17, 17, 136, 136, 1, 17,
           (29): 17, 17, 34, 68, 17, 136, 68, 2, 17, 34, 17, 34, 17, 68, 68,
           (44): 68, 8, 136, 136, 17, 68, 34, 68, 34, 68, 136, 17, 2, 17, 130,
  $ rm tmpfile
 

#Test --maxDivergence --minAnchorSize --minAccuracy 
  $ READFILE=$DATDIR/lambda_query.fasta
  $ REFFILE="/mnt/secondary-siv/references/lambda/sequence/lambda.fasta"

  $ SAMOUT=$OUTDIR/lambda5.sam

  $ rm -f $SAMOUT
  $ pbalign --maxDivergence 40 --minAnchorSize 20 --minAccuracy 80 $READFILE $REFFILE $SAMOUT 
  $ tail -n+6 $SAMOUT  | cut -f 1-11 | sort | md5sum
  29f8897b8ee6d4b7fff126d374edb306  -

#Test whether pbalign interprets minAccuracy and maxDivergence correclty.
  $ rm -f $SAMOUT
  $ pbalign --maxDivergence 0.4 --minAnchorSize 20 --minAccuracy 0.8 $READFILE $REFFILE $SAMOUT 
  $ tail -n+6 $SAMOUT  | cut -f 1-11 | sort | md5sum
  29f8897b8ee6d4b7fff126d374edb306  -

#Test --hitPolicy  random
  $ SAMOUT=$OUTDIR/lambda_hitPolicy_random.sam

  $ rm -f $SAMOUT
  $ pbalign --hitPolicy random --seed 1 $READFILE $REFFILE $SAMOUT 
  $ tail -n+6 $SAMOUT  | cut -f 1-11 | sort | md5sum
  ea31763bc847a6c75d3ddb5fb6036489  -

#Test --hitPolicy  all
  $ SAMOUT=$OUTDIR/lambda_hitPolicy_all.sam

  $ rm -f $SAMOUT
  $ pbalign --hitPolicy all $READFILE $REFFILE $SAMOUT 
  $ tail -n+6 $SAMOUT  | cut -f 1-11 | sort | md5sum
  2022614eb99fe3288c332aadcfefe739  -


#Test --hitPolicy  randombest
  $ SAMOUT=$OUTDIR/lambda_hitPolicy_randombest.sam

  $ rm -f $SAMOUT
  $ pbalign  --hitPolicy randombest --seed 1 $READFILE $REFFILE $SAMOUT
  $ tail -n+6 $SAMOUT  | cut -f 1-11 | sort | md5sum
  ea31763bc847a6c75d3ddb5fb6036489  -

#Test --scoreFunction
  $ SAMOUT=$OUTDIR/lambda_scoreFunction_editdist.sam

  $ rm -f $SAMOUT
  $ pbalign $READFILE $REFFILE $SAMOUT --scoreFunction editdist
  $ tail -n+6 $SAMOUT  | cut -f 1-11 | sort | md5sum
  ea31763bc847a6c75d3ddb5fb6036489  -


#Test --hitPolicy  allbest
  $ READFILE=$DATDIR/example_read.fasta
  $ REFFILE=$DATDIR/example_ref.fasta
  $ SAMOUT=$OUTDIR/hitPolicy_allbest.sam

  $ rm -f $SAMOUT
  $ pbalign --hitPolicy allbest $READFILE $REFFILE $SAMOUT 
  $ tail -n+8 $SAMOUT  | cut -f 1-11 | sort | md5sum
  6e68a0902f282c25526e14e5516e663b  -

#Test --useccs=useccsdenovo, whether attribute /ReadType is 'CCS'
  $ READFILE=$DATDIR/lambda_bax.fofn
  $ REFFILE="/mnt/secondary-siv/references/lambda/sequence/lambda.fasta"
  $ CMPOUT=$OUTDIR/lambda_denovo.cmp.h5

  $ rm -f $CMPOUT
  $ pbalign $READFILE $REFFILE $CMPOUT --useccs=useccsdenovo --algorithmOptions=" -holeNumbers 0-100"
  $ h5dump -a /ReadType $CMPOUT | grep "CCS"
     (0): "CCS"

#Test --forQuiver can not be used together with --useccs
  $ pbalign $READFILE $REFFILE $CMPOUT --useccs=useccsdenovo --algorithmOptions=" -holeNumbers 0-100" --forQuiver 1>/dev/null 2>/dev/null || echo 'fail as expected'
  fail as expected


#Test whether pbalign can produce sam output for non-PacBio reads
#  $ READFILE=$DATDIR/notSMRT.fasta
#  $ REFFILE="/mnt/secondary-siv/references/lambda/sequence/lambda.fasta"
#  $ SAMOUT=$OUTDIR/notSMRT.sam
#
#  $ rm -f $SAMOUT $CMPOUT
#  $ pbalign $READFILE $REFFILE $SAMOUT


# Test whether (ccs.h5) produces
# identical results as (bas.h5 and --useccs=useccsdenovo).
  $ READFILE=$DATDIR/test_ccs.fofn 
  $ REFFILE=/mnt/secondary-siv/references/ecoli_k12_MG1655/sequence/ecoli_k12_MG1655.fasta
  $ CCS_CMPOUT=$OUTDIR/test_ccs.cmp.h5

  $ rm -f $CCS_CMPOUT
  $ pbalign $READFILE $REFFILE $CCS_CMPOUT

  $ READFILE=$DATDIR/test_bas.fofn
  $ BAS_CMPOUT=$OUTDIR/test_bas.cmp.h5

  $ rm -f $BAS_CMPOUT
  $ pbalign $READFILE $REFFILE $BAS_CMPOUT --useccs=useccsdenovo

  $ h5diff $CCS_CMPOUT $BAS_CMPOUT /AlnGroup  /AlnGroup
  $ h5diff $CCS_CMPOUT $BAS_CMPOUT /AlnInfo   /AlnInfo
  $ h5diff $CCS_CMPOUT $BAS_CMPOUT /MovieInfo /MovieInfo
  $ h5diff $CCS_CMPOUT $BAS_CMPOUT /RefInfo   /RefInfo
  $ h5diff $CCS_CMPOUT $BAS_CMPOUT /ref000001 /ref000001


#Test pbalign with -filterAdapterOnly
  $ READFILE=$DATDIR/test_filterAdapterOnly.fofn
  $ REFDIR=/mnt/secondary-siv/testdata/BlasrTestData/pbalign/data/references/H1_6_Scal_6x/
  $ OUTPUT=$OUTDIR/test_filterAdapterOnly.sam
  $ rm -f $OUTPUT
  $ pbalign $READFILE $REFDIR $OUTPUT --filterAdapterOnly --algorithmOptions=" -holeNumbers 10817,14760" --seed=1 
  $ tail -n+6 $OUTPUT | cut -f 1-4

# Test pbalign with --pulseFile
# This is an experimental option which goes only with gmap,
# it enables users to bypass the pls2fasta step and use their own fasta 
# file instead, while keep the ability of generating cmp.h5 files with pulses 
# (i.e., --forQuiver). Eventually, we need to support --algorithm=blasr.
  $ OUTFILE=$OUTDIR/test_pulseFile.cmp.h5
  $ REFPATH=/mnt/secondary-siv/references/Ecoli_K12_DH10B/
  $ REFFILE=/mnt/secondary-siv/references/Ecoli_K12_DH10B/sequence/Ecoli_K12_DH10B.fasta
  $ pbalign $DATDIR/test_pulseFile.fasta $REFPATH $OUTFILE --pulseFile $DATDIR/test_pulseFile.fofn --forQuiver --algorithm gmap --byread
  $ echo $?
  0

  $ OUTFILE=$OUTDIR/test_pulseFile.cmp.h5
  $ REFPATH=/mnt/secondary-siv/references/Ecoli_K12_DH10B/
  $ REFFILE=/mnt/secondary-siv/references/Ecoli_K12_DH10B/sequence/Ecoli_K12_DH10B.fasta
  $ rm -f $OUTFILE
  $ pbalign $DATDIR/test_pulseFile.fasta $REFPATH $OUTFILE --pulseFile $DATDIR/test_pulseFile.fofn --forQuiver --algorithm blasr --byread
  $ echo $?
  0

#Test pbalign with space in file names.
  $ FA=$DATDIR/dir\ with\ spaces/reads.fasta 
  $ pbalign "$FA" "$FA" $OUTDIR/with_space.sam
  $ echo $?
  0

#Test pbalign with -hitPolicy leftmost
  $ Q=$DATDIR/test_leftmost_query.fasta
  $ T=$DATDIR/test_leftmost_target.fasta
  $ O=$OUTDIR/test_leftmost_out.sam 
  $ pbalign $Q $T $O --hitPolicy leftmost
  $ echo $?
  0
  $ tail -n+6 $O | cut -f 4 
  1


