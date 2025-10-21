#!/bin/bash -v

cd ..

# let us turn the data into binary format needed for structure learning

datadir=example/data
resdir=example/results
vdfile=$datadir/iris.vd
idtfile=$datadir/iris.idt
bdtfile=$datadir/iris.bdt
bnfile=$resdir/iris.bn

bens='python -m src.bens'
$bens data dat2bdt $vdfile $idtfile $bdtfile

# and then run structure learning for 10 seconds

mkdir -p $resdir
$bens learn stocgreedy --time 10s --outfile $bnfile $bdtfile

# # now let us learn the parameters
# 
# bn_model  data/iris.vd res/iris.bn data/iris.idt res/iris.bnm
# 
# # and then use it to compute log_probability of the data
# 
# bn_logprob  res/iris.bnm data/iris.vd data/iris.idt 
