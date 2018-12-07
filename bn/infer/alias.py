from math import floor
from random import random

def dstr2alias(dstr):
    nvals = len(dstr)
    ndstr = [p*nvals for (i,p) in enumerate(dstr)]
    high = [[i,p] for (i,p) in enumerate(ndstr) if p>1]
    low  = [[i,p] for (i,p) in enumerate(ndstr) if p<1]
    while len(low)>0:
        (li,lp) = low.pop(0)
        (hi,hp) = high.pop(0)
        yield(lp,li,hi)

        hp -= (1-lp)
        if hp < 1:
            low.append([hi,hp])
        elif hp >= 0:
            high.append([hi,hp])

    for (hi,hp) in high:
        yield (1,hi,hi)

def sample(a):
     r = random()*len(a)
     i = int(floor(r))
     ip = r-i
     (p,j,alt) = a[i]

     return j if ip<=p else alt

if __name__ == '__main__':
    a = list(dstr2alias([0.2,0.5,0.1,0.2]))
    for i in xrange(100000):
        x = sample(a)
        # print x
