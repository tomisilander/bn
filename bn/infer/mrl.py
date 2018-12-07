#!/usr/bin/python

import udg
from itertools import product
"""
Go through variables and add edges between their parents.
"""

def moralize(bnt):
    mg = udg.Udg(bnt.vars(), bnt.arcs())
    
    for v in bnt.vars():
        vps = list(bnt.parents(v))
        mg.addedges(pp for pp in product(vps,vps) if pp[0]<pp[1] )
    return mg
