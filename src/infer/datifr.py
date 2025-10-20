from itertools import ifilter, izip, imap, product

"""
This is a naive inferer that estimates conditional probabilities directly
from frequencies in data + pseudocount (ess). 
"""

def cfgs(vrs,valcs):
    return product(*imap(xrange, valcs(vrs)))

def itembetter(ixs):
    return lambda xs: tuple(xs[i] for i in ixs)

def count(valcs, ds, vrs, e, ess):
    (evrs,evls) = ((),()) if len(e)==0 else zip(*e)
    ecfg = itembetter(evrs)
    vcfg = itembetter(vrs)

    freqs = dict((cfg,ess) for cfg in cfgs(vrs,valcs))
    for d in ifilter(lambda row: evls == ecfg(row), imap(tuple,ds.dats())):
            freqs[vcfg(d)] += 1
    return freqs

def distrib(valcs, ds, ess, vrs, e):
    dstr = map(count(valcs,ds,vrs,e,ess).get, cfgs(vrs,valcs))
    nzer = sum(dstr)
    return (int(nzer-len(dstr)*ess), [p/nzer for p in imap(float,dstr)])
