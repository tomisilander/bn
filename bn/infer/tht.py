#!/usr/bin/python

import utils

def normalize(xs):
    return map((1/sum(xs)).__mul__, xs)

def thti(dpi):
    d = dict([(pcfg, normalize(dp))
              for pcfg, dp in dpi.dict.iteritems()])
    return utils.sparse_func(d, normalize(dpi.default))

def tht(dps):
    for dpi in dps:
        yield thti(dpi)
