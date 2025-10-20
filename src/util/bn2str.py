#!/usr/bin/env python3
import typer

from src.bn import load

app = typer.Typer()

@app.command()
def bn2str(bnfile: str, strfile: str):
    """Which format is this?"""
    bns = load(bnfile)
    strf = open(strfile,"w")

    print(bns.varc, file=strf)
    
    for v in bns.vars():
        ps = sorted(bns.parents(v))
        print (len(bns.children(v)), len(ps), " ".join(map(str,ps)), file=strf)
    strf.close()

if __name__ == "__main__":
    app()
