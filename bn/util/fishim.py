#!/usr/bin/python

import sys
import bn.model.bnmodel
import bn.vd
import bn.infer.ifr
from itertools import combinations_with_replacement, imap, product
from math import exp


def build_pprobs(ifr, bnm, valcs, i):
    cpot = ifr.pots[ifr.vclqs[i]]
    pi = list(bnm.bn.parents(i))
    pi.sort()
    return (cpot >> bn.infer.pot.Potential(pi, valcs, 0.0)).normalize()


def build_cfgextractors(bnet, i):
    pi = list(bnet.parents(i))
    pi.sort()
    return lambda d: (d[i], tuple(imap(d.__getitem__, pi)))


def lognorm(ls):
    loga = sum(ls) / len(ls)
    try:
        nonp = map(exp, imap((-loga).__add__, ls))
        nzer = 1.0/sum(nonp)
        return map(nzer.__mul__, nonp)
    except:
        # remove smallest and retry
        ls = list(ls)
        minl = min(ls)
        mini = ls.index(minl)
        del ls[mini]
        p = lognorm(ls)      # for long ls this may stack overflow
        p.insert(mini, 0.0)  # insert back
        return p


def vrsims(x, y, pprobs, cfgextractors, bnm):
    bns = bnm.bn
    for vr in bns.vars():
        (xvl, xp), (yvl, yp) = map(cfgextractors[vr], (x, y))
        if xp != yp:
            yield 0.0
        else:
            pp = pprobs[vr][xp]
            if xvl != yvl:
                yield -1.0/pp
            else:
                pxvl = bnm.theta(vr, xp)[xvl]
                yield (1-pxvl)/pxvl/pp


def gen_versions(x, cix, bnm):
    if x[cix] != -1:
        yield x
    else:
        nx = list(x)
        for c in range(bnm.valcounts[cix]):
            nx[cix] = c
            yield list(nx)


def sim(x, y, pprobs, cfgextractors, bnm, cix):
    if cix is None:
        fkterms = list(vrsims(x, y, pprobs, cfgextractors, bnm))
        return sum(fkterms)
    else:
        xs = list(gen_versions(x, cix, bnm))
        xprobs = (1.0,) if len(xs) == 1 else lognorm([bnm.logprob_d(x) for x in xs])
        ys = list(gen_versions(y, cix, bnm))
        yprobs = (1.0,) if len(ys) == 1 else lognorm([bnm.logprob_d(y) for y in ys])

        # if this works you can turn this into a one big sum
        res = 0.0
        for (x, xp), (y, yp) in product(zip(xs, xprobs), zip(ys, yprobs)):
            res += xp*yp*sum(vrsims(x, y, pprobs, cfgextractors, bnm))
        return res


def main(vdfile, bnmfile, ifrdir, cix=None, matrix=False):
    valcs = bn.vd.load(vdfile)
    bnm = bn.model.bnmodel.load(bnmfile, valcs)
    ifr = bn.infer.ifr.load(ifrdir)
    pfs = [build_pprobs(ifr, bnm, valcs, i) for i in bnm.bn.vars()]
    cfgxs = [build_cfgextractors(bnm.bn, i) for i in bnm.bn.vars()]
    dats = [map(int, l.split()) for l in sys.stdin]
    N = len(dats)
    combs = combinations_with_replacement(enumerate(dats), 2)
    if matrix:
        K = [[0.0]*N for i in range(N)]
        for((i1, d1), (i2, d2)) in combs:
            K[i1][i2] = K[i2][i1] = sim(d1, d2, pfs, cfgxs, bnm, cix)

        for i in range(N):
            print(' '.join(map(str, K[i])))
    else:
        for((i1, d1), (i2, d2)) in combs:
            print(i1, i2, sim(d1, d2, pfs, cfgxs, bnm, cix))


if __name__ == '__main__':
    from coliche import che
    che(main, """vdfile; bnmfile; ifrdir
    -c --cix cix (int) : class index counting from 0 : default None
    -m --matrix : print in matrix form""")
