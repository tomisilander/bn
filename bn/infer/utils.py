#!/usr/bin/python

from itertools import izip, imap
import operator


def sparse_func(d, default):
    def f(k):
        return d.get(k, default)
    f.dict = d
    f.default = default
    return f


# builds function that turns configuration to index

def posvals(vcs):
    pvs = [1]
    for vc in vcs:
        pvs.append(pvs[-1] * vc)
    return pvs

def cfg2ixer(vcs):
    if vcs:
        pvs = posvals(vcs)
        return lambda xs: sum(imap(operator.__mul__, xs, pvs))
    else :
        return lambda xs: -1

# builds function that turns index to configuration

def ix2cfger(vcs, as_list = False):
    
    def cfg(ix):
        lst = []
        if ix != -1:        
            for vc in vcs:
                ix, r = divmod(ix, vc)
                lst.append(r)


        if as_list:
            return lst
        else:
            return tuple(lst)

    return lambda ix: cfg(ix)


# parents ordered

def ops(i, bn):
    ps = list(bn.parents(i))
    ps.sort()
    return ps


def pcfgc(i, bn, valcs):
    return nof_cfgs(valcs(list(bn.parents(i))))
    
    
def cfgs(vcs, as_list = False):

    cfger = ix2cfger(vcs, as_list)

    if not vcs:
        yield cfger(-1)
        return

    cfgc  = reduce(operator.__mul__,vcs,1)

    for i in xrange(cfgc):
        yield cfger(i)


def cfgs_old(vcs):

    if not vcs:
        yield ()
        return

    len_cfg = len(vcs)
    
    cfg = [0] * len_cfg
    p = 0
    while True:

        yield cfg
        cfg[p] += 1

        while cfg[p] == vcs[p]:
            p+=1
            if p == len_cfg : return
            cfg[p] += 1

        cfg[:p] = [0]*p
        p=0

def nof_cfgs(vcs):
    return reduce(operator.mul, vcs, 1)
