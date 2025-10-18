#!/usr/bin/env python3
import bn
import typer
from eqvnets import skeleton

def is_eqv(bnfile1:str, bnfile2:str):
    bns1 = bn.bn.load(bnfile1)
    bns2 = bn.bn.load(bnfile2)
    fix1, free1 = skeleton(bns1)
    fix2, free2 = skeleton(bns2)

    # print map(frozenset,free1)
    samefree = frozenset(map(frozenset, free1)) == frozenset(map(frozenset, free2))
    print (int(fix1 == fix2 and samefree))
    return

if __name__ == "__main__":
    typer.run(is_eqv)
