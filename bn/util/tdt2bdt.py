#!/usr/bin/python

from array import array
from itertools import izip
import coliche, disdat

def tdt2bdt(vdfile, tdtfile, bdtfile, v=False):
    
    cdt = disdat.ColData(vdfile, tdtfile)

    bdtf = file(bdtfile,"w")

    di1 = cdt.vars()
    length = len(di1[0])
    array("I",[length]).tofile(bdtf)
    
    di2 = cdt.vars()
    for i,vci in enumerate(cdt.nof_vals()):
        if v: print ".",
        array("B",[vci]).tofile(bdtf)
        array("b",di2[i]).tofile(bdtf)

    bdtf.close()

    if v: print ""
    
if __name__ == '__main__' :
    coliche.che(tdt2bdt,
                """
                vdfile; tdtfile; bdtfile
                -v (bool): verbose""")
