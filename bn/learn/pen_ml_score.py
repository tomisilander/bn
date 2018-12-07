#!/usr/bin/python

import score

class PenMLScore(score.Score):
    def __init__(self, data, scoref,
                 do_cache=True, do_storage=True, cachefile=None):
        self.scoref = scoref
        score.Score.__init__(self,data,do_cache, do_storage, cachefile)

    def score_ss_var(self, bn, v):
        nof_parents, parents = score.cparents(bn,v)    
        return self.scoref(self.data.dt, v, nof_parents, parents)
