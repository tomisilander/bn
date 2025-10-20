#!/usr/bin/env python3
import typer

from bn import vd
from bn import disdat
from itertools import chain, product

app = typer.Typer()

@app.command("todyta")
def main(vdfile: str, outvdfile: str, constraintfile: str,
         datafile: str | None = None, outdatafile: str | None = None, 
         nof_levels: int = 2, 
         no_within: bool = False):

    """I do not know what this fnction does"""

    # create format

    valdes  = vd.load(vdfile)    
    varnames = tuple(vn+'_%d'%line for line in range(nof_levels)
                     for vn in valdes.varnames)
    values   = valdes.values * nof_levels
    vd.save(vd.VariableDescriptors(varnames, values), outvdfile)

    # create constraints
    cstrf = open(constraintfile,'w')
    nof_vars = len(valdes.varnames)
    for l_to in range(nof_levels):
        fromstart = l_to if no_within else l_to+1
            
        for l_from in range(fromstart, nof_levels):
            for (x,y) in product(range(nof_vars), range(nof_vars)):
                print('-', x+l_from*nof_vars, y+l_to*nof_vars, file=cstrf)
    cstrf.close()

    # create data
    
    if datafile is not None and outdatafile is not None:
        dat = disdat.RowData(vdfile, datafile)
        ds = [dat.dats() for _ in range(nof_levels)]
        for level in range(nof_levels): # skip initial l from ds[l]
            for ll in range(level): 
                next(ds[level])

        datf = open(outdatafile,'w')
        for drows in zip(*ds):
            print('\t'.join(map(str, chain(*drows))), file=datf)
        datf.close()
    
if __name__ == "__main__":
    app()
