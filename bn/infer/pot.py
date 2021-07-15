#!/usr/bin/env python
import operator
from itertools import imap, izip
import utils, copy


class Potential:

    def __init__(self, vars, valcs, ival = 1.0):
        self.vars  = list(vars)
        self.vars.sort()
        self.vcs   = valcs(self.vars)
        self.valcs = valcs
        
        # print 'V', self.vars

        self.nof_cfgs = reduce(operator.__mul__, self.vcs, 1)
        self.p = [ival] * self.nof_cfgs
        self.ix = utils.cfg2ixer(self.vcs)


    # CONTAINER METHODS
    
    def __getitem__(self, cfg):
        return self.p[self.ix(cfg)]

    def __setitem__(self, cfg, val):
        self.p[self.ix(cfg)] = val

    def __len__(self):
        return self.nof_cfgs

    def __iter__(self):
        return iter(self.p)


    # NUMERIC METHODS
    

    def __mul__(self, o):
        uvars = list(set(self.vars + o.vars))
        uvars.sort()
        u = Potential(uvars, valcs)
        u *= self
        u *= o

        return u

    def __imul__(self, o):
        six, sp = self.ix, self.p
        opos = map(self.vars.index, o.vars)
        for cfg in utils.cfgs(self.vcs):
            ocfg = map(cfg.__getitem__, opos)
            sp[six(cfg)] *= o[ocfg]
        return self

    def __div__(self, o):
        r = Potential(self.vars, self.valcs)
        r.p = [y and x/y or 0.0 for (x,y) in izip(self, o)]
        return r

    def __rshift__(self, o):

        opos = map(self.vars.index, o.vars)
        ovcs = self.valcs(o.vars)
        
        r   = Potential(o.vars, o.valcs, 0.0)
        rp  = r.p
        rix = r.ix

        for cfg, p in izip(utils.cfgs(self.vcs), self):
            rcfg = imap(cfg.__getitem__, opos)
            rp[rix(rcfg)] += p

        return r


    # AND SOME EXTRA

    def normalize(self):
        self.p = map((1.0/sum(self.p)).__mul__, self.p)
        return self
    
    def save(self, potf):
        print >>potf, len(self)
        print >>potf, "\n".join(map(str, self))


    def cpy(self):
        n = copy.copy(self)
        n.p = n.p[:]
        return n
    
def load(potfile, clqs, valcs):
    potf = file(potfile)
    pots = []
    for clq in clqs:
        ptl = Potential(clq, valcs)

        if len(ptl) != int(potf.readline()):
            raise "Incompatible potential for clique!"

        for x in xrange(len(ptl)):
            ptl.p[x] = float(potf.readline())

        pots.append(ptl)
    return pots

def save(pots, potfile):
    potf  = file(potfile,"w")
    for pot in pots:
        pot.save(potf)
    potf.close()


def cpy(pt):
    return pt.cpy()

# turn CPD to potential
def vpot(v, bn, thtv, valcs):

    fam = list(bn.parents(v)) + [v]
    fam.sort()

    vp = Potential(fam, valcs)
    vix = fam.index(v)

    for fcfg in utils.cfgs(valcs(fam)):
        cfg = list(fcfg)
        vl = cfg.pop(vix)
        vp[fcfg] = thtv(tuple(cfg))[vl] 
        # IIKS - thtv may return float if v has 1 value

    return vp


# multiply thetas to their corresponding potentials

def get_pots(bn, tht, valcs, clqs, vclqixs):
    pots = [Potential(clq, valcs) for clq in clqs]
    for v, (clqix, thtv) in enumerate(izip(vclqixs, tht)):
        pots[clqix] *= vpot(v, bn, thtv, valcs)

    return pots
