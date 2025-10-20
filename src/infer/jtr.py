#!/usr/bin/env python
import heapq
import udg, elo

""" Builds a tree of clique(indice)s """

def jtr(clqs, valcs):

    # sort sepsets (cliquepairs) largest first (smallest weight)
    w = [elo.weight(clq, valcs) for clq in clqs]
    clqpairs = [((-len(clq1&clq2), w[i]+w[j]), (i, j))
                for (i,clq1) in enumerate(clqs)
                for (j,clq2) in enumerate(clqs)
                if i<j]
    heapq.heapify(clqpairs)

    # from now on cliques are identified by their indices
    nof_clqs = len(clqs)    
    # one of these qlique trees will be returned
    jtrs = [udg.Udg([i]) for i in xrange(nof_clqs)] 

    ti = jtrs[0]
    while ti.nof_edges() != nof_clqs - 1:
        (i,j) = heapq.heappop(clqpairs)[1] # cliques
        ti, tj = jtrs[i], jtrs[j]   # and their trees        

        if ti != tj:

            # join udg tj to udg ti
            ti.join_with(tj, (i,j))
            
            # mark cliques of tj to be now in ti
            for clqj in tj.nodes():
                jtrs[clqj] = ti

    # return if ready
    return ti
