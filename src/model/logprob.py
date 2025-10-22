#!/usr/bin/env python

import math

import typer 

from src.data.disdat import RowData 
from src.model.bnmodel import load as bnmload
from src.vd import load as vdload

app = typer.Typer()

def gen_logprobs(bnm, tstdat, base=None):

    lbase = 1 if base is None else math.log(base)
    for d in tstdat.dats():
        yield bnm.logprob_d(d) / lbase

def logprob(bnm, tstdat, base=None):
    lp = bnm.logprob_D(tstdat)
    if base: 
        lp /= math.log(base)
    return lp

@app.command("logprob")
def main(modelfile: str,
         vdfile: str,
         tstfile: str,
         density: bool = False,
         base: float | None = None,
         avg: bool = False,
         verbose: bool = False):
    
    valdes = vdload(vdfile)
    bnm = bnmload(modelfile, valdes)
    if density:
        bnm.use_density = True
    tstdat = RowData(vdfile, tstfile)
    if verbose:
        for lp in gen_logprobs(bnm,tstdat, base):
            print(lp)
    else:
        lp =  logprob(bnm, tstdat, base)
        print(lp/tstdat.N() if avg else lp)


if __name__ == '__main__':
    app()    