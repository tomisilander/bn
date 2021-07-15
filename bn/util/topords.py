#!/usr/bin/env python
from bn.bn import load

def main(bnfile):
    bn=load(bnfile)
    stages=[]
    varsleft=set(bn.vars())
    while len(varsleft)>0:
        sources=set(v for v in varsleft if len(bn.parents(v))==0)
        stages.append(sources)
        varsleft -= sources
        for v in sources:
            for c in bn.children(v):
                bn.delarc((v,c))
    
    return stages

def fac(n):
    r=1
    for x in xrange(1,n+1):
        r*=x
    return r

import coliche
stages = coliche.che(main,'bnfile')
print 'THIS DOES NOT WORK'
print stages
if stages != None:
    res = 1
    for s in stages: res *= fac(len(s))
    print res

