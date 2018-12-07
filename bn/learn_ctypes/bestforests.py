#!/usr/bin/python

from bn import BN
from score import Score
# from sets import Set
import operator

def kruskal(bn, scr) :
    arcscores = {}
    for v1 in bn.vars() :
        for v2 in xrange(v1) :
            arc = (v1,v2)
            bn.addarc(arc, False)
            arcscores[arc] = scr.score_ss_var(bn, v2)
            bn.delarc(arc, False)

    ordarcs = [(s,a) for (a,s) in arcscores.items()]
    ordarcs.sort()
    ordarcs.reverse()
    
    ########################################################

    (v1,v2) = ordarcs.pop(0)[1]
    treevars = set([v1,v2])
    treearcs = set()
    treearcs.add((v1,v2))
    six = 0
    while len(treevars) < bn.varc :
        for i in xrange(six, len(ordarcs)):
            s, arc = ordarcs[i]
            (v1,v2) = arc 
            v_a = -1
            if v1 in treevars:
                if v2 in treevars:
                    del ordarcs[i]
                    six = i
                    break
                else:
                    v_a = v2
                    a_a = (v1, v2)
            else:
                if v2 in treevars:
                    v_a = v1
                    a_a = (v2, v1)
                
            if v_a >= 0:
                treevars.add(v_a)
                treearcs.add(a_a)
                del ordarcs[i]
                six = 0
                break

    for tarc in treearcs:
        (v1, v2) = tarc
        bn.addarc(tarc)
        scr.score_new_v(bn,v2)

def prune_1(bn, score):
    for arc in bn.arcs():
        (v1,v2) = arc
        old_v2_score = score.vscores[v2]
        score.storevar(v2)
        bn.delarc(arc, False)
        score.score_new_v(bn,v2)
        new_v2_score = score.vscores[v2]
        if(new_v2_score >= old_v2_score):
            score.clearstore()
            bn.pic_del(arc)
        else:
            bn.addarc(arc, False)
            score.restore()


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

def reroot_tree(bn, r, newps = set()) :
    nps = set(newps)
    nps.add(r)
    for rpr in bn.parents(r):
        if rpr not in newps:
            bn.revarc((rpr,r))
            reroot_tree(bn, rpr, nps)

    for rpr in bn.children(r):
        reroot_tree(bn, rpr, nps)

def reroot_forest(bn, comps, counter):
    for comp, c in zip(comps, counter):
        reroot_tree(bn, comp[c])


def count_in_radices(radices):        

    def nums(d):
        for radix in radices:
            d, r = divmod(d, radix)
            yield r
                
    for n in xrange(reduce(operator.__mul__, radices, 1)):
        yield list(nums(n))
        
def forests(init_forest_bn):
    forest = init_forest_bn.copy()
    comps  = conncomps(forest)
    for counter in count_in_radices(map(len, comps)):
        forest = forest.copy()
        reroot_forest(forest, comps, counter)
        yield forest

if __name__ == '__main__':
    for n in count_in_radices((2,3,4)):
        print n
