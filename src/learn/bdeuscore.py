#!/usr/bin/env python
from ctypes import c_double, c_void_p, c_int, POINTER
from functools import lru_cache

import src.learn.score as score

class BDeuScore(score.Score):
    def __init__(self, data, ess, 
                 do_cache=True, do_storage=True, cachefile=None):

        self.scoref = score.libcscore.bde_score
        self.scoref.restype = c_double
        self.scoref.argtypes = [c_void_p, c_double, c_int, c_int, POINTER(c_int)]
        self.cess = c_double(ess)

        score.Score.__init__(self,data, do_cache, do_storage, cachefile)

    @lru_cache(maxsize=2**16)
    def score_v_ps(self, v, parentset):
        c_nof_parents, c_parents = score.cparents(parentset)    
        s = self.scoref(self.data.dt, self.cess,
                           v, c_nof_parents, c_parents)
        return float(s)

    def score_ss_var(self, bn, v):
        ps = bn.parents(v)
        return float(self.score_v_ps(v, ps))
