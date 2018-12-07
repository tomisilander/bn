#!/usr/bin/python

import bn
import coliche

def main(bnfile, v, bnout):

    bns = bn.load(bnfile,do_pic=False)
    mb =  bns.markovblanket(v,do_pic=False)
    mb.save(bnout)

if __name__ == '__main__':
    coliche.che(main,'bnfile; nodeindex (int); bnout')
