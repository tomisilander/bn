#!/usr/bin/env python3

from bn.bn import load as load_bn
from bn.learn.constraints import Constraints

import coliche
from itertools import combinations
import typer
from typing import Optional

def gen_forbidden_arcs(bn):

    sarcs = frozenset(tuple(arc) for arc in map(sorted, bn.arcs()))

    for arc in combinations(bn.vars(), 2):
        if not arc in sarcs: 
            yield arc
            yield tuple(reversed(arc))

def main(bnfile, cstrfile, opt: Optional[str] = None):
    bn = load_bn(bnfile)
    cstrs = Constraints()
    for arc in gen_forbidden_arcs(bn):
        cstrs.no.add(arc)
    cstrs.save(cstrfile)

if __name__ == "__main__":
    typer.run(main)
