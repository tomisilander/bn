#!/usr/bin/env python3

import typer
from src.bn import load as load_bn
app = typer.Typer()

@app.command()
def markovblanket(bnfile: str, v: int, bnout: str):
    bns = load_bn(bnfile, do_pic=False)
    mb = bns.markovblanket(v, do_pic=False)
    mb.save(bnout)

if __name__ == "__main__":
    app()
