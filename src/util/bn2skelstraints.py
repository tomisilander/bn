#!/usr/bin/env python3

"""Forbid all the arcs that are not in skeleton of the given BN."""

from src.bn import load as load_bn
from src.learn.constraints import Constraints

from itertools import combinations
import typer

app = typer.Typer()

def gen_forbidden_arcs(bn):

    sarcs = frozenset(tuple(arc) for arc in map(sorted, bn.arcs()))

    for arc in combinations(bn.vars(), 2):
        if arc not in sarcs: 
            yield arc
            yield tuple(reversed(arc))

@app.command()
def skelstraints(bnfile, cstrfile):
    bn = load_bn(bnfile)
    cstrs = Constraints()
    for arc in gen_forbidden_arcs(bn):
        cstrs.no.add(arc)
    cstrs.save(cstrfile)

if __name__ == "__main__":
    app()
