#!/usr/bin/env python
from ctypes import *
import cache

class Score :
    def __init__(self, bn, data, ess):
        self.ess = ess
        self.data = data
        vars = bn.vars()

        self.cache   = [cache.Cache(None,100000/len(vars)) for v in  vars]
        self.clearcache()
        
        self.clearstore()

        self.libcscore = cdll.LoadLibrary("/home/tsilande/projects/bn/learn_ctypes/cscore.so")
        self.bde_score = self.libcscore.bde_score
        self.bde_score.restype = c_double
        self.bde_score.argtypes = [c_void_p, c_double, c_int, c_int, c_void_p]

        self.vscores = [self.score_ss_var(bn, v) for v in  vars]

    def storevar(self,v): 
        self.storage.append((v, self.vscores[v]))

    def restore(self) :
        for (v, vscore) in self.storage :
            self.vscores[v] = vscore
        self.clearstore()
        
    def clearstore(self):
        self.storage = []

    def clearcache_v(self, v):
        self.cache[v].clear()

    def clearcache(self):
        map(cache.Cache.clear, self.cache)
        self.cachehits = 0
        self.cachetrys = 0
        
    def score_ss_var(self, bn, v):        
        parentset = bn.parents(v)
        nof_parents = len(parentset)
        parentarray = c_int * nof_parents
        parents = parentarray(*parentset)
        res = self.bde_score(self.data, self.ess, v, nof_parents, parents)
        return res

    def score(self) : return sum(self.vscores)

    def score_new_v(self, bn, v) :
        vps = bn.parents(v)
        if vps in self.cache[v]:
            vscore = self.cache[v][vps]
            self.cachehits += 1
        else :
            ss_score = self.score_ss_var(bn, v)
            vscore = self.cache[v][vps] = ss_score
        self.cachetrys += 1
        self.vscores[v] = vscore

        # if self.cachetrys % 10000 == 1:
        # print "Cache hit ratio:", 1.0 * self.cachehits / self.cachetrys
        
    def score_new(self,bn):
        for v in bn.vars():
            self.score_new_v(bn, v)

