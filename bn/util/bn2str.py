#!/usr/bin/env python3
import sys, os
import typer
from typing import Optional

import bn

def main(bnfile: str, strfile: str, opt: Optional[str] = None):
    bns = bn.load(bnfile)
    strf = file(strfile,"w")

    print >>strf, bns.varc
    
    for v in bns.vars():
        ps = sorted(bns.parents(v))
        print >>strf, len(bns.children(v)), len(ps), " ".join(map(str,ps))
    strf.close()

if __name__ == "__main__":
    typer.run(main)
