#!/usr/bin/python

# NOT READY YET - INFER 1 VARIABLE GIVEN THE REST (MARKOV BLANKET)

import os, utils
import bn, tht, vd, clx, vcx, pot, udg

class Inferer1:
    
    def __init__(self, valcs, bn, tht, var):

        # CONSTANTS 
        self.bn = bn
        self.vvals = range(valcs(var))
        self.varfam = bn.children(var).union((var,))
        self.pcfget = dict((v, itemgetter(utils.ops(v,bn)))
                           for v in self.varfam)
        # AND WORK VARIABLES
        
        self.reset()

    def infer(self):
        dstr = utils.normalize([1.0] * len(self.vvals))
        for v in self.varfam:
            pcfg = self.pcfget[v](self.inst)
            for val in self.vvals:
                dstr[val] *= self.tht[v](pcfg)[val]
            dstr = utils.normalize(dstr)
        return dstr


    def insert_evidence(self, vars, vals):
        
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


import inout

def save(ifr, ifrdir):

    if not os.path.exists(ifrdir):
        os.mkdir(ifrdir)

    needed, haved = [],{}
    
    for n, o in zip('vd clx jtr vcx pot'.split(),
                    (ifr.valcs, ifr.clqs, ifr.jt, ifr.vclqs, ifr.pots_)):
        needed.append(n+"save")
        haved[n+"_o"] = o
        haved['new_'+n+'file'] = os.path.join(ifrdir, n)
    
    inout.inout(needed, haved)

def load(ifrdir):

    needed, haved = [],{}
    ns = 'vd jtr clx pot vcx'.split()
    for n in ns:
        needed.append(n + "_o")
        haved[n + "file"] = os.path.join(ifrdir, n)
        
    inout.inout(needed, haved)

    return Inferer(*map(haved.get, [n+'_o' for n in ns]))
