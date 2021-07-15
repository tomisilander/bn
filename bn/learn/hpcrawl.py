#!/usr/bin/env python
# hpcrawl tries to go through new high probability networks

from heapq import heappop, heapify, heappush
from constraints import Constraints
import scorefactory, data, bn
from bn import bn as bnmodule
from nsearch import nsearch

def hpcrawl(bn0s, sc, cstrs=None,
            topN=0, dump_worklist=False):

    if cstrs==None: cstrs = Constraints('')

    varc = bn0s[0].varc
    worklist=[]
    workset = set()
    for bn0 in bn0s: 
        sc.score_new(bn0)
        bn0as=bn0.arcs()
        worklist.append((-sc.score(),bn0as))
        workset.add(bn0as)
    heapify(worklist)

    doneset = set()
    c = 0
    while True:
        if len (workset)==0: break
        if topN>0 and c==topN: break

        (hpsc, hpbnas) = heappop(worklist)
        workset.remove(hpbnas)
        if hpbnas in doneset: continue

        doneset.add(hpbnas)
        yield (hpbnas, -hpsc)
        c += 1

        for (s,(nbr,seq)) in nsearch(bnmodule.BN(varc,hpbnas),sc,1,0,cstrs):
            nbras= nbr.arcs()
            if nbras not in doneset and nbras not in workset:
                heappush(worklist,(-s,nbras))
                workset.add(nbras)
        if dump_worklist and (c+len(workset))>=topN: break

    if dump_worklist:
        while c<topN and len(worklist)>0:
            (hpsc, hpbnas) = heappop(worklist)
            workset.remove(hpbnas)
            if hpbnas in doneset: continue
            doneset.add(hpbnas)
            yield (hpbnas, -hpsc)
            c += 1

import coliche, os

def main(bnfile,bdtfile,
         scoretype='BDeu', ess=1.0, constraint_file="",
         cachefile=None, topN=0, dump_worklist=False):

    cstrs = Constraints(constraint_file)
    bn0 = bnmodule.load(bnfile)
    sc = scorefactory.getscorer(data.Data(bdtfile), scoretype, ess, 
                                cachefile=cachefile)
    c=0
    for (_bnas,s) in hpcrawl([bn0],sc, cstrs=cstrs,topN=topN, 
                             dump_worklist=dump_worklist):
        print c, s
        # if c == 20000: 
        #     bnmodule.BN(bn0.varc,_bnas,do_pic=False).save('X%d.bn' % c)
        c+=1

coliche.che(main, 
            """bnfile; bdtfile; 
                -g --goodness scoretype BDeu|fNML|AIC|BIC : default: BDeu
                -e --ess ess (float) : default 1.0
                -c constraint_file : a file with arcs marked with + or -
                -m --cachefile cachefile: local scores
                -d --dump_worklist (bool): default: False
                -t --top topN (int): default: 0 - all
                """)
