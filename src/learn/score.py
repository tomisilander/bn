#!/usr/bin/env python
from ctypes import CDLL, c_int, c_double
import os

# import bn.learn.cache as cache

libcscore = CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "cscore.so"))

cscorefuncs =  {
    'BIC' : libcscore.bic_score,
    'AIC' : libcscore.aic_score,
    'fNML': libcscore.fnml_score,
    'BDeu': libcscore.bde_score
    }

def cparents(parentset):
    nof_parents = len(parentset)
    Parents = c_int * nof_parents
    parents = Parents(*sorted(parentset))
    return nof_parents, parents


# Use of cache should be better controlled !!!

class Score :
    def __init__(self, data, 
                 do_cache=True, do_storage=True, cachefile=None):

        self.scoref.restype = c_double
        self.data = data
        vars = range(data.nof_vars())
 
        if do_storage: 
            self.clearstore()

        self.vscores = [None]*len(vars)

    def storevar(self,v):
        self.storage.append((v, self.vscores[v]))

    def restore(self) :
        for (v, vscore) in self.storage : #how about going in reversed order
            self.vscores[v] = vscore
        self.clearstore()

    def clearstore(self):
        self.storage = []

    def score(self) : 
        return sum(self.vscores)            
            
    def score_new_v(self, bn, v) :
        ss_score = self.score_ss_var(bn, v)
        self.vscores[v] = ss_score

        # if self.cachetrys % 10000 == 1:
        # print "Cache hit ratio:", 1.0 * self.cachehits / self.cachetrys

    def score_new(self, bn):
        for v in bn.vars():
            self.score_new_v(bn, v)

