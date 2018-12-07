from operator import itemgetter, __mul__, __and__
from itertools import chain, izip

# STUPID ITEMGETTER SOMETIMES YIELDS TUPLE AND SOMETIMES NOT, THUS
def itembetter(ixs):
    return lambda xs: tuple(xs[i] for i in ixs)

def tht2pot(bnm,i):
    fami = [i]+list(bnm.bn.parents(i))
    fami.sort()
    iix = fami.index(i)

    def genpot():
        for pcfg in bnm.pcfgs(i):
            for v,tht in enumerate(bnm.theta(i,pcfg)):
                cfg = list(pcfg)
                cfg.insert(iix,v)                
                yield (tuple(cfg),tht)
    return (fami, tuple(genpot()))


def bnm2pots(bnm):
    return [tht2pot(bnm,i) for i in bnm.bn.vars()]

def print_buckets(buckets):
    for i,b in enumerate(buckets):
        print '#', i
        for (f,pot) in b:
            print f
            print pot
        print

def get_buckets(pots,e):
    buckets = [[] for p in pots] + [[]]
    for p in pots:
        (fam,pot) = p
        fp = (tuple(fam),pot)
        sfp = select(fp, e)
        if len(sfp[0]) == 0:
            buckets[-1].append(sfp)
        else:
            buckets[max(sfp[0])].append(sfp)
    return buckets

def select(fp, e): 
    evrs = zip(*e)[0]
    eh = dict(e)
    (fam,pot) = fp

    relvrs = set(fam) & set(evrs)
    if len(relvrs) == 0: return fp
        
    def match(cfg):
        for vr in relvrs:
            if cfg[fam.index(vr)] != eh[vr]:
                return False
        return True
    proj = itembetter(tuple(i for (i,vr) in enumerate(fam) if vr not in evrs))

    return (proj(fam), 
            tuple((proj(cfg), tht) for (cfg,tht) in pot if match(cfg)))

def marginalize(bnm,fp,i):
    (fam,pot) = fp
    iix = fam.index(i)
    newfam = list(fam)
    newfam.remove(i)

    newpot=dict((ncfg,0.0) for ncfg in bnm.cfgs(newfam))

    for cfg,t in pot:
        ncfg = list(cfg)
        del ncfg[iix]
        newpot[tuple(ncfg)] += t

    return (tuple(newfam),tuple(newpot.items()))

def multiply(bnm, b):
    (fams,pots) = zip(*b)

    pots = map(dict, pots)
    newfam = list(set(chain(*fams)))
    newfam.sort()
    projs = [itembetter(map(newfam.index, fam))
             for fam in fams]   

    def genpots():
        for cfg in bnm.cfgs(newfam):
            yield (cfg,  reduce(__mul__, (pot[proj(cfg)] 
                                          for (proj, pot) in izip(projs,pots))))
    return (tuple(newfam), tuple(genpots()))

def belim(bnm, pots, e):
    bs = get_buckets(pots, e)

    for i in xrange(len(bs)-2,-1,-1):
        if len(bs[i]) == 0: continue
        nfp = multiply(bnm,bs[i])
        (nfam,npot) = marginalize(bnm,nfp,i)
        if len(nfam)>0:
            bs[max(nfam)].append((nfam,npot))
        else:
            bs[-1].append((nfam,npot))

    return multiply(bnm, bs[-1])[1][0][1]


def distrib(bnm, pots, vrs, e):
    dstr = [belim(bnm,pots,tuple(sorted(chain(e,izip(vrs,cfg)))))
            for cfg in bnm.cfgs(vrs)]
    nzer = sum(dstr)
    return [p/nzer for p in dstr] 
    
if __name__ == '__main__':
    import bnmodel, vd
    vdfile = "iris/vd"
    varnames = tuple(vd.varnames(vdfile))
    valcs = vd.valcs(vdfile)
    bnm = bnmodel.load(varnames, valcs, "iris/mdl")
    e = ((4,0),)
    print belim(bnm, bnm2pots(bnm),e)

# Implement elimination order
