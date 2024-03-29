#!/usr/bin/env python
import coliche, bnmodel, bucketelim, vd

def pretty_dstrs(fmt, dstrs):
    for vn, dstr in zip(fmt.varnames, dstrs):
        yield "%s: %s" % (vn, " ".join(["%.2f" % p for p in dstr]))

def varix(fmt, t):

    if not t: return "No variable index or name found!"

    v = t.pop(0)
        
    if v.isdigit():
        return int(v)
    elif v in fmt.varnames:
        return fmt.varnames.index(v)
    else:
        return "Not good for variable index or name: %s!" % v

# Should just check and mark evidence
def evidence(bnm, fmt, t, s):

    v = varix(fmt,t) # pops t[0]
    if isinstance(v, str) : return v
    
    try:
        vc = fmt(v)
    except:
        return "Illegal variable index: %d!" % v

        
    if len(t) == 1: # hard evidence
        if t[0].isdigit():
            l = int(t[0])
        elif t[0] in fmt.valnames[v]:
            l = list(fmt.valnames[v]).index(t[0])
        else:
            return "Not good for value index or name: %s!" % t[0]
        if not 0 <= l < vc:
            return "Illegal value index: %d!" % v        

        e = [0.0]*vc
        e[l] = 1.0

    else: # soft evidence
        try:
            e = map(float, t)
            if len(e) != vc:
                return "Evidence vector of length %d expected (got %d)!" \
                       % (vc, len(e))
        except:
            return "Could not convert values to float!"

    s['evidence'].add((v,tuple(e)))

def watch(bnm, fmt, t, s) :
    for v in t:
        if v == '-*':
            s['watch'] = set()
        elif v == '*':
            s['watch'] = range(len(fmt.varnames))
        else:
            out = v.startswith("-")
            v = varix(fmt.varnames, [out and v[1:] or v])
            if isinstance(v, str) : return v
            
            if out:
                if v in s['watch']:
                    s['watch'].remove(v)
            else:
                s['watch'].add(v)
    
def reset(bnm, fmt, t, s) :
    s['evidence']=set()
    
def infer(bnm, fmt, t, s):
    pots = bucketelim.bnm2pots(bnm)
    eh = dict(s['evidence'])
    for v,vn in enumerate(fmt.varnames):
        if v not in s['watch'] : continue
        if v in eh:
            dstr = eh[v]
        else:
            e = [(vr,e.index(1.0)) for (vr, e) in s['evidence']]
            dstr = bucketelim.distrib(bnm,pots,(v,),e)
        print "%s: %s" % (vn, " ".join(["%.2f" % p for p in dstr]))

def nocmd(bnm, fmt, t,s):
    return "Unknown command!"

def main(vdfile, mdlfile):
    
    valcs = vd.load(vdfile)
    bnm = bnmodel.load(mdlfile,valcs)

    cmd    = {'e' : evidence,
              'w' : watch,
              'r' : reset,
              'i' : infer}
    state = {'watch':set(),
             'evidence':set()
             }

    while True:
        l = raw_input().strip()
        if not l: continue
        if l.startswith("q"): break

        argv = l.split()
        c = argv.pop(0)

        r = cmd.get(c, nocmd)(bnm, valcs, argv, state)
        if r: print "ERROR:", r
            

coliche.che(main,"""vdfile; mdlfile""")
