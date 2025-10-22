#!/bin/bash -v

cd ..

datadir=example/data
resdir=example/results

vdfile=$datadir/iris.vd
idtfile=$datadir/iris.idt
bdtfile=$datadir/iris.bdt

bnfile=$resdir/iris.bn
bnmfile=$resdir/iris.bnm

bens='python -m src.bens'

# let us turn the data into binary format needed for structure learning

$bens data dat2bdt $vdfile $idtfile $bdtfile

# and then run structure learning for 10 seconds

mkdir -p $resdir
$bens learn stocgreedy --time 10s --outfile $bnfile $bdtfile

# now let us learn the parameters

$bens model learn $vdfile $bnfile $idtfile $bnmfile

# and then use it to compute the average log_probability of the data

$bens model logprob $bnmfile $vdfile $idtfile --avg
