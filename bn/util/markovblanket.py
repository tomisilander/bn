#!/usr/bin/env python3
import typer
import bn

def main(bnfile: str, v: int, bnout: str):
    bns = bn.load(bnfile, do_pic=False)
    mb = bns.markovblanket(v, do_pic=False)
    mb.save(bnout)

if __name__ == "__main__":
    typer.run(main)
