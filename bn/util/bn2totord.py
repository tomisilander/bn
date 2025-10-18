#!/usr/bin/env python3
from bn.bn import load
from collections import defaultdict
import sys, os
import typer
from typing import Optional

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
            
def main(bnfile: str, opt: Optional[str] = None):
    bn = load(bnfile)
    print(" ".join(map(str, gen_totord(bn))))

if __name__ == "__main__":
    typer.run(main)
