#!/usr/bin/python

from itertools import izip
import pot, utils

def vpot(v, bn, thtv, valcs):

    ps  = utils.ops(v,bn)
    fam = ps + [v]
    fam.sort()

    vp = pot.Potential(fam, valcs)
    vix = fam.index(v)

    for fcfg in utils.cfgs(valcs(fam)):
        cfg = list(fcfg)
        vl = cfg.pop(vix)
        cfg = tuple(cfg)
        vp[fcfg] = thtv(tuple(cfg))[vl]

    return vp

def init(bn, tht, valcs, clqs, vclqixs):
    pots = [pot.Potential(clq, valcs) for clq in clqs]
    for v, (clqix, thtv) in enumerate(izip(vclqixs, tht)):
        clq = clqs[clqix]
        pots[clqix] *= vpot(v, bn, thtv, valcs)

    return pots
