#!/usr/bin/env python
import operator
from itertools import imap, izip, product

def prod(xs):
    return reduce(operator.__mul__, xs, 1)

def weight(vs, valcs):
     return prod(valcs(vs))

def clq_n_xedges(g, v): # Find clique for v
    vclq = [v] + list(g.neighbours(v))
    cedges = set(nn for nn in product(vclq,vclq) if nn[0] < nn[1])
    xedges = cedges - set(g.edges())
    return vclq, xedges

def find_min_cost_n(tmpg, valcs):

    # recalculation needed actually only for neighbours of neighbours of
    # minimal element

    def vscore(v):
        vclq, xedges = clq_n_xedges(tmpg, v)
        return (len(xedges), weight(vclq, valcs), vclq, xedges)

    return min(imap(vscore, tmpg.nodes()))


def elo(mg, valcs):

    """
    Triangulate mg by sequantially extracting cliques from its copy
    tmpg and adding those clique-edges to the mg. 
    The order of the sequence is determined by the number of
    edges needed to form a clique and the weight of the clique (number
    of configurations of the variables in the clique.
    """
    
    tmpg    = mg.copy()
    eo = []
    
    while tmpg.nof_nodes()>0:

        # Find minimum clique and its center variable clq[0]

        (s1, w, clq, xedges) = find_min_cost_n(tmpg, valcs)

        # add extra edges to mg and tmpg and delete n from tmpg

        mg.addedges(xedges)
        tmpg.addedges(xedges)
        
        eo.append(clq[0])
        tmpg.delnode(clq[0]) 

    return eo #NB! mg has changed

def load(elofile):
    return map(int, file(elofile))

def save(elo, elofile):
    elof = file(elofile,"w")
    print >>elof, "\n".join(map(str, elo))
    elof.close()
