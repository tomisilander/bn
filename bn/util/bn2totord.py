#!/usr/bin/env python
from bn.bn import load
from collections import defaultdict

def gen_totord(bn_org):
    bn = bn_org.copy()

    d  = defaultdict(list)
    for v in bn.vars():
        d[bn.nof_parents(v)].append(v)
    
    while len(d[0])>0:
        v = d[0].pop(0)
        yield v
        for c in bn.children(v):
            d[bn.nof_parents(c)].remove(c)
            bn.delarc((v,c), do_pic=False)
            d[bn.nof_parents(c)].append(c)
            
def main(bnfile):
    bn = load(bnfile)
    print(" ".join(map(str, gen_totord(bn))))

import coliche
coliche.che(main,'bnfile')
