#!/usr/bin/env python
from operator import __mul__
import bn.vd, bn.bn

def nof_params(valcs, bns):
    nps=0
    for v in xrange(valcs.nof_vars):
        nof_pcfgs=reduce(__mul__,(valcs(p) for p in bns.parents(v)),1)
        nps += nof_pcfgs*(valcs(v)-1)

    return  nps

def main(vdfile, bnfile):
    print nof_params(bn.vd.load(vdfile), bn.bn.load(bnfile))

if __name__ == '__main__':
    import coliche
    coliche.che(main, '''vdfile; bnfile''')
