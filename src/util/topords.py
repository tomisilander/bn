#!/usr/bin/env python3
import typer

from itertools import product
from src.bn import load

app = typer.Typer()

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

@app.command("topords")
def main(bnfile: str = typer.Argument(..., help="The Bayesian network file.")):
    topords(bnfile)

if __name__ == "__main__":
    app()

