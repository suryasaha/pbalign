Test mask_aligned_reads.py 
  $ CURDIR=$TESTDIR
  $ DATDIR=/mnt/secondary-siv/testdata/BlasrTestData/pbalign/data/test_mask_aligned_reads
  $ OUTDIR=$CURDIR/../out
  $ STDDIR=$DATDIR/../../stdout

#Test mask_aligned_reads.py with movie.rgn.h5

  $ CMPFILE=$DATDIR/in.cmp.h5
  $ INRGNFOFN=$DATDIR/in_rgn.fofn
  $ OUTRGNFOFN=$OUTDIR/out_rgn.fofn
  $ TMP1=$OUTDIR/test_mask_aligned_reads.tmp1
  $ TMP2=$OUTDIR/test_mask_aligned_reads.tmp2

  $ rm -rf $OUTDIR/out_rgn
  $ maskAlignedReads.py $CMPFILE $INRGNFOFN $OUTRGNFOFN 
  $ echo $?
  0
  $ cat $OUTRGNFOFN | xargs ls -1
  */out_rgn/m121215_065521_richard_c100425710150000001823055001121371_s1_p0.rgn.h5 (glob)
  */m121215_065521_richard_c100425710150000001823055001121371_s2_p0.rgn.h5 (glob)
  $ h5dump -d /PulseData/Regions $OUTDIR/out_rgn/m121215_065521_richard_c100425710150000001823055001121371_s1_p0.rgn.h5 | sed '1d' > $TMP1 
  $ h5dump -d /PulseData/Regions $STDDIR/out_rgn/m121215_065521_richard_c100425710150000001823055001121371_s1_p0.rgn.h5 | sed '1d' > $TMP2 
  $ diff $TMP1 $TMP2 

  $ h5dump -d /PulseData/Regions $OUTDIR/out_rgn/m121215_065521_richard_c100425710150000001823055001121371_s2_p0.rgn.h5 | sed '1d' > $TMP1 
  $ h5dump -d /PulseData/Regions $STDDIR/out_rgn/m121215_065521_richard_c100425710150000001823055001121371_s2_p0.rgn.h5 | sed '1d' > $TMP2 
  $ diff $TMP1 $TMP2 

#Test while cmp.h5 alignments are generated from multiple movie.bax.h5
  $ CMPFILE=$DATDIR/in_2.cmp.h5
  $ INRGNFOFN=$DATDIR/in_rgn_2.fofn
  $ OUTRGNFOFN=$OUTDIR/out_rgn_2.fofn

  $ maskAlignedReads.py $CMPFILE $INRGNFOFN $OUTRGNFOFN 
  $ echo $?
  0
  $ cat $OUTRGNFOFN | xargs ls -1
  */out_rgn_2/m130322_020628_ethan_c100499142550000001823070408081367_s1_p0.1.rgn.h5 (glob)
  */m130322_020628_ethan_c100499142550000001823070408081367_s1_p0.2.rgn.h5 (glob)


