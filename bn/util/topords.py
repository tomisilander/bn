#!/usr/bin/env python3

from itertools import product
from bn.bn import load
import typer

def get_stages(bnfile:str):
    bn=load(bnfile)
    stages=[]
    varsleft=set(bn.vars())
    while len(varsleft)>0:
        sources = set(v for v in varsleft if len(bn.parents(v))==0)
        stages.append(sorted(sources))

        varsleft -= sources
        for v in sources:
            for c in bn.children(v):
                bn.delarc((v,c))
    
    return stages

def gen_topords(bnfile:str):
    stages = get_stages(bnfile)
    for ord in product(*[sorted(s) for s in stages]):
        yield ord

def topords(bnfile:str):
    for ord in gen_topords(bnfile):
        print(" ".join(map(str, ord)))

if __name__ == "__main__":
    typer.run(topords)

