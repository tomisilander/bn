#!/usr/bin/env python
from bn import BN
from data import Data
from score import Score
import math
from sets import Set
import bestforests
import os


def depx(v1,v2,cols,vc):

    # Collect counts
    c12 = [[0]*vc[v2] for x in xrange(vc[v1])]
    c1  =  [0]*vc[v1]
    c2  =  [0]*vc[v2]
    n   = 0
    for x,y in zip(cols[v1],cols[v2]):
        c12[x][y] += 1
        c1[x]     += 1
        c2[y]     += 1
        n         += 1
    n = float(n)
    
    # Calculate DEP
    res  = 0.0

    for x in xrange(vc[v1]):
        px = c1[x]/n
        for y in xrange(vc[v2]):
            py   = c2[y]/n
            pxy = c12[x][y]/n
            print x,y, pxy
            if pxy > 0:
                res += pxy * math.log(pxy / px / py)
    return res

def CL1(data):
    cols = data.cols()
    vc   = data.valcounts()
    def dep(v1,v2): return depx(v1,v2,cols,vc)

    tdep = []

    for v1 in xrange(data.varcount()):
        for v2 in xrange(v1):
            d = dep(v1,v2)
            tdep.append((d,v1,v2))
            tdep.append((d,v2,v1))

    tdep.sort()
    tdep.reverse()
#    print tdep
    
    ns = range(data.varcount())
    (d,x1,x2) = tdep[0]
    ts = [x1,x2]
    ns.remove(x1)
    ns.remove(x2)
    es = [(x1,x2)]
    while ns:
#        print ns
        x,y = [(x1,x2) for (d,x1,x2) in tdep if x1 in ts and x2 in ns][0]
        es.append((x,y))
        ts.append(y)
        ns.remove(y)

    bane = BN(vc)
    for e in es: bane.addarc(e)
    bestforests.reroot(bane, 0, Set())
    return bane

    
def ETC(data):
    cols = data.cols()
    vc   = data.valcounts()

    def dep(v1,v2): return depx(v1,v2,cols,vc)

    for x in xrange(data.varcount()):
        print ("%.2d: " % x), " ".join(["%.5f " % dep(x,y) for y in xrange(x)])
            

    def put(tr,x):
        lst, (c,a,b,d,dep_ab), rst = tr
        dep_cx = dep(c,x)
        dep_dx = dep(d,x)
        print "putting %d to [%d]%d=(%.5f)=%d[%d]" % (x,c,a,dep_ab,b,d)
        print "  based on %.5f %.5f, thus" % (dep_cx, dep_dx), 
        if dep_cx < dep_dx :
            print "right" 
            return put_right(tr,x)
        else :
            print "left" 
            return put_left(tr,x)

    def put_right(tr,x):
        lst, (c,a,b,d,dep_ab), rst = tr
        dep_ax = dep(a,x)
        print "   dep_ax = %.5f" % dep_ax
        if dep_ab < dep_ax:
            print "   shifting root"
            new_rn = x; new_dep = dep_ax
        else:
            new_rn = b; new_dep = dep_ab
        if not rst:
            print "   on empty"
            rst = (),(b,b,x,x,dep(b,x)),()
        else:
            print "   going down"
            rst = put(rst,x)
            
        return (lst,(c,a,new_rn,d,new_dep), rst)

    def put_left(tr,x):
        lst, (c,a,b,d,dep_ab), rst = tr
        dep_bx = dep(b,x)
        print "   dep_bx = %.5f" % dep_bx
        if dep_ab < dep_bx:
            print "   shifting root"
            new_ln = x; new_dep = dep_bx
        else:
            new_ln = a; new_dep = dep_ab
        if not lst:
            print "   on empty"
            lst =(), (x,x,a,a,dep(a,x)),()
        else:
            print "   going down"
            lst = put(lst,x)
            
        return (lst,(c,new_ln,b,d,new_dep), rst)

            
    vars = range(2,data.varcount())
    tr = ((), (0,0,1,1,dep(0,1)), ())
    trshow(tr,etr2dot)
    print ""
    while vars:
        tr = put(tr, vars.pop(0))
        tr = refoc(tr)
        if not check_inv(tr,cols,vc):
            trshow(tr,etr2dot)
            print "XXXXXXXXXXXXX ERROR XXXXXXXXXXXX"
        trshow(tr,etr2dot)
        print ""
            
    return tr


