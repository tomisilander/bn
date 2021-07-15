#!/usr/bin/env python
import elo

def in_any(clq0, clqs):
    for clq in clqs :
        if clq0.issubset(clq):
            return True
    return False

def triangulate(mg, valcs, eord):
    """
    Triangulate mg by sequantially extracting cliques from its copy
    tmpg and adding those clique-edges to the mg. 
    """
    
    clx = []
    tmpg    = mg.copy()
    
    for e in eord:

        clq, xedges = elo.clq_n_xedges(tmpg, e)        
        clqe = frozenset(clq)
        if not in_any(clqe, clx): # add only "new" cliques
            clx.append(clqe)

        # add extra edges to mg and tmpg and delete n from tmpg
        mg.addedges(xedges)
        tmpg.addedges(xedges)        
        tmpg.delnode(clq[0]) 

    return clx #NB! mg gets triangulated

def clx_load(clqfile):
    return [map(int, l.split()) for l in file(clqfile)]

def clx_save(clqlst, clqfile):
    clqf = file(clqfile,"w")
    for clq in clqlst:
        print >>clqf, " ".join(map(str,clq))
    clqf.close()
