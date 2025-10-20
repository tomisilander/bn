#!/usr/bin/env python

import math

import disdat
import bn.model.bnmodel
import bn.vd

def gen_logprobs(bnm, tstdat, base=None):
    if base is not None:
        lbase = math.log(base)

    for d in tstdat.dats():
        lp = bnm.logprob_d(d)
        if base: 
            lp /= lbase
        yield lp

def logprob(bnm, tstdat, base=None):
    lp = bnm.logprob_D(tstdat)
    if base: 
        lp /= math.log(base)
    return lp

def main(args):
    # modelfile, vdfile, tstfile, 
    # density=False, base=None, avg=False, verbose=False):
    valcs = bn.vd.load(args.vdfile)
    bnm = bn.model.bnmodel.load(args.modelfile, valcs)
    if args.density:
        bnm.use_density = True
    tstdat = disdat.RowData(args.vdfile, args.tstfile)
    if args.verbose:
        for lp in gen_logprobs(bnm,tstdat, args.base):
            print(lp)
    else:
        lp =  logprob(bnm, tstdat, args.base)
        print(lp/tstdat.N() if args.avg else lp)

def parse_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('modelfile', help='The model file to use.')
    parser.add_argument('vdfile', help='The value distribution file to use.')
    parser.add_argument('tstfile', help='The test data file to use.')
    parser.add_argument('-d', '--density', action='store_true',
                        help='Use ranges in vdfile to give density')
    parser.add_argument('-b', '--base', type=float, default=None,
                        help='Log base (default natural)')
    parser.add_argument('-a', '--avg', action='store_true',
                        help='Give average instead of sum')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='List individual logprobs')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(args)
    