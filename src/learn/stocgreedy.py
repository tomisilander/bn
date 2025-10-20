#!/usr/bin/env python
import random
import sigpool

from bn import bn as bnmodule
from bn.learn.constraints import Constraints
import bn.learn.bnsearch as bnsearch
import bn.learn.scorefactory as scorefactory
import bn.learn.bestforests as bestforests
import bn.learn.greedysearch as greedysearch
#import cycheck


def wheelselect(lst):
    scores, items = zip(*lst)
    w = random.uniform(0.0, sum(scores))
    s = 0
    for i, scr in enumerate(scores):
        s += scr
        if s > w: 
            break
    return i, scores[i], items[i]



# def main(bdtfile, scoretype='BDeu',
#          ess=1.0, time=None, iters=None,
#          outfile=None, constraint_file="", startbn=None, cachefile=None):

def main(args):
    sigpool.watch('SIGUSR2')
    sigpool.watch('SIGUSR1')

    if args.time:
        sigpool.wait_n_raise(sigpool.str2time(args.time), 'SIGUSR2')

    cstrs = Constraints(args.constraint_file)

    if args.startbn is not None:
        bn = bnmodule.load(args.startbn,do_pic=False)
        sc = scorefactory.getscorer(args.bdtfile, args.score_type, args.ess,
                                    cachefile=args.cachefile)
        forests_left = False
    else:
        bn, sc = bnsearch.empty_net(args.bdtfile, args.score_type, args.ess, 
                                    cachefile=args.cachefile)
        bestforests.kruskal(bn,sc,cstrs)
        fry = bestforests.Forest(bn)
        forests_left = True
        bn = fry.next()
    
    if args.constraint_file: # should check if compatible with start
        for a in cstrs.must:
            bn.addarc(a)

    sc.score_new(bn)
    bn.picall()
    
    good_nets = [(sc.score(),bn.copy())]
    
    t = 0
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
            for x in range(len(sas) // 2) :
                i, n, sa = wheelselect(eas)
                ii, (s,a) = eas.pop(i)
                if a not in cstrs.must:
                    #print 'DEL', a
                    bn.delarc(a)
                    #print 'ADEL', bn.arcs()
                    #for v in bn.vars(): print v, bn.path_in_counts[v]          

        sc.score_new(bn)

        if (args.iters and t > args.iters): 
            break
        if 'SIGUSR2' in sigpool.flags: 
            break
        if 'SIGUSR1' in sigpool.flags:
            if args.outfile: 
                good_nets[-1][1].save(args.outfile)
            print (good_nets[-1][0])
            sigpool.flags.remove('SIGUSR1')

    if args.outfile:
        good_nets[-1][1].save(args.outfile)

    print (good_nets[-1][0])

if __name__ == '__main__':
    from argparse import ArgumentParser
    from bn.learn.args import add_learning_args 

    parser = ArgumentParser()
    add_learning_args(parser, [])    
    main(parser.parse_args())
