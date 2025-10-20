#!/usr/bin/env python
import cache

class Score :
    def __init__(self, bn, data, ess):
        self.ess = ess
        self.data = data
        vars = bn.vars()

        self.cache   = [cache.Cache(None,100000/len(vars)) for v in  vars]
        self.clearcache()
        
        self.clearstore()
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
        parentsv = bn.parents(v)
        vcv = self.data.nof_vals()[v]
        
        def cfgetter(d):
            return tuple(d[v] + [d[i] for i in parentsv])
        
        cfreqs = {}
        for cfg in imap(cfgetter, self.data.dats()):
            if -1 in cfg: continue

            if not cfg in cfreqs:
                cfreqs[cfg] = [0]*vcv
            cfreqs[cfg][cfg[0]] += 1 

        ml = 0
        rgt = 0
        
        for cfreq in cfreqs.values():
            nj = sum(cfreq)
            lml += (f*log(float(f)/nj) for f in cfreq)
            lrgt += math.log(reg(nj, vcv))

        return ml - rgt
        
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

q
