#!/usr/bin/python

import sys, math

import data
import score

from data import Data
from score import Score
import vd

from bn import BN

valcs = vd.fn2valcs("y.vd")
data  = Data("y.tidt")
ess   = 1.0

def distance(v1, v2) :
    return math.sqrt(sum(map(lambda x,y: (x-y)**2, v1, v2)))

def checkvec(cand, corr):
    ok = distance(cand, corr) < 0.01
    if not ok :
        print >>sys.stderr, "Test failed (cand, corr):"
        print >>sys.stderr, "\n".join(map(str, zip(cand,corr)))
    return ok


# TEST 1 - EMPTY NET

bn = BN(valcs)
s = Score(bn, data, ess)

ans = [-1250.5488145294876,
       -1171.1291846986223,
       -976.40166811463496,
       -892.82769670723064,
       -83.102000300590589,
       -99.165032538714513,
       -954.58540412074035,
       -749.0057745498616,
       -2596.4405910417199]

if not checkvec (s.vscores ,ans):
    print >>sys.stderr, "i.e Test 1 failed."
    sys.exit(1)
    
# TEST 2 - ONE ARC

bn = BN(valcs)
bn.addarc((1,3))
s = Score(bn, data, ess)

ans =[-1250.5488145294876,
      -1171.1291846986223,
      -976.40166811463496,
      -897.45684229080427,
      -83.102000300590589,
      -99.165032538714513,
      -954.58540412074035,
      -749.0057745498616,
      -2596.4405910417199]

if not checkvec (s.vscores ,ans):
    print >>sys.stderr, "i.e Test 2 failed."


# TEST 3 - THREE ARCS

bn = BN(valcs)
bn.addarc((1,3))
bn.addarc((2,3))
bn.addarc((5,3))
s = Score(bn, data, ess)

ans = [-1250.5488145294876,
       -1171.1291846986223,
       -976.40166811463496,
       -929.05299377124084,
       -83.102000300590589,
       -99.165032538714513,
       -954.58540412074035,
       -749.0057745498616,
       -2596.4405910417199]

if not checkvec (s.vscores ,ans):
    print >>sys.stderr, "i.e Test 3 failed."


# TEST 4 - FULL NET

bn = BN(valcs)
for arc in [(i,j) for i in bn.vars() for j in bn.vars() if i<j] :
    bn.addarc(arc)

for i in xrange(1000):
    s = Score(bn, data, ess)

ans = [-1250.5488145294876,
       -992.26213190977387,
       -970.83693234779287,
       -954.42212335693341,
       -136.40118124208118,
       -198.45699718633341,
       -1188.6797357589467,
       -1164.4110829375766,
       -3416.4791511414883]

if not checkvec (s.vscores ,ans):
    print >>sys.stderr, "i.e Test 4 failed."


    
