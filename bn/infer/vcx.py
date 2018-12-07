#!/usr/bin/python

def first(p, xs):
    for i,x in enumerate(xs):
        if p(x): return i, x
    return -1, None


# For each variable find the clique index for its family

def vclqs(bn, clqlst):

    def gen():
        clqsets = map(set, clqlst)
        for v in bn.vars():
            fam = set(bn.parents(v))
            fam.add(v)
            yield first(fam.issubset, clqsets)[0]

    return list(gen())

def load(vcxfile):
    return map(int, file(vcxfile).read().split())

def save(vcx, vcxfile):
    print >> file(vcxfile,"w"), "\n".join(map(str, vcx))
