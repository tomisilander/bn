#!/usr/bin/env python
import sys, random
import bnmodel, bn.vd

def order(bns):
    o=[]
    ls = [len(bns.parents(v)) for v in bns.vars()]

    while len(o) < bns.varc:
        for v,l in enumerate(ls):
            if l == 0:
                o.append(v)
                ls[v] = -1
                for c in bns.children(v):
                    ls[c] -= 1
    return o

def wheel(theta):
    p = random.random()
    s = 0.0
    for n,t in enumerate(theta):
        s += t
        if s > p:
            return n
    return len(theta) - 1


def gen1(ord, bnm):
    bns = bnm.bn
    d = [0]*len(ord)
    for o in ord:
        d[o] = wheel(bnm.thetd(o,d))
    return d

def gen(bnm, N):
    ord = order(bnm.bn)
    for n in xrange(N):
        yield gen1(ord, bnm)


def main(vdfile, modelfile, N, outfile="-"):
    valcs = bn.vd.load(vdfile)
    bnm = bnmodel.load(modelfile, valcs)

    outf = outfile == "-" and sys.stdout or file(outfile, "w")
    for d in gen(bnm, N):
        print >> outf, " ".join(map(str, d))
    if outfile != "-": outf.close()

if __name__ == '__main__':
    from coliche import che
    che(main,
        '''vdfile; modelfile; N (int)
        -o outfile
        ''')
