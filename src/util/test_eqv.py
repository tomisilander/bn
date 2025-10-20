#!/usr/bin/env python3
import typer
from src.bn import load as load_bn
from eqvnets import skeleton
app = typer.Typer()

@app.command()
def test_eqv(bnfile1: str, bnfile2: str):
    is_eqv(bnfile1, bnfile2)

def is_eqv(bnfile1:str, bnfile2:str):
    bns1 = load_bn(bnfile1)
    bns2 = load_bn(bnfile2)
    fix1, free1 = skeleton(bns1)
    fix2, free2 = skeleton(bns2)

    # print map(frozenset,free1)
    samefree = frozenset(map(frozenset, free1)) == frozenset(map(frozenset, free2))
    print (int(fix1 == fix2 and samefree))
    return

if __name__ == "__main__":
    app()
