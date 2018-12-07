#!/usr/bin/python

import os, copy
import pot

class Inferer:
    
    def __init__(self, valcs, jt, clqs, pots, vclqs):

        # CONSTANTS 

        self.valcs = valcs
        self.jt    = jt
        self.clqs  = clqs
        self.vclqs = vclqs
        self.nof_vars = len(vclqs)

        # AND WORK VARIABLES
        
        self.pots_  = pots
        self.spots_ = self.sepot(jt, clqs, valcs)
        self.lhs_   = [pot.Potential([v], valcs) for v in xrange(self.nof_vars)]

        self.reset()


    def reset(self):
        self.pots  = map(pot.cpy, self.pots_)
        self.spots = dict([(k,pt.cpy())
                           for (k,pt) in self.spots_.iteritems()])
        self.lhs   = map(pot.cpy, self.lhs_)
        
        self.insts = []


    def infer1(self,v, needs_propagation=True):
        if needs_propagation:
            self.globprop(self.jt, self.pots, self.spots)
        cpot = self.pots[self.vclqs[v]]
        return (cpot >> pot.Potential([v], self.valcs, 0.0)).normalize().p
        
    def infer(self):
        self.globprop(self.jt, self.pots, self.spots)
        return [self.infer1(v, False) for v in xrange(self.nof_vars)]

    def insert_evidence(self, v, dstr):
        
        if isinstance(dstr, int):
            val = dstr
            dstr = [0.0]*self.valcs(v)
            dstr[val] = 1.0

        old_lhv     = self.lhs[v]
        new_lhv     = pot.Potential(old_lhv.vars, old_lhv.valcs)
        new_lhv.p   = dstr[:]
        self.lhs[v] = new_lhv

        vpot        = self.pots[self.vclqs[v]]
        vpot       *= new_lhv / old_lhv


    
    def globprop(self, jt, cpots, spots):
    
        def pass_message(x, y):
            sepix = min(x,y), max(x,y)
            r_old = spots[sepix]
            spots[sepix] = cpots[x] >> r_old
            cpots[y] *= spots[sepix] / r_old
        
        def collect_evidence(c, x):
        
            marked[x] = True
        
            for xn in jt.neighbours(x):
                if not marked[xn]:
                    collect_evidence(x,xn)

            if c != None:
                pass_message(x, c)


        def distribute_evidence(x):

            marked[x] = True

            for xn in jt.neighbours(x):
                if not marked[xn]:
                    pass_message(x, xn)

            for xn in jt.neighbours(x):
                if not marked[xn]:
                    distribute_evidence(xn)


        nof_nodes = len(list(jt.nodes()))
        marked = [False]*nof_nodes
        collect_evidence(None, 0)
        marked = [False]*nof_nodes
        distribute_evidence(0)


    def sepot(self, jt, clqs, valcs):
        spots = {}
        for (x,y) in jt.edges():
            svars = list(set(clqs[x]) & set(clqs[y]))
            svars.sort()
            spots[(x,y)] = pot.Potential(svars, valcs)
        return spots


import inout

def save(ifr, ifrdir):

    if not os.path.exists(ifrdir):
        os.mkdir(ifrdir)

    needed, haved = set(),{}
    
    for n, o in zip('vd clx jtr vcx pot'.split(),
                    (ifr.valcs, ifr.clqs, ifr.jt, ifr.vclqs, ifr.pots_)):
        needed.add(n+"save")
        haved[n+"_o"] = o
        haved['new_'+n+'file'] = os.path.join(ifrdir, n)
    
    inout.inout(needed, haved)

def load(ifrdir):

    needed, haved = set(),{}
    ns = 'vd jtr clx pot vcx'.split()
    for n in ns:
        needed.add(n + "_o")
        haved[n + "file"] = os.path.join(ifrdir, n)
        
    inout.inout(needed, haved)

    return Inferer(*map(haved.get, [n+'_o' for n in ns]))
