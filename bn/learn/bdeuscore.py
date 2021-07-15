#!/usr/bin/env python
from ctypes import *
import score

class BDeuScore(score.Score):
    def __init__(self, data, ess, 
                 do_cache=True, do_storage=True, cachefile=None):

        self.scoref = score.libcscore.bde_score
        self.scoref.restype = c_double
        self.scoref.argtypes = [c_void_p, c_double, c_int, c_int, POINTER(c_int)]
        self.cess = c_double(ess)

        score.Score.__init__(self,data, do_cache, do_storage, cachefile)

    def score_ss_var(self, bn, v):
        nof_parents, parents = score.cparents(bn,v)    
        return self.scoref(self.data.dt, self.cess,
                           v, nof_parents, parents)
