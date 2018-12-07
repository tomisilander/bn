#!/usr/bin/python

from random import random, randint
from itertools import imap, izip, islice
from bn.util.bn2totord  import gen_totord
import bn.vd, bn.model.bnmodel, sigpool

class Gifr(): pass

def bnm2gifr(valcs,bnm):
    bnt = bnm.bn
    gifr = Gifr()
    gifr.parents =  [list(sorted(bnt.parents(v))) for v in bnt.vars()]
    gifr.children = [list(sorted(bnt.children(v))) for v in bnt.vars()]
    gifr.bnm = bnm
    gifr.valcs = valcs
    return gifr

def wheel(ps):
    su = 0.0
    r = random()
    for i,p in enumerate(ps):
        su += p
        if r<=su: return i
    return len(ps) - 1 

def nze(d): 
    nzer = 1.0/sum(d)
    for k in xrange(len(d)):
        d[k] *= nzer

def mb(v,cfg, gifr):
    vpcfg = map(cfg.__getitem__, gifr.parents[v])
    vdstr = gifr.bnm.thti(v)[tuple(vpcfg)][:]
    for c in gifr.children[v]:
        cval = cfg[c]
        vpos = next(i for (i,cp) in enumerate(gifr.parents[c]) if cp==v)

        # build parent cfg for c
        cpcfg = map(cfg.__getitem__, gifr.parents[c])
    
        thtc = gifr.bnm.thti(c) 
        for vval in xrange(gifr.valcs(v)):
            cpcfg[vpos] = vval
            vdstr[vval] *= thtc[tuple(cpcfg)][cval]
        nze(vdstr)
    return vdstr

def lw(v,cfg, gifr):
    vpcfg = map(cfg.__getitem__, gifr.parents[v])
    vdstr = gifr.bnm.thti(v)[tuple(vpcfg)][:]
    return vdstr

def gs(xs, e, gifr, time, gibbs=True): # xs are of interest, e is evidence
    bnt = gifr.bnm.bn
 
    freevars = tuple(v for v in bnt.vars() if v not in e)
    if not gibbs:
        tord = list(gen_totord(bnt))
        freevars = sorted(freevars, key=lambda v:tord.index(v))

    counts = {}  # For counting xcfgs
    # initial configuration
    cfg = [e[v] if (v in e) else randint(0,gifr.valcs(v)-1) 
           for v in bnt.vars()]

    sigpool.watch('SIGUSR2')
    if time: sigpool.wait_n_raise(time, 'SIGUSR2')

    while True:
        w = 1.0
        if gibbs:
            for v in freevars: cfg[v] = wheel(mb(v,cfg,gifr))
        else:
            for v in freevars: cfg[v] = wheel(lw(v,cfg,gifr))
            for v in e:
                vpcfg = map(cfg.__getitem__, gifr.parents[v])
                w *= gifr.bnm.thti(v)[tuple(vpcfg)][e[v]]

        xcfg = tuple(cfg[x] for x in xs)
        counts[xcfg] = counts.get(xcfg,0) + w

        if 'SIGUSR2' in sigpool.flags: break
        sigpool.flags.remove('SIGUSR2')

    # normalize
    nzer = 1.0/sum(counts.itervalues())
    for xcfg in counts: counts[xcfg] *= nzer
    return counts

def str2q(l):
    xspart, epart = l.split('|')
    et = map(int,epart.strip().split())
    xs = map(int,xspart.strip().split())
    xs.sort()
    e = dict(izip(islice(et, 0,None,2), islice(et, 1,None,2)))
    return xs, e

def main(vdfile, bnmfile, query='', time="10s", lw=False):
    valcs = bn.vd.load(vdfile)
    bnm = bn.model.bnmodel.load(bnmfile,valcs)
    gifr = bnm2gifr(valcs,bnm)
    if len(query)>0:
        (xs,e) = str2q(query)
        t = sigpool.str2time(time)
        return gs(xs,e,gifr,t, gibbs = not lw)
    return None

if __name__ == '__main__':
    from coliche import che
    r = che(main,
            """vdfile; bnmfile
    -q query  : example '0 2 | 1 1 3 0'
    -t time   : like -t '4d 3h 5m 5[s]' (default till SIGUSR2)
    --lw      : use likelihood weighting instead of Gibbs sampling
    """)
    if r!=None:
        print r
