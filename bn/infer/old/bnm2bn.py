#!/usr/bin/python
import vd, bnmodel, coliche

def main(vdfile, mdlfile, bnfile):
    fmt = vd.load(vdfile)
    valcs = map(len, fmt.values)
    bnm = bnmodel.load(fmt.varnames, valcs, mdlfile)
    bnm.bn.save(bnfile)

coliche.che(main, 'vdfile; mdlfile; bnfile')

