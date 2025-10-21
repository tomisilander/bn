#!/usr/bin/env python
import random
import heapq
from typing import List

import typer

import sigpool

from src import bn as bnmodule
from src.learn.constraints import Constraints
import src.learn.bnsearch as bnsearch
import src.learn.scorefactory as scorefactory
import src.learn.bestforests as bestforests
import src.learn.greedysearch as greedysearch
#import cycheck

app = typer.Typer()

def wheelselect(lst):
    scores, items = zip(*lst)
    w = random.uniform(0.0, sum(scores))
    s = 0
    i = 0
    for i, scr in enumerate(scores):
        s += scr
        if s > w: 
            break
    return i, scores[i], items[i]



@app.command("stocgreedy")
def main(bdtfile: str,
         score_type: str = 'BDeu',
         ess: float = 1.0,
         time: str|None = None,
         iters: int|None = None,
         outfile: str|None = None,
         constraint_file: str = "",
         startbn: str|None = None,
         cachefile: str|None = None):
 
    # set up signal handling for termination
    sigpool.watch('SIGUSR2')
    sigpool.watch('SIGUSR1')

    if time:
        sigpool.wait_n_raise(sigpool.str2time(time), 'SIGUSR2')

    cstrs = Constraints(constraint_file)

    # set up initial bn and scorer
    
    if startbn is not None:
        bn = bnmodule.load(startbn,do_pic=False)
        sc = scorefactory.getscorer(bdtfile, score_type, ess,
                                    cachefile=cachefile)
        forests_left = False
        fry = None
    else: # start from forests
        bn, sc = bnsearch.empty_net_n_score(bdtfile, score_type, ess, 
                                            cachefile=cachefile)
        bestforests.kruskal(bn,sc,cstrs)
        fry = bestforests.Forest(bn)
        forests_left = True
        bn = fry.next()
    
    if constraint_file: # should check if compatible with start
        for a in cstrs.must:
            bn.addarc(a)

    sc.score_new(bn)
    bn.picall()
    
    
    # start doing stochastic greedy search
    good_nets:List = [(sc.score(),bn.copy())]
    t = 0
    while True:

        greedysearch.greedysearch(bn, sc, 1000, cstrs)
        gs = sc.score()

        t += 1

        # store good nets found so far
        MAX_KEEP = 10

        # add worthy candidate if not already present
        already_in_goods = any(gn == bn for (_, gn) in good_nets)
        worth_adding = gs >= good_nets[0][0]
        if worth_adding and not already_in_goods:
            if len(good_nets) >= MAX_KEEP:
                good_nets.pop(0) # remove worst
            good_nets.append((gs, bn.copy()))
            good_nets.sort(key=lambda score_n_bn: score_n_bn[0]) # best last
           
        # prepare for next iteration       
        start_from_forest = random.choice((0,1)) # stupid if out of forests
        if forests_left and start_from_forest: 
            try:
                assert fry is not None
                bn = fry.next()
                bn.picall()
            except StopIteration:
                forests_left = False
                
        if (not start_from_forest) or (not forests_left):
              
            bn = random.choice(good_nets)[1].copy()
            
            sc.score_new(bn)

            sas = bnsearch.score_arcs(bn,sc)
            sas.reverse()
            eas = list(enumerate(sas))
            for x in range(len(sas) // 2) :
                i, n, sa = wheelselect(eas)
                ii, (s,a) = eas.pop(i)
                if a not in cstrs.must:
                    #print 'DEL', a
                    bn.delarc(a)
                    #print 'ADEL', bn.arcs()
                    #for v in bn.vars(): print v, bn.path_in_counts[v]          

        sc.score_new(bn)

        # check for termination
        
        if (iters and t > iters): 
            break
        if 'SIGUSR2' in sigpool.flags: 
            break
        if 'SIGUSR1' in sigpool.flags:
            if outfile: 
                good_nets[-1][1].save(outfile)
            print (good_nets[-1][0])
            sigpool.flags.remove('SIGUSR1')

    # save best net found
    if outfile:
        good_nets[-1][1].save(outfile)

    # print score of best net found 
    print (good_nets[-1][0])

if __name__ == '__main__':
    app()