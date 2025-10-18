#!/usr/bin/env python3
import os
import sys
from pathlib import Path  
import typer
import bn
from bn.bn import load as bnload
from bn.learn.constraints import Constraints
from eqvorient import Orient

def vstructs(bns):
    vstr = set()
    arcs = bns.arcs()
    for v in bns.vars():
        for p1 in bns.parents(v):
            for p2 in bns.parents(v):
                if p1<p2:
                    if (p1,p2) not in arcs and (p2,p1) not in arcs:
                        vstr.add((v,p1,p2))
    return vstr

def skeleton(bns):
    # Find vstructures
    vstr = vstructs(bns)

    # divide arcs to fixed and free
    fix  = set()
    free = bns.arcset.copy()    
    for (v,p1,p2) in vstr:
        a1 = (p1,v)
        a2 = (p2,v)
        fix.add(a1)
        fix.add(a2)
        if a1 in free: free.remove(a1)
        if a2 in free: free.remove(a2)

    return (fix, free)


def gen_eqvnets_with_arc(varc,fix,free,arc):
    # print 'bo', fix, free
    fix  = fix  | set([arc])
    # print "fixing", arc
    o = Orient(varc,fix,free)
    # print 'ao', o.fix, o.free
    for net in gen_eqvnets(varc,o.fix,o.free): yield net
    
def gen_eqvnets(varc,fix,free):
    if len(free) == 0: 
        # print 'ready', fix
        yield bn.bn.BN(varc,fix, do_pic = False)
    else:
        nfree = free.copy()
        arc = nfree.pop()
        # print 'fix', fix, nfree, arc
        for net in gen_eqvnets_with_arc(varc,fix,nfree,arc): yield net

        arc=(arc[1],arc[0])
        # print 'then', fix, nfree, arc

        for net in gen_eqvnets_with_arc(varc,fix,nfree,arc): yield net
        
def g_eqvnets(bns):
    o = Orient(bns.varc, *skeleton(bns))
    return gen_eqvnets(bns.varc, o.fix, o.free)

def eqvnets(bnfile:str, resdir:str, constraint_file=''):

    cstrs = Constraints(constraint_file)

    bns=bnload(bnfile)

    if cstrs.violated(bns.arcs()):
        sys.exit("%s violates given constraints" % bnfile)

    resdirpath = Path(resdir)
    resdirpath.mkdir(parents=True, exist_ok=True) 
       
    i=0
    for net in g_eqvnets(bns):
        if resdir != None and cstrs.satisfied(net.arcs()):
            net.save(str(resdirpath/str(i))+".bn")
            i+=1

if __name__ == "__main__":
    typer.run(eqvnets)
