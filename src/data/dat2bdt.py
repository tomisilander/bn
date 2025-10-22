#!/usr/bin/env python3
import os
import typer

from .transpose_file import transpose
from .tdt2bdt import tdt2bdt

app = typer.Typer()

def dat2bdt(vdfile:str, idtfile:str, bdtf:str, delim:str|None=None, verbose=False):
    """Convert a data file in DAT format to BDT format
       by first transposing it to TDT format and then converting to BDT format.

    Args:
        idtfile (str): Path to the input DAT file.
        bdtf (str): Path to the output BDT file.
        delim (str, optional): Delimiter used in the DAT file. Defaults to None (whitespace).
        verbose (bool, optional): If True, print verbose output. Defaults to False.

    """
    tdtfile = bdtf + ".tdt"    
    transpose(idtfile, tdtfile, delim=delim)
    tdt2bdt(vdfile, tdtfile, bdtf, verbose)
    os.remove(tdtfile)       

@app.command("dat2bdt")
def main(
    vdfile: str = typer.Argument(..., help='VD file'),
    idtfile: str = typer.Argument(..., help='IDT file'),
    bdtfile: str = typer.Argument(..., help='BDT file'),
    delim: str = typer.Option(None, "--delim", help='IDT delimiter'),
    verbose: bool = typer.Option(False, "-v", "--verbose", help='Verbose mode')
):
    dat2bdt(vdfile, idtfile, bdtfile, delim, verbose)

if __name__ == "__main__":
    app()