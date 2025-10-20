#!/usr/bin/env python3
import typer
from src.bn import BN

app = typer.Typer()

@app.command("str2bn")
def main(strfile: str, bnfile: str):
    str2bn(strfile, bnfile)

def str2bn(strfile: str, bnfile: str):
    strf = open(strfile)
    varc = int(strf.readline())
    
    arcs = []
    for i,line in enumerate(strf):
        arcs.extend([(p,i) for p in map(int, line.split()[2:])])

    BN(varc, arcs, do_pic=False).save(bnfile)

if __name__ == "__main__":
    app()
