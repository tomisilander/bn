#!/usr/bin/python

import vd, bnmodel, coliche, sdt, utils

def get_thetas(bnm):
    for i in bnm.bn.vars():
        vci = bnm.valcounts[i]
        uni = [1.0/vci] * vci
        thi = bnm.thti(i)
        yield utils.sparse_func(thi,uni)

def main(vdfile, mdlfile, thtfile):
    fmt = vd.load(vdfile)
    valcs = map(len, fmt.values)
    bnm = bnmodel.load(fmt.varnames, valcs, mdlfile)
    sdt.save(get_thetas(bnm),thtfile)

coliche.che(main, 'vdfile; mdlfile; thtfile')

