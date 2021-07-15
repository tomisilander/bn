#!/usr/bin/env python
from itertools import imap, izip
import utils


def ssi(i, vci, bn, dt):
    ss = {}

    pi = list(bn.parents(i))
    pi.sort()
    
    for d in imap(list, dt.dats()):

        di = d[i]
        if di == -1 : continue
                
        pcfg = tuple(imap(d.__getitem__, pi)) # maybe ()
        if -1 in pcfg: continue
        
        if pcfg not in ss :  ss[pcfg] = [0]*vci

        ss[pcfg][di] += 1

    return utils.sparse_func(ss, (0,)*vci)


def sss(bn, dt):
    for i,vci in izip(bn.vars(), dt.nof_vals()):
        yield ssi(i, vci, bn, dt)
