#!/usr/bin/env python3
import sys, os
import typer
from typing import Optional

import disdat, bn.vd
from itertools import izip, chain, product

def main(vdfile, outvdfile, constraintfile,
         datafile: Optional[str] = None, outdatafile: Optional[str] = None, nof_levels: int = 2, no_within: bool = False):

    # create format

    f  = bn.vd.load(vdfile)    
    varnames = tuple(vn+'_%d'%l for l in range(nof_levels)
                     for vn in f.varnames)
    values   = f.values * nof_levels
    bn.vd.save(bn.vd.vd(varnames, values), outvdfile)

    # create constraints
    cstrf = open(constraintfile,'w')
    nof_vars = len(f.varnames)
    for l_to in range(nof_levels):
        fromstart = l_to if no_within else l_to+1
            
        for l_from in range(fromstart, nof_levels):
            for (x,y) in product(range(nof_vars), range(nof_vars)):
                print('-', x+l_from*nof_vars, y+l_to*nof_vars, file=cstrf)
    cstrf.close()

    # create data
    
    if datafile is not None and outdatafile is not None:
        dat = disdat.RowData(vdfile, datafile)
        ds = [dat.dats() for l in range(nof_levels)]
        for l in range(nof_levels): # skip initial l from ds[l]
            for ll in range(l): next(ds[l])

        datf = open(outdatafile,'w')
        for drows in izip(*ds):
            print('\t'.join(map(str, chain(*drows))), file=datf)
        datf.close()
    
if __name__ == "__main__":
    typer.run(main)
