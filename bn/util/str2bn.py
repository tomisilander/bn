#!/usr/bin/env python3
import bn
import typer

def str2bn(strfile: str, bnfile: str):
    strf = open(strfile)
    varc = int(strf.readline())
    
    arcs = []
    for i,l in enumerate(strf):
        arcs.extend([(p,i) for p in map(int, l.split()[2:])])

    bn.bn.BN(varc, arcs, do_pic=False).save(bnfile)

if __name__ == "__main__":
    typer.run(str2bn)
