#!/usr/bin/env python3
import typer
from array import array

from . import disdat

app = typer.Typer()

def tdt2bdt(vdfile, tdtfile, bdtf, verbose=False):
    
    cdt = disdat.ColData(vdfile, tdtfile)
        
    array("I",[cdt.N()]).tofile(bdtf)
    for vci, di in zip(cdt.nof_vals(), cdt.vars()):
        if verbose: 
            print('.', end='')
        array("B",[vci]).tofile(bdtf)
        array("b",list(di)).tofile(bdtf)

    if verbose: 
        print()

@app.command("tdt2bdt")
def main(
    vdfile: str = typer.Argument(..., help='VD file'),
    tdtfile: str = typer.Argument(..., help='TDT file'),
    bdtfile: str = typer.Argument(..., help='BDT file'),
    verbose: bool = typer.Option(False, "-v", "--verbose", help='Verbose mode')
):
    tdt2bdt(vdfile, tdtfile, bdtfile, verbose)

if __name__ == "__main__":
    app()