#!/usr/bin/python

import utils

def dpi(ssi, e):
    d = dict((pcfg, map(e.__add__, freqs))
              for pcfg, freqs in ssi.dict.iteritems())
    return utils.sparse_func(d, map(e.__add__, ssi.default))
    
def dpa(sss, ess, bn, valcs):
    for i, ssi in enumerate(sss):
        e = ess / utils.pcfgc(i,bn,valcs) / valcs(i)
        yield dpi(ssi, e)
