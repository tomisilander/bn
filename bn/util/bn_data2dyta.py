#!/usr/bin/python
import disdat, bn.vd
from itertools import izip, chain, product

def main(vdfile, outvdfile, constraintfile,
         datafile=None, outdatafile=None, nof_levels=2, no_within=False):

    # create format

    f  = bn.vd.load(vdfile)    
    varnames = tuple(vn+'_%d'%l for l in xrange(nof_levels)
                     for vn in f.varnames)
    values   = f.values * nof_levels
    bn.vd.save(bn.vd.vd(varnames, values), outvdfile)

    # create constraints
    cstrf = file(constraintfile,'w')
    nof_vars = len(f.varnames)
    for l_to in xrange(nof_levels):
        fromstart = l_to if no_within else l_to+1
            
        for l_from in xrange(fromstart, nof_levels):
            for (x,y) in product(xrange(nof_vars), xrange(nof_vars)):
                print >>cstrf, '-', x+l_from*nof_vars, y+l_to*nof_vars
    cstrf.close()

    # create data
    
    if datafile != None and outdatafile != None:
        dat = disdat.RowData(vdfile, datafile)
        ds = [dat.dats() for l in xrange(nof_levels)]
        for l in xrange(nof_levels): # skip initial l from ds[l]
            for ll in xrange(l): ds[l].next()

        datf = file(outdatafile,'w')
        for drows in izip(*ds):
            print >>datf, '\t'.join(map(str, chain(*drows)))
        datf.close()
    
if __name__ == '__main__':
    import coliche

    coliche.che(main,
                """vdfile; outvdfile; constraintfile
                -d datafile: datafile
                -o outdatafile: outdatafile
                -l --levels nof_levels (int) : default:2
                --no_within     : disallow arcs within timestep
""")
