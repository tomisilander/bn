#!/usr/bin/env python
import sets
import inout
import coliche
import vd, bn

def pretty_dstrs(varnames, dstrs):
    for vn, dstr in zip(varnames, dstrs):
        yield "%s: %s" % (vn, " ".join(["%.2f" % p for p in dstr]))

def varix(ir, t, allow_neg = False):

    if not t:
        return "No variable index or name found!"

    v = t.pop(0)
        
    try:
        v = int(v)
    except:
        if v in ir.valcs.varnames:
            v = list(ir.valcs.varnames).index(v)
        else:
            return "Not good for variable index or name: %s!" % v

    if v<0:
        if allow_neg:
            v = -v
        else:
            return "Negative variable index (%d) not allowed!" % v
    
    return v


def evidence(ir, t,s):

    v = varix(ir,t)

    try:
        vc = ir.valcs(v)
    except:
        return "Illegal variable index: %d!" % v

    if isinstance(v, str) : return v
        
    if len(t) == 1:
        try:
            l = int(t[0])
        except:
            if t[0] in ir.valcs.values:
                l = list(ir.values).index(t[0])
            else:
                return "Not good for value index or name: %s!" % l

        if not 0<= l <vc:
            return "Illegal value index: %d!" % v        
        e = [0.0]*vc
        e[l] = 1.0

    else:
        try:
            e = map(float, t)
            if len(e) != vc:
                return "Evidence vector of length %d expected (got %d)!" \
                       % (vc, len(e))
        except:
            return "Could not convert values to float!"

    ir.insert_evidence(v,e)
        

def act(ir, t, s):

    v = varix(ir,t)

    try:
        vc = ir.valcs(v)
    except:
        return "Illegal variable index: %d!" % v

    if isinstance(v, str) : return v
        
    if len(t) == 1:
        try:
            l = int(t[0])
        except:
            if t[0] in ir.valcs.values:
                l = list(ir.values).index(t[0])
            else:
                return "Not good for value index or name: %s!" % l

        if not 0<= l <vc:
            return "Illegal value index: %d!" % v        
        e = [0.0]*vc
        e[l] = 1.0

    else:
        try:
            e = map(float, t)
            if len(e) != vc:
                return "Evidence vector of length %d expected (got %d)!" \
                       % (vc, len(e))
        except:
            return "Could not convert values to float!"

    

    bns = s['bn_o']
        
    # create bna twin

    vrc    = len(ir.valcs.varnames)
    v2     = v + vrc
    vns2   = ir.valcs.varnames + tuple([vn+'*' for vn in ir.valcs.varnames])
    vls2   = ir.valcs.values + ir.valcs.values
    valcs2 = vd.vd(vns2, vls2)
    
    bn2 = bn.BN(2*vrc)

    for (f,t) in bns.arcs():
        bn2.addarc((f,t))
        if bns.parents(f):
            bn2.addarc((f+vrc, t+vrc))
        else:
            bn2.addarc((f, t+vrc))

    # Now cut remove the arcs by action
        
    for p in bn2.parents(v2):
        bn2.delarc((p,v2))

    # create thta by bna

    tht2 = s['tht_o'][:] + s['tht_o'][:]
    tht2[v2] = {():[1.0/vc]*vc}

    # get inferer for the acted model
    
    needed = ['ifr_o']
    haved  = {'bn_o': bn2, 'tht_o': tht2, 'vd_o' : valcs2}
    inout.inout(needed, haved)
    ir2 = haved['ifr_o']
    

    s2 = s.copy()
    w2 = s2['watch'][:]
    for i in s['watch']:
        w2.append(i+vrc)
    s2['watch'] = w2

    print bn2.arcs()

    
    evidence(ir2, ["D","1"], s2) 
    ir2.insert_evidence(v2, e)
    infer(ir2, [], s2)


def watch(ir, t, s) :
    for v in t:
        if v == '-*':
            s['watch'] = sets.Set()
        elif v == '*':
            s['watch'] = range(len(ir.valcs.varnames))
        else:
            v = varix(ir, [v], True)
            if isinstance(v, str) : return v
            
            if v < 0:
                if -v in s['watch']:
                    s['watch'].remove(-v)
            else:
                    s['watch'].add(v)
    
def reset(ir, t, s) :
    ir.reset()

def infer(ir, t, s):
    for v, dstr in enumerate(ir.infer()):
        if v not in s['watch'] : continue
        vn = ir.valcs.varnames[v]
        print "%s: %s" % (vn, " ".join(["%.2f" % p for p in dstr]))        

def nocmd(ir, t,s):
    return "Unknown command!"

def main(vdfile, bnfile, thtfile):

    needed = ['ifr_o', 'vd_o', 'bn_o', 'tht_o']
    haved  = {'vdfile'  : vdfile, 'bnfile'  : bnfile, 'thtfile' : thtfile}

    inout.inout(needed, haved)
    ir = haved['ifr_o']
    
    cmd    = {'e' : evidence,
              'w' : watch,
              'a' : act,
              'r' : reset,
              'i' : infer}
    
    state = {'watch':sets.Set(),
             'bn_o': haved['bn_o'],
             'tht_o': list(haved['tht_o'])}

    while True:
        l = raw_input().strip()
        if not l: continue
        if l.startswith("q"): break

        argv = l.split()
        c = argv.pop(0)

        r = cmd.get(c, nocmd)(ir, argv, state)
        if r: print "ERROR:", r
            
coliche.che(main,"""vdfile; bnfile; thtfile""")
