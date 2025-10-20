#!/usr/bin/env python3
import sys
import typer
from bn import vd
from src.model import bnmodel
from src.infer.ifr import load as load_ifr
from src.infer.pot import Potential
from itertools import product, combinations_with_replacement
from math import exp

app = typer.Typer()

def build_pprobs(ifr, bnm, valcs, i):
    cpot = ifr.pots[ifr.vclqs[i]]
    pi = list(bnm.bn.parents(i))
    pi.sort()
    return (cpot >> Potential(pi, valcs, 0.0)).normalize()


def build_cfgextractors(bnet, i):
    pi = list(bnet.parents(i))
    pi.sort()
    return lambda d: (d[i], tuple(d[p] for p in pi))


def lognorm(ls):
    loga = sum(ls) / len(ls)
    try:
        # materialize to list so we can sum and reuse
        nonp = [exp(x - loga) for x in ls]
        nzer = 1.0 / sum(nonp)
        return [nzer * v for v in nonp]
    except Exception:
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


def gen_versions(x,vcs):
    misixs = [i for (i,v) in enumerate(x) if v == -1]
    if len(misixs)==0:
        yield x
    else:
        for mcfg in product(*(range(vcs[i]) for i in misixs)):
            nx = list(x)
            for (i,v) in zip(misixs,mcfg):
                nx[i]=v
            yield nx

def sim(x, y, pprobs, cfgextractors, bnm):
    xs = list(gen_versions(x, bnm.valcounts))
    xprobs = (1.0,) if len(xs) == 1 else lognorm([bnm.logprob_d(x) for x in xs])
    ys = list(gen_versions(y, bnm.valcounts))
    yprobs = (1.0,) if len(ys) == 1 else lognorm([bnm.logprob_d(y) for y in ys])

    return sum(xp*yp*sum(vrsims(x, y, pprobs, cfgextractors, bnm))
               for (x, xp), (y, yp) in
               product(zip(xs, xprobs), zip(ys, yprobs)))


@app.command()
def fishim(vdfile: str, bnmfile: str, ifrdir: str, matrix: bool = False):
    valcs = vd.load(vdfile)
    bnm = bnmodel.load(bnmfile, valcs)
    ifr = load_ifr(ifrdir)
    pfs = [build_pprobs(ifr, bnm, valcs, i) for i in bnm.bn.vars()]
    cfgxs = [build_cfgextractors(bnm.bn, i) for i in bnm.bn.vars()]
    # make each row a concrete list of ints
    dats = [list(map(int, line.split())) for line in sys.stdin]
    N = len(dats)
    combs = combinations_with_replacement(enumerate(dats), 2)
    if matrix:
        K = [[0.0]*N for i in range(N)]
        for((i1, d1), (i2, d2)) in combs:
            K[i1][i2] = K[i2][i1] = sim(d1, d2, pfs, cfgxs, bnm)

        for i in range(N):
            print(' '.join(map(str, K[i])))
    else:
        for((i1, d1), (i2, d2)) in combs:
            print(i1, i2, sim(d1, d2, pfs, cfgxs, bnm))


if __name__ == "__main__":
    app()
