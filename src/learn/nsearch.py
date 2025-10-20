# nsearch takes an initial network and tries to find 
# top N best networks around it at most depth steps away.

from itertools import combinations, product
from heapq import heappushpop, heappush
from bn.learn.bnsearch import can_addarc
from bn.learn.constraints import Constraints
from bn.learn.scorefactory import getscorer
from bn.learn.score import Score
from bn.bn import BN, load as load_bn
from bn.learn.data import Data


def tryseq(bn0:BN ,sc:Score, opseq):
 
    if len(set(a for (op,a) in opseq)) < len(opseq):
        return False # illegal sequence since same arc acted on many times

    bnw = bn0.copy()

    needs_scoring=set()
    for (op,a) in opseq:
        (f,t) = a
        if t not in needs_scoring: 
            sc.storevar(t)
            needs_scoring.add(t)

        if op == 'd':
            bnw.delarc(a)
        else: # op == 'a':
            if can_addarc(bnw,a):
                bnw.addarc(a)
            else:
                sc.restore()
                return False

    for v in needs_scoring:
        sc.score_new_v(bnw,v)
        
    s = sc.score()
    sc.restore()

    return (s, bnw)
    

# TODO ADD TABU LISTING TO N-SEARCH

def nsearch(bn0: BN, sc:Score, cstrs, depth, topN, elite, elitnets): # consider obeying stop-signal

    # should add hash to bn
    
    """Try a sequence of at most depth deletion and addition operations of arcs 
    keeping topN best results"""
        
    # initialize possible operations
    dops = [('d',a) for a in bn0.arcs() if a not in cstrs.must]
    aops = [('a', a) for a in product(bn0.vars(),bn0.vars())
            if (a not in bn0.arcs()) and a[0]!=a[1] and a not in cstrs.no]
    ops = dops + aops
    

    cannots = {}
    for depth in range(1,depth+1):
        cannots[depth]=set()
        for opseq in combinations(ops, depth):

            can = True  
            # check for illegal prefix
            for pl in range(1, depth): 
                if opseq[:pl] in cannots[pl]:
                    can = False
                    break
            if not can: 
                continue

            # get new BN and its score  and update heap          
            res = tryseq(bn0, sc, opseq)
            score, bn = res
            if res:
                bn_id = hash(bn) 
                el = (score, bn_id)
                if len(elite) >= topN:
                    smallest_score = elite[0][0]
                    if score > smallest_score: # need to replace smallest score
                        _s, _weak_id = heappushpop(elite, el)            
                        del elitnets[_weak_id]
                        elitnets[bn_id] = bn
                else:
                    heappush(elite, el)            
                    elitnets[bn_id] = bn
            else:
                cannots[depth].add(opseq)
                
    elite.sort(reverse=True)

    return elite, elitnets


def iter_elites(bn0:BN, sc:Score, cstrs:Constraints, depth: int, topN: int, iters:int, timestr:str):
    """runs  a topN wide beam search of local searches using neighbourhood of "depth" additions/deletions"""

    # initialise topN heap
    sc.score_new(bn0)
    elite = [(sc.score(), hash(bn0))]
    elitnets = {hash(bn0):bn0}

    iter = 0    
    while True: # add time limit here
        if iter is not None and iter >= iters:
            break 

        old_elite, old_elitnets = elite[:], elitnets.copy()
        for (sc, key) in old_elite:
            bn = old_elitnets[key]
            elite, elitenets = nsearch(bn, sc, cstrs, depth, topN, elite, elitnets)

        iter += 1

        
    return elite, elitenets

if __name__ == '__main__':
    import pathlib

    def main(args):

        bdata = Data(args.bdtfile)

        bn0 = load_bn(args.startbn) if args.startbn else BN(bdata.nof_vars())
        sc = getscorer(bdata, args.score_type, args.ess, cachefile=args.cachefile)
        cstrs = Constraints(args.constraint_file)

        resdirpath = pathlib.Path(args.outfile)
        resdirpath.mkdir(parents=True, exist_ok=True)

        elite, nets = iter_elites(bn0, sc, cstrs, args.depth, args.topN, args.iters, timestr=args.time)
        
        for (i,(s,bnid)) in enumerate(elite):
            nets[bnid].save(resdirpath/f'{i}.bn')
            print(s)
            # print s, seq
    
    from argparse import ArgumentParser
    from bn.learn.args import add_learning_args

    parser = ArgumentParser(description='Network Search')
    add_learning_args(parser, exceptions=[])
    parser.add_argument('--depth', type=int, default=3, help='depth of search (default: 3)')
    parser.add_argument('--topN', type=int, default=3, help='beam search width (default: 10)')
    args = parser.parse_args()
    
    main(args)