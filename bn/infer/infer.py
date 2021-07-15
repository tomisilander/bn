#!/usr/bin/env python
import sets, pot

def svs(vars):
    return "".join(map("ABCDEFGH".__getitem__, vars))

def globprop(jt, cpots, spots):
    
    def pass_message(x, y):
        sepix = min(x,y), max(x,y)
        r_old = spots[sepix]
        spots[sepix] = cpots[x] >> r_old
        cpots[y] *= spots[sepix] / r_old
        
    def collect_evidence(c, x):
        
        marked[x] = True
        
        for xn in jt.neighbours(x):
            if not marked[xn]:
                collect_evidence(x,xn)

        if c != None:
            pass_message(x, c)


    def distribute_evidence(x):

        marked[x] = True

        for xn in jt.neighbours(x):
            if not marked[xn]:
                pass_message(x, xn)

        for xn in jt.neighbours(x):
            if not marked[xn]:
                distribute_evidence(xn)


    nof_nodes = len(list(jt.nodes()))
    marked = [False]*nof_nodes
    collect_evidence(None, 0)
    marked = [False]*nof_nodes
    distribute_evidence(0)

def sepot(jt, clqs, valcs):
    spots = {}
    for (x,y) in jt.edges():
        svars = list(sets.Set(clqs[x]) & sets.Set(clqs[y]))
        svars.sort()
        spots[(x,y)] = pot.Potential(svars, valcs)
    return spots

def insert_evidence(lhs, v, p, vpot):
    old_lhv = lhs[v]
    new_lhv   = pot.Potential(old_lhv.vars, old_lhv.valcs)
    new_lhv.p = p[:]
    vpot   *= new_lhv / old_lhv
    lhs[v]  = new_lhv
    
def inferer(valcs, jt, clqs, pots, vclqs):

    def infer(insts):
        lhs = [pot.Potential([v], valcs) for v in xrange(len(vclqs))]
        for v, i in insts:

            if isinstance(i, int):
                newi = [0.0]*valcs(v)
                newi[i] = 1.0
                i = newi
                
            insert_evidence(lhs, v, map(float,i), pots[vclqs[v]])

        spots   = sepot(jt,clqs, valcs)

        globprop(jt, pots, spots)

        dstrs = []
        for v, clqix in enumerate(vclqs):
            cpot = pots[clqix]
            dstr = (cpot >> pot.Potential([v], valcs, 0.0)).normalize().p
            dstrs.append(dstr)
        return dstrs

    return infer

if __name__ == '__main__' :

    import coliche, vd, jtr, trg, udg

    def main(jtrfile, clqfile, vcxfile, vdfile, potfile):
        valcs = vd.valcser(vdfile)
        clqs  = [clq for (w,clq) in trg.wclqs_load(clqfile)]
        vclqixs = map(int, file(vcxfile))
        jt      = udg.load(jtrfile) 
        cpots   = list(pot.load(potfile, clqs, valcs))

        ifr = inferer(valcs, jt, clqs, cpots, vclqixs)

        for v, vdstr in enumerate(ifr([])):
            print svs([v])," ",  "  ".join(["%.2f" % p for p in vdstr])
        
    coliche.che(main,'jtrfile; clqfile; vcxfile; vdfile; potfile')
