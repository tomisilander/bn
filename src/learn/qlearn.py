#!/usr/bin/env python
from data import Data
from src.bn import BN
from score import Score
from heapq import *
import itertools
import bnsearch, greedysearch

    
def get_2_best_arcs(net, allarcs, taboo, scr, init_score):

    def score_new_arcs():
        for a in allarcs - net.arcs() - taboo - net.cyclarcs():
            (v1,v2) = a
            scr.storevar(v2)
            net.addarc(a, False)
            scr.score_new_v(net,v2)
            yield (scr.score(), a)
            net.delarc(a, False)
            scr.restore()

    scored_new_arcs = list(score_new_arcs())
    
    badarcs = set(a for (s,a) in scored_new_arcs if s < init_score) # maybe too strict
    s1_a1   = scored_new_arcs and max(scored_new_arcs) or (None, None)
    if scored_new_arcs: scored_new_arcs.remove(s1_a1)
    s2_a2   = scored_new_arcs and max(scored_new_arcs) or (None, None)

    return s1_a1, s2_a2, badarcs


def qlearn(data, ess, max_heap_size, min_heap_size, max_iters):

    # INITIAL QUEUE ELEMENT
    
    qe = {'net': BN(data.nof_vars()), 'taboo' : set(), 'nof_arcs' : 0}
    qe['score'] = Score(qe['net'], data, ess).score()
    
    hq = [(0, qe)]

    best_score = qe['score']
    best_net   = qe['net'].copy(False)
    plty = abs(best_score) / 1000 # HACK
    scr = Score(best_net, data, ess)
    vars = best_net.vars()
    allarcs = set([(v1,v2) for v1 in vars for v2 in vars if v1!=v2])

    for t in itertools.count():

        if t == max_iters: break
        if not hq: break
        
        pri, qe = heappop(hq)
        net, taboo, score, nof_arcs = map(qe.__getitem__,
                                          'net taboo score nof_arcs'.split())

        to_be_inserted = []

        oldscr = scr
        scr = Score(net, data, ess)
        scr.cache = oldscr.cache
            
        while True: # greedily add arcs creating a twin task each round

            # find the greediest arc addition
            
            (s1,a1), (s2,a2), badarcs = get_2_best_arcs(net, allarcs, taboo, scr, score)

            if (not a1) or s1 <= score : break
            
            # create a twin task like current, but taboo extended

            qe_twn = {'net'   : net.copy(False),
                      'taboo' : taboo | set((a1,)) | badarcs,
                      'score' : score,
                      'nof_arcs'  : nof_arcs}

            # taking the greedy step
            
            net.addarc(a1)
            scr.score_new_v(net,a1[1])
            score = s1
            nof_arcs += 1
            
            if score > best_score:
                best_score = score
                best_net   = net.copy()
            
            # no need to continue since no more additions possible

            if not a2: break 
            
            # store aside a twin task
            
            qe_twn['delta'] = s1 - s2
            to_be_inserted.append(qe_twn)

        # Now when we are at the bottom, let us try to improve by greedy
        #score = greedysearch.greedysearch(net,
        #                                  scr,
        #                                  bnsearch.acts,
        #                                  greedysearch.stuck_for_t_test(None,100))
        
        if score > best_score:
            best_score = score
            best_net   = net.copy()
            # print t, best_score, best_net.arcs()

        # insert twin tasks to the heap
        
        for qe_tbi in to_be_inserted:
            pri = -score +qe_tbi['delta'] + plty * qe_tbi['nof_arcs']            
            heappush(hq, (pri, qe_tbi))

        if max_heap_size > 0 and len(hq) > max_heap_size :
            print "truncating hq"
            hq = hq[:min_heap_size+1]
            
    print t, best_score, best_net.arcs()

def main(bdtfile, ess=1.0,
         max_heap_size = 5000, min_heap_size = 4000,
         max_iters = -1):
    data  = Data(bdtfile)
    qlearn(data, ess, max_heap_size, min_heap_size, max_iters)
    

if __name__ == '__main__':
    import coliche
    coliche.che(main,
                """
                bdtfile : data in bdt-format
                -e --ess ess (float) : ESS (default 1.0)
                --max_heap_size max_heap_size (int) : give negative for infinite (default 5000)
                --min_heap_size min_heap_size (int) : (default 4000)
                --max_iters max_iters (int) : give negative for infinite (default -1)
                """)
