#!/usr/bin/env python
from bn.bn import BN
from  UnionFind import UnionFind
import operator
from itertools import *

# For decomposable scores one can use undirected MST algorithms
# like Kruskal

def kruskal(bn, scr, cstrs) :
    # get weighted edges - do not include negative ones
    
    ordarcs = []
    for v2 in bn.vars():
        sv2 = scr.score_ss_var(bn, v2)
        for v1 in xrange(v2+1,bn.varc) :
            arc = (v1,v2)
            if arc not in cstrs.no:
                bn.addarc(arc, False)
                sarc = scr.score_ss_var(bn, v2) - sv2
                if sarc > 0: ordarcs.append((sarc,arc))
                bn.delarc(arc, False)
    ordarcs.sort()
    ordarcs.reverse()
    
    ########################################################
    # Kruskal

    subtrees = UnionFind()
    treearcs = set()

    for (w,arc) in ordarcs:
        (v1,v2) = arc
        if subtrees[v1] != subtrees[v2]:
            treearcs.add(arc)
            subtrees.union(v1,v2)

    # make a bn out of it
    for tarc in treearcs:
        bn.addarc(tarc)

    # orient away from roots:
    roots = [subtrees[x] for x in bn.vars()]
    for r in roots:
        orient_away(bn,r)

def orient_away(bn, r, newp=None):
    for p in bn.parents(r):  # turn parents to children
        if p != newp:        # not the sole new one
            bn.revarc((p,r),do_pic=False)

    for c in bn.children(r): # orient away from children but not me
        orient_away(bn,c,r)
    

def newclosure(bn,v,old):
    newpcs = set(bn.parents(v) | bn.children(v)) - old
    old.add(v)
    return reduce(set.union, [newclosure(bn,nv,old) for nv in newpcs],set())

def conncomps(bn):
    notfoundset = set(bn.vars())
    comps = []
    while notfoundset:
        comp = set()
        newclosure(bn,notfoundset.pop(),comp)
        comps.append(comp)
        notfoundset.difference_update(comp)
    return map(list,comps)

def reroot_forest(bn, comps, counter):
    for comp, c in zip(comps, counter):
        orient_away(bn, comp[c])


class Forest:
    def __init__(self, bn):
        self.bn0 = bn.copy()
        self.comps = conncomps(bn)
        self.radices = map(len, self.comps)
        self.nof_forests = reduce(operator.__mul__, self.radices, 1)
        self.i = 0
            
    def ith_forest(self, i):
        ibn = self.bn0.copy()
        reroot_forest(ibn, self.comps, list(self.nums(i)))
        return ibn

    # how about going in order that minimizes changes to previous
    def next(self): # next() is the heart of any iterator
        if self.i == self.nof_forests: raise StopIteration
        nbn = self.ith_forest(self.i)
        self.i += 1
        return nbn

    # HOWABOUT permuting nums so that forests are searched in very
    # random order
    
    def nums(self,d):
        for radix in self.radices:
            d, r = divmod(d, radix)
            yield r
            
    def __iter__(self):
        return self

class Polyforest:
    def __init__(self, bn):
        self.arcs0 = list(bn.arcs())
        self.nof_forests = 2**len(arcs)
        self.i = 0
            
    def ith_forest(self, i):
        arcs = self.arcs0.copy()
        for i,b in enumerate(bin(i)[2:]):
            if b=='0':
                arcs[i][0],arcs[i][1]=arcs[i][1],arcs[i][0]
        return BN(arcs)
    
    # use grey code for quick iteration
    # http://icodesnip.com/snippet/python/gray-code-generatoriterator

    def next(self): # next() is the heart of any iterator
        if self.i == self.nof_forests: raise StopIteration
        nbn = self.ith_forest(self.i)
        self.i += 1
        return nbn

    def __iter__(self):
        return self


if __name__ == '__main__':
    import coliche
    import bnsearch
    import constraints
    def main(bdtfile, scoretype='BDeu', ess = 1.0, 
             outfile=None, constraint_file="", cachefile=None):
        bn,sc = bnsearch.empty_net(bdtfile, scoretype, ess, cachefile=cachefile)
        cstrs = constraints.Constraints(constraint_file)
        kruskal(bn,sc, cstrs)
        if outfile:
            bn.save(outfile)
        sc.score_new(bn)
        print sc.score()

    coliche.che(main,
                ''' bdtfile;
                -g --goodness scoretype BDeu|fNML|AIC|BIC : default: BDeu
                -e --ess ess (float) : default 1.0
                -c constraint_file : a file with arcs marked with (+) or -
                -o outfile : file to save the model found
                -m --cachefile cachefile: local scores
                ''')
