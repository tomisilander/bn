#!/usr/bin/env python
import re

def varnames(filename):
    return tuple([l.split("\t")[0] for l in file(filename)])

def fn2valcs(filename):
    return tuple([l.count("\t") for l in file(filename)])

def valcs(filename):
    for l in file(filename):
        yield l.count("\t")

def valcser(filename):
    vcs = tuple(valcs(filename))
    return lambda vars: (isinstance(vars, int)) and vcs[vars] or map(vcs.__getitem__, vars)

def get_ranges(valnames):
    rng_re = re.compile('\s*[\[|\]]\s*([\d.]+)\s+..\s*([\d.]+)\s*\]\s*')

    def get_range(vn):
        vn_match = rng_re.match(vn)
        vn_is_range = not vn_match is None 
        if vn_is_range:
            return float(vn_match.group(2)) - float(vn_match.group(1))
        else:
            return 1.0

    return [list(map(get_range, vns_i)) for vns_i in valnames]

def vd(varnames, valnames):

    vcs = tuple(map(len, valnames))

    def f(vars):
        if isinstance(vars, int):
            return vcs[vars]
        else:
            return map(vcs.__getitem__, vars)

    f.nof_vars = len(varnames)
    f.varnames = varnames
    f.values   = valnames
    f.vcs      = vcs
    f.ranges   = get_ranges(valnames)

    return f


def load(vdfile):
    vns, vls = zip(*[l.strip().split("\t",1) for l in file(vdfile)])
    vls = tuple([tuple(vs.split("\t")) for vs in vls])
    return vd(vns, vls)
    
def save(f, vdfile):
    vdf = file(vdfile,"w")
    for vn, vls in zip(f.varnames, f.values):
        print >>vdf, "\t".join((vn, "\t".join(vls)))
    vdf.close()
