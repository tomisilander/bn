#!/usr/bin/env python

import coliche, disdat, bn.model.bnmodel, bn.vd, math

def gen_logprobs(bnm, tstdat, base=None):
    if base != None:
        lbase = math.log(base)

    for d in tstdat.dats():
        lp = bnm.logprob_d(d)
        if base: lp /= lbase
        yield lp

def logprob(bnm, tstdat, base=None):
    lp = bnm.logprob_D(tstdat)
    if base: lp /= math.log(base)
    return lp

def main(modelfile, vdfile, tstfile, 
         density=False, base=None, avg=False, verbose=False):
    valcs = bn.vd.load(vdfile)
    bnm = bn.model.bnmodel.load(modelfile, valcs)
    if density:
        bnm.use_density = True
    tstdat = disdat.RowData(vdfile, tstfile)
    if verbose:
        for lp in gen_logprobs(bnm,tstdat,base):
            print lp
    else:
        lp =  logprob(bnm, tstdat, base)
        print avg and lp/tstdat.N() or lp

if __name__ == '__main__':
    coliche.che(main,
                '''modelfile; vdfile; tstfile
                -d --density : use ranges in vdfile to give density
                -b --base base (float) : log base (default natural)
                -a --avg : give average instead of sum
                -v --verbose: list individual logprobs''')
