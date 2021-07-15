#!/usr/bin/env python
# from data import Data
from score import Score
from constraints import Constraints
import vd
import random
import bnsearch
import coliche
import sigpool, signal

from bn import BN

def wheelselect(lst):
    scores, items = zip(*lst)
    w = random.uniform(0.0, sum(scores))
    s = 0
    for i, scr in enumerate(scores):
        s += scr
        if s > w: break
    return i, scores[i], items[i]



def main(bdtfile, 
         ess=1.0, time=None, iters=None, outfile=None, constraint_file=""):

    sigpool.raise_on_signal(signal.SIGUSR2)

    if time:
        sigpool.wait_n_raise(sigpool.str2time(time), signal.SIGUSR2)

    bn, sc = bnsearch.empty_net(bdtfile, ess)
    
    if constraint_file:
        cstrs = Constraints(constraint_file)
        forests_left = False
        for a in cstrs.must:
            bn.addarc(a)
    else:
        cstrs = Constraints()
        bestforests.kruskal(bn,sc)
        bestforests.prune_1(bn,sc)
        fry = bestforests.forests(bn)
        forests_left = True

        bn = fry.next()

    sc.score_new(bn)
    
    good_nets = [(sc.score(),bn.copy())]
    
    t = 0L
    while True:

        greedysearch.greedysearch(bn, sc, 1000, cstrs)
        gs = sc.score()

        t += 1
        
        if gs > good_nets[0][0] and bn not in [gn for (sn,gn) in good_nets]:
            good_nets.append((gs,bn.copy(False)))
            good_nets.sort()
            if len(good_nets) > 2 * 10 :
                good_nets = good_nets[10:]
            
        start_from_forest = random.choice((0,1)) # stupid if out of forests

        if forests_left and start_from_forest: 
            try:
                bn = fry.next()
            except StopIteration:
                forests_left = False
                
        if (not start_from_forest) or (not forests_left):
              
            bn = random.choice(good_nets)[1].copy(False)
            # bn = good_nets[0][1].copy()
            
            sc.score_new(bn)

            arcs = bnsearch.score_arcs(bn,sc)
            arcs.reverse()
            eas = list(enumerate(arcs))
            for x in xrange(len(arcs) / 2) :
                i, n, sa = wheelselect(eas)
                ii, (s,a) = eas.pop(i)
                if not a in cstrs.must: bn.delarc(a)

        sc.score_new(bn)

        if (iters and t > iters): break
        if signal.SIGUSR2 in sigpool.flags: break

    if outfile:
        good_nets[-1][1].save(outfile)

    print good_nets[-1][0]


if __name__ == '__main__':
    import sys
    import bestforests

    import greedysearch
    
    coliche.che(main,
                ''' bdtfile;
                -e --ess ess (float) : default 1.0
                -t time : like -t '4d 3h 5m 5[s]' (default till SIGUSR2)
                -i --iters iters (int) :number of iterations (default infinite)
                -c constraint_file : a file with arcs marked with + or -
                -o outfile : file to save the model found
                ''')