def refoc(tr):
    if not tr: return tr
    lst, (c,a,b,d,dep_ab), rst = tr
    return refoc(lst), (a,a,b,b,dep_ab), refoc(rst)


def get_nodes(tr):
    if not tr: return Set()
    lst, (c,a,b,d,dep_ab), rst = tr
    return Set([a,b]) | get_nodes(lst) | get_nodes(rst)

def check_inv(tr, cols, vc):
    if not tr: return True
    lst, (c,a,b,d,dep_ab), rst = tr

    lnodes = get_nodes(lst)
    ldeps = [depx(b,x,cols,vc) for x in lnodes if x != a]
    if ldeps and max(ldeps) > dep_ab:
        return False

    rnodes = get_nodes(rst)
    rdeps = [depx(a,x,cols,vc) for x in rnodes if x != b]
    if rdeps and max(rdeps) > dep_ab:
        return False

    return check_inv(lst,cols,vc) and check_inv(rst,cols,vc)

def trshow(tr,tdfunc):
    dotfn = "/tmp/tr.dot"

    trps  = "/tmp/tr.ps"
    trs2dotf(tr,dotfn,tr2dot)
    os.system("dot -Tps %s -o %s" % (dotfn,trps))

    etrps  = "/tmp/etr.ps"
    trs2dotf(tr,dotfn,etr2dot)
    os.system("dot -Tps %s -o %s" % (dotfn,etrps))

    os.system("gv %s &" % trps)
    os.system("gv %s" % etrps)
    os.unlink(dotfn); os.unlink(trps); os.unlink(etrps)
              
def trs2dotf(tr,fn,tdfunc):
    f = file(fn,"w")
    f.write(tdfunc(tr))
    f.close()
    

def dot_etr_narcs(etr,name):
    if not etr: return []
    lst, (c,a,b,d,dep_ab), rst = etr
    lines = [" %s [label=\"[%d]%d=(%.5f)=%d[%d]\"]" % (name,c,a,dep_ab,b,d)]
    pname = name[:-1]
    if pname: lines.append("%s -> %s [label=\"%s\"]" % (pname,name,name[-1]))
    llines = dot_etr_narcs(lst,name+"L")
    rlines = dot_etr_narcs(rst,name+"R")
    lines.extend(llines)
    lines.extend(rlines)
    return lines

def etr2dot(etr):
    lines = ["digraph klop {"]
    lines.extend(dot_etr_narcs(etr,"X"))
    lines.append("}")
    return "\n".join(lines)

def dot_tr_arcs(etr):
    if not etr: return []
    lst, (c,a,b,d,dep_ab), rst = etr
    lines = [" %d -- %d [label=\"%.5f\"]" % (a,b,dep_ab)]
    lines.extend(dot_tr_arcs(lst))
    lines.extend(dot_tr_arcs(rst))
    return lines
    
def tr2dot(etr):
    lines = ["graph klop {"]
    lines.extend(dot_tr_arcs(etr))
    lines.append("}")
    return "\n".join(lines)

def getarcs(tr):
    if not tr: return []
    lst, (c,a,b,d,dep_ab), rst = tr
    return [(a,b)]+getarcs(lst)+getarcs(rst)

def tr2bn(tr,vc):
    bane = BN(vc)
    for a in getarcs(tr): bane.addarc(a)
    bestforests.reroot(bane, 0, Set())
    return bane

if __name__ == '__main__':
    import sys
    dn = sys.argv[1]
    data = Data(dn)
    tr = ETC(data)
    # dotprint(tr)
    bane = tr2bn(tr,data.valcounts())
#    bane.print_str()
    print >>sys.stderr, Score(bane, data, 1.0).score()
    print CL1(data).arcs()
    print >>sys.stderr, Score(CL1(data), data, 1.0).score()
