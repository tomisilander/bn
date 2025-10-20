#!/usr/bin/env python
from operator import __mul__
from functools import reduce

import bn.vd
import bn.bn

def nof_params(valcs, bns):
    nps=0
    for v in range(valcs.nof_vars):
        nof_pcfgs=reduce(__mul__,(valcs(p) for p in bns.parents(v)),1)
        nps += nof_pcfgs*(valcs(v)-1)

    return  nps

def main(args):
    print(nof_params(bn.vd.load(args.vdfile), bn.bn.load(args.bnfile)))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('vdfile', type=argparse.FileType('r'))
    parser.add_argument('bnfile', type=argparse.FileType('r'))
    args = parser.parse_args()
    main(args)
    