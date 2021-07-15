#!/bin/bash -v

# let us turn the data into binary format needed for structure learning

bn_dat2bdt data/iris.vd data/iris.idt data/iris.bdt

# and then run structure learning for 10 seconds

mkdir -p res
bn_stocgreedy -t 10s -o res/iris.bn data/iris.bdt

# now let us learn the parameters

bn_model  data/iris.vd res/iris.bn data/iris.idt res/iris.bnm

# and then use it to compute log_probability of the data

bn_logprob  res/iris.bnm data/iris.vd data/iris.idt 
