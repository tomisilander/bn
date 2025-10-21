#!/usr/bin/env python
import src.learn.score as score
from ctypes import c_double, c_int, c_void_p, POINTER
from functools import lru_cache

class PenMLScore(score.Score):
    def __init__(self, data, scoref,
                 do_cache=True, do_storage=True, cachefile=None):
        self.scoref = scoref
        self.scoref.restype = c_double
        self.scoref.argtypes = [c_void_p, c_int, c_int, POINTER(c_int)]

        score.Score.__init__(self,data,do_cache, do_storage, cachefile)

    @lru_cache(maxsize=2**16)
    def score_v_ps(self, v, parentset):
        c_nof_parents, c_parents = score.cparents(parentset)    
        return self.scoref(self.data.dt,
                           v, c_nof_parents, c_parents)

    def score_ss_var(self, bn, v):
        ps = bn.parents(v)
        return float(self.score_v_ps(v, ps))
