#!/usr/bin/python

from data import Data
from constraints import Constraints
import random
import bnsearch
import coliche
import sigpool
#import cycheck
from bn import bn as bnmodule
import data
import scorefactory
import bestforests
import greedysearch


def wheelselect(lst):
    scores, items = zip(*lst)
    w = random.uniform(0.0, sum(scores))
    s = 0
    for i, scr in enumerate(scores):
        s += scr
        if s > w: break
    return i, scores[i], items[i]



def main(bdtfile, scoretype='BDeu',
         ess=1.0, time=None, iters=None,
         outfile=None, constraint_file="", startbn=None, cachefile=None):

    sigpool.watch('SIGUSR2')
    sigpool.watch('SIGUSR1')

    if time:
        sigpool.wait_n_raise(sigpool.str2time(time), 'SIGUSR2')

    cstrs = Constraints(constraint_file)

    if startbn != None:
        bn = bnmodule.load(startbn,do_pic=False)
        sc = scorefactory.getscorer(bdtfile,scoretype,ess,
                                    cachefile=cachefile)
        forests_left = False
    else:
        bn, sc = bnsearch.empty_net(bdtfile, scoretype, ess, 
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
    
    good_nets = [(sc.score(),bn.copy())]
    
    t = 0L
    while True:

        greedysearch.greedysearch(bn, sc, 1000, cstrs)
        gs = sc.score()

        t += 1

        if gs > good_nets[0][0] and bn not in [gn for (sn,gn) in good_nets]:
            good_nets.append((gs,bn.copy()))
            good_nets.sort()
            if len(good_nets) > 2 * 10 :
                good_nets = good_nets[10:]
            
        start_from_forest = random.choice((0,1)) # stupid if out of forests

        if forests_left and start_from_forest: 
            try:
                bn = fry.next()
                bn.picall()
            except StopIteration:
                forests_left = False
                
        if (not start_from_forest) or (not forests_left):
              
            bn = random.choice(good_nets)[1].copy()

            # bn = good_nets[0][1].copy()
            
            sc.score_new(bn)

            sas = bnsearch.score_arcs(bn,sc)
            sas.reverse()
            eas = list(enumerate(sas))
            for x in xrange(len(sas) / 2) :
                i, n, sa = wheelselect(eas)
                ii, (s,a) = eas.pop(i)
                if not a in cstrs.must:
                    #print 'DEL', a
                    bn.delarc(a)
                    #print 'ADEL', bn.arcs()
                    #for v in bn.vars(): print v, bn.path_in_counts[v]          

        sc.score_new(bn)

        if (iters and t > iters): break
        if 'SIGUSR2' in sigpool.flags: break
        if 'SIGUSR1' in sigpool.flags:
            if outfile: good_nets[-1][1].save(outfile)
            print good_nets[-1][0]
            sigpool.flags.remove('SIGUSR1')

    if outfile:
        good_nets[-1][1].save(outfile)

    print good_nets[-1][0]


coliche.che(main,
            ''' bdtfile;
                -g --goodness scoretype BDeu|fNML|AIC|BIC : default: BDeu
                -e --ess ess (float) : default 1.0
                -t time : like -t '4d 3h 5m 5[s]' (default till SIGUSR2)
                -i --iters iters (int) :number of iterations (default infinite)
                -c constraint_file : a file with arcs marked with + or -
                -o outfile : file to save the model found
                -s --start startbn : file to start search from
                -m --cachefile cachefile: local scores
                ''')
