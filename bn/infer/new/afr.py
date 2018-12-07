#!/usr/bin/python

class actor():

    def __init__(valcs, bns, tht):

        v2ix = []
        vns2 = valcs.varnames[:]
        vls2 = valcs.values[:]
        for v in bns.vars():
            if bns.parents(v):
                v2ix.append(len(vns2))
                vns2.append(vns2[v]+'*')
                vls2.append(vls2[v])
                tht2.append(tht[v])
            else
                v2ix.append(v)

        valcs2 = vd.vd(bns2, vls2)
        
        # TWIN BN
        
        bn2 = bn.BN(len(vns2))
        for (f,t) in bns.arcs():
            bn2.addarc((f,t))
            f2, t2 = v2ix[f], v2ix[t]
            if f2 != f:
                bn2.addarc(f2, t2))
            else:
                bn2.addarc((f, t2))

    def act(v, a):

        v2 = self.v2idx[v]

        # Remove the arcs by action
        
        for p in bn2.parents(v2):
            bn2.delarc((p,v2))

        # create thta by bna

        tht2 = s['tht_o'][:] + s['tht_o'][:]
        tht2[v2] = {():[1.0/vc]*vc}

        
