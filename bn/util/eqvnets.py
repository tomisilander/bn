import bn.bn
from eqvorient import Orient
from bn.learn.constraints import Constraints

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
        
def eqvnets(bns):
    o = Orient(bns.varc, *skeleton(bns))
    # print o.fix
    # print o.free

    return gen_eqvnets(bns.varc, o.fix, o.free)

from coliche import che
import os, sys

def main(bnfile, resdir=None, constraint_file=''):

    cstrs = Constraints(constraint_file)

    bns=bn.bn.load(bnfile)
    if cstrs.violated(bns.arcs()):
        sys.exit("%s violates given constraints" % bnfile)

    if resdir != None:
        if os.path.exists(resdir):
            if not os.path.isdir:
                sys.exit('"%s" exists but is not a directory' % resdir)
        else:
            os.makedirs(resdir)
    
    i=0
    for net in eqvnets(bns):
        if resdir != None and cstrs.satisfied(net.arcs()):
            net.save(os.path.join(resdir,str(i)+".bn"))
            i+=1

che(main,
    """bnfile
    -d --dir resdir : directory to store nets
    -c constraint_file : a file with arcs marked with + or -
""")
