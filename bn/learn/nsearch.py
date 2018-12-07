# nsearch takes an initial network and tries to find 
# top N best networks around it at most level steps away.

from itertools import izip, combinations, product
from heapq import heappushpop, heappush
from bnsearch import can_addarc
from constraints import Constraints
import scorefactory, data, bn
import sys

def tryseq(bn0,sc,opseq):
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
    return (s, (bnw, opseq))
    

# def nsearch_basic(bn0,sc,level,topN): 
# # consider obeying stop-signal, constraints
#     dops = [('d',a) for a in bn0.arcs()]
#     aops = [('a', a) for a in product(bn0.vars(),bn0.vars())
#             if (a not in dops) and a[0]!=a[1]]    
#     ops = dops+aops
#     elite = [(sc.score(),bn0)]*topN
#     for l in xrange(1,level+1):
#         for opseq in combinations(ops,l):
#             res = tryseq(bn0,sc,opseq)
#             if res != False:
#                 weakest = heappushpop(elite,res)

#     elite.sort(reverse=True)
#     return elite


# Try to make a smarter version that excludes not working prefixes

def nsearch(bn0,sc,level,topN,cstrs): # consider obeying stop-signal
    dops = [('d',a) for a in bn0.arcs() if a not in cstrs.must]
    aops = [('a', a) for a in product(bn0.vars(),bn0.vars())
            if (a not in bn0.arcs()) and a[0]!=a[1] and a not in cstrs.no]
    ops = dops + aops
    # print ops
    
    sc.score_new(bn0)
    if topN > 0:
        elite = [(-sys.float_info.max, (None,None))]*(topN-1) \
            + [(sc.score(),(bn0,[]))]
    else:
        elite = [(sc.score(),(bn0,[]))]

    cannots = {}
    for l in xrange(1,level+1):
        cannots[l]=set()
        for opseq in combinations(ops,l):

            can = True  

            # check for illegal prefix
            for pl in xrange(1,l): 
                if opseq[:pl] in cannots[pl]:
                    can = False
                    break
            if not can: continue

            res = tryseq(bn0,sc,opseq)
            if res != False:
                if topN > 0:
                    _weakest = heappushpop(elite,res)
                else:
                    heappush(elite,res)
            else:
                cannots[l].add(opseq)
    elite.sort(reverse=True)
    return elite

def get_elite(bnfile,bdtfile,level,topN,resdir,
              scoretype='BDeu', ess=1.0, constraint_file="", cachefile=None):

    cstrs = Constraints(constraint_file)
    bn0 = bn.bn.load(bnfile)
    sc = scorefactory.getscorer(data.Data(bdtfile), scoretype, ess, 
                                cachefile=cachefile)
    return nsearch(bn0,sc,level,topN, cstrs)

if __name__ == '__main__':
    import coliche, os

    def main(bnfile,bdtfile,level,topN,resdir, 
             scoretype='BDeu', ess=1.0, constraint_file="",
             cachefile=None):
        if not os.path.exists(resdir): os.mkdir(resdir)

        elite = get_elite(bnfile,bdtfile,level,topN,resdir,
                          scoretype, ess, constraint_file, cachefile)
        
        for (i,(s,(bnw,seq))) in enumerate(elite):
            if bnw != None: 
                bnw.save(os.path.join(resdir,'%d.bn'%i))
                print s
            # print s, seq

    coliche.che(main, 
                """bnfile; bdtfile; level (int); topN (int); resdir
                -g --goodness scoretype BDeu|fNML|AIC|BIC : default: BDeu
                -e --ess ess (float) : default 1.0
                -c constraint_file : a file with arcs marked with + or -
                -m --cachefile cachefile: local scores
                """)
