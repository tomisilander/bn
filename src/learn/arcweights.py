#!/usr/bin/env python
import bn.bn, data, scorefactory
from math import exp

def toggle_arc(bns,a):
    if bns.has_arc(a):
        bns.delarc(a,do_pic=False)
    else:
        bns.addarc(a,do_pic=False)        

def arcweights(bns, sc, arcs=None):
        
    if arcs == None: arcs = bns.arcs()

    for a in arcs:
        harc = 1 if bns.has_arc(a) else -1
        toggle_arc(bns,a)
        (f,t) = a
        yield (a, (harc*(sc.vscores[t] - sc.score_ss_var(bns,t))))
        toggle_arc(bns,a)
        
if __name__ == '__main__':
    
    def main(bnfile, bdtfile, scoretype='BDeu', ess=1.0,
             vdfile=None, sort=False, probratio=False, arcfile=None,
             cachefile=None):
        
        bdt = data.Data(bdtfile)
        sc = scorefactory.getscorer(bdt,scoretype,ess,cachefile=cachefile)

        bns = bn.bn.load(bnfile,False)
        sc.score_new(bns)

        arcs = None if arcfile == None else [tuple(map(int,l.split()))
                                             for l in open(arcfile)]
            
        warcs = sorted(arcweights(bns,sc,arcs), key = lambda x: -x[1]) if sort \
                else arcweights(bns,sc, arcs)

        names = [l.split("\t",1)[0] for l in file(vdfile)] if vdfile \
                else map(str, range(bns.varc))
        
        for ((f,t),s) in warcs:
            if probratio: s = exp(s)

            print names[f], names[t], s
            
    import coliche
    coliche.che(main,
                ''' bnfile; bdtfile
                -g --goodness scoretype BDeu|fNML|AIC|BIC : default: BDeu
                -e --ess ess (float) : default 1.0
                -n --vdfile vdfile   : to print names not indices
                -s --sort            : sort by weights
                -p --probratio       : probratio instead of logdiff
                -a --arcs arcfile    : default: arcs in the bn
                -m --cachefile cachefile: local scores
                ''')
