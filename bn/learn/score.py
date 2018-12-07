#!/usr/bin/python

from ctypes import *
import os
from itertools import imap

import cache

libcscore = CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "cscore.so"))

cscorefuncs =  {
    'BIC' : libcscore.bic_score,
    'AIC' : libcscore.aic_score,
    'fNML': libcscore.fnml_score,
    'BDeu': libcscore.bde_score
    }

def cparents(bn, v):
    parentset = bn.parents(v)
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

        if do_cache:
            if cachefile != None:
                dicts = [{} for v in xrange(data.nof_vars())]
                for l in open(cachefile):
                    t = l.split()
                    v,s = t[:2]
                    dicts[int(v)][frozenset(imap(int,t[2:]))]=float(s)
                self.cache   = [cache.Cache(dicts[v],len(dicts[v])) 
                                for v in  vars]
                self.cachehits = 0
                self.cachetrys = 0
            else:
                self.cache   = [cache.Cache(None,100000/len(vars)) 
                                for v in  vars]
                self.clearcache()

        if do_storage: self.clearstore()

        self.vscores = [None]*len(vars)

    def storevar(self,v):
        self.storage.append((v, self.vscores[v]))

    def restore(self) :
        for (v, vscore) in self.storage : #how about going in reversed order
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

