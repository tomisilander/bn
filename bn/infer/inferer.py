#!/usr/bin/python

import bn.vd as vd
import ifr
import coliche
import bucketelim
import bn.model.bnmodel as bnmodel

def pretty_dstrs(varnames, dstrs):
    for vn, dstr in zip(varnames, dstrs):
        yield "%s: %s" % (vn, " ".join(["%.2f" % p for p in dstr]))

class Inferer():

    def __init__(self, fmt, state):
        self.fmt = fmt
        self.state = state

    def varix(self, t):

        if not t: return "No variable index or name found!"

        v = t.pop(0)
        
        if v.isdigit():
            return int(v)
        elif v in self.fmt.varnames:
            return list(self.fmt.varnames).index(v)
        else:
            return "Not good for variable index or name: %s!" % v


    def watch(self, t):
        for v in t:
            if v == '-*':
                self.state['watch'] = set()
            elif v == '*':
                self.state['watch'] = set(xrange(len(self.fmt.varnames)))
            else:
                out = v.startswith("-")
                v = self.varix([out and v[1:] or v])
                if isinstance(v, str): return v

                if out:
                    if v in self.state['watch']:
                        self.state['watch'].remove(v)
                else:
                    self.state['watch'].add(v)

    def reset(self, s) :
        self.state['evidence']=set()

    def evidence(self, t):

        v = self.varix(t)  # pops t[0]
        if isinstance(v, str): return v

        try:
            vc = self.fmt(v)
        except:
            return "Illegal variable index: %d!" % v

        if len(t) == 1:  # hard evidence
            if t[0].isdigit():
                l = int(t[0])
            elif t[0] in self.fmt.values:
                l = list(self.fmt.values).index(t[0])
            else:
                return "Not good for value index or name: %s!" % t[0]

            if not 0 <= l < vc:
                return "Illegal value index: %d!" % v

            e = [0.0] * vc
            e[l] = 1.0

        else:  # soft evidence
            try:
                e = map(float, t)
                if len(e) != vc:
                    return "Evidence vector of length %d expected (got %d)!" % (vc, len(e))
            except:
                return "Could not convert values to float!"

        self.insert_evidence(v, e)

    def nocmd(self):
        return "Unknown command!"


class JTInferer(Inferer):

    def __init__(self, ifrdir, state):
        self.ir = ifr.load(ifrdir, state)
        Inferer.__init__(self, self.ir.valcs)

    def insert_evidence(self,v,e):
        self.ir.insert_evidence(v,e)

    def reset(ir) :
        self.state['evidence'] = set()
        ir.reset()

    def infer(self):
        for v, dstr in enumerate(self.ir.infer()):
            if v not in self.state['watch'] : continue
            vn = self.fmt.varnames[v]
            print "%s: %s" % (vn, " ".join(["%.2f" % p for p in dstr]))


class BEInferer(Inferer):

    def __init__(self, vdfile, bnmfile, state):
        Inferer.__init__(self, vd.load(vdfile), state)
        self.bnm = bnmodel.load(bnmfile, self.fmt)

    def insert_evidence(self,v,e):
        self.state['evidence'].add((v,tuple(e)))

    def infer(self):
        pots = bucketelim.bnm2pots(self.bnm)
        eh = dict(self.state['evidence'])
        for v,vn in enumerate(self.fmt.varnames):
            if v not in self.state['watch'] : continue
            if v in eh:
                dstr = eh[v]
            else:
                e = [(vr,e.index(1.0)) for (vr, e) in self.state['evidence']]
                dstr = bucketelim.distrib(self.bnm,pots,(v,),e)
            print "%s: %s" % (vn, " ".join(["%.2f" % p for p in dstr]))


class Sampler(Inferer):

    def __init__(self, vdfile, bnmfile, state):
        Inferer.__init__(self, vd.load(vdfile), state)
        self.bnm = bnmodel.load(bnmfile, self.fmt)
        self.bnt = bnm.bn
        self.parents =  [list(sorted(bnt.parents(v))) for v in bnt.vars()]
        self.children = [list(sorted(bnt.children(v))) for v in bnt.vars()]

    def infer(self):

        eh = dict(self.state['evidence'])
        freevars = self.get_freevars()
        # freevars = tuple(v for v in self.bnt.vars() if v not in eh)
        # if not gibbs:
        #    tord = list(gen_totord(bnt))
        #    freevars = sorted(freevars, key=lambda v:tord.index(v))

        counts = dict((v,[0]*self.fmt.valcs(v)) for v in self.state['watch']  # For counting values
        # initial configuration

        cfg = [wheel(eh[v]) if (v in eh) else randint(0,self.fmt.valcs(v)-1)  for v in self.bnt.vars()]

        sigpool.watch('SIGUSR2')
        if self.time: sigpool.wait_n_raise(self.time, 'SIGUSR2')

        while True:

            for v in freevars: cfg[v] = wheel(self.get_dstr(v,cfg))
            w = self.get_weight(cfg)
            for v in counts:
                counts[v][cgf[v]] += w # how about soft evidence

            if 'SIGUSR2' in sigpool.flags: break
            sigpool.flags.remove('SIGUSR2')

     # CONTINUE FROM HERE ONE DAY by printing the distrs

        # normalize
        nzer = 1.0/sum(counts.itervalues())
        for xcfg in counts: counts[xcfg] *= nzer
        return counts

def main(irtype, ifrdir='', bnmfile=None, vdfile=None):
    
    cmds   = 'ewri'
    state = {'watch':set(), 'evidence':set()}

    if irtype == 'jt':
        ir    = JTInferer(ifrdir, state)
    elif irtype == 'bucketelim':
        ir = BEInferer(vdfile, bnmfile, state)
    else:
        print('Unknown inferer type:',irtype)
        return

    while True:
        l = raw_input().strip()
        if not l: continue
        if l.startswith("q"): break

        argv = l.split()
        c = argv.pop(0)

        if c == 'e':
            r = ir.evidence(argv)
        elif c == 'w':
            r = ir.watch(argv)
        elif c == 'r':
            r = ir.reset()
        elif c == 'i':
            r = ir.infer()
        else:
            r = ir.nocmd()
        if r: print "ERROR:", r


coliche.che(main,"""irtype
  --ifrdir ifrdir : if irtype is jt
  -f --fmt vdfile : needed but for jt
  --bnmodel bnmfile : if irtype is gibbs or bucketelim or lhweighting
  """)
