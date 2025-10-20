#!/usr/bin/env python
import sys
import random
from bn.model.bnmodel import BnModel, load as load_model
from bn.bn import BN
import bn.vd

def gen_genorder(bns:BN):
    """
   Always generate child only after all its parents have been generated.
    """

    nof_pss = [len(bns.parents(v)) for v in bns.vars()]
    n = 0
    while n < bns.varc:
        for v, nof_ps in enumerate(nof_pss):
            if nof_ps == 0: # v has no parents.
                yield v
                n += 1
                nof_pss[v] = -1 # remove v from consideration bu setting it to -1
                # remove v from the parent count of its children.
                for c in bns.children(v):
                    nof_pss[c] -= 1

def wheel(theta):
    p = random.random()
    s = 0.0
    for n,t in enumerate(theta):
        s += t
        if s > p:
            return n
    return len(theta) - 1


def gen1(ord, bnm:BnModel):
    d = [0]*len(ord)
    for o in ord:
        d[o] = wheel(bnm.thetd(o,d))
    return d

def gen(bnm, N):
    ord = list(bnm.bn)
    for n in range(N):
        yield gen1(ord, bnm)


def main(args):
    valcs = bn.vd.load(args.vdfile)
    bnm = load_model(args.modelfile, valcs)

    for d in gen(bnm, args.N):
        print (" ".join(map(str, d)), file=args.outf)

if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    parser = ArgumentParser(description='Generate data for a Bayesian network.')
    parser.add_argument('vdfile', type=str, help='The value distribution file.')
    parser.add_argument('modelfile', type=str, help='The Bayesian network model file.')
    parser.add_argument('N', type=int, help='The number of samples to generate.')
    parser.add_argument('-o', '--outfile', type=FileType('w'), default="-", help='The output file. If not specified, the data will be printed to stdout.')

    main(parser.parse_args())
