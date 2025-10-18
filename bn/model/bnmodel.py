#!/usr/bin/env python
import math
import operator
from itertools import product, chain
from functools import reduce
import disdat
import bn.vd
import bn.bn

def normalize(xs):
    xs = list(xs)
    s = sum(xs)
    if s == 0:
        xs = [1]*len(xs)
    return tuple(map((1.0/s).__mul__, xs))

def cnml(frq):
    if frq:
        return (frq+1) * pow((frq+1.0)/frq, frq)
    else:
        return 1.0

class BnModel:

    def __init__(self, bn, valcs=None, use_density=False):
        self.bn = bn
        self.valcs = valcs
        self.use_density = use_density and valcs is not None

    def save(self, varnames, fn):

        f = open(fn,'w')

        for i in self.bn.vars():
            pcc = self.nof_pcfgs(i)
            lenthti = len(self.thti(i))
            sparse = lenthti < 0.8*pcc
            
            print('#@SPARSE@' if sparse else '#@DENSE@', file=f)

            parent_names = (varnames[p] for p in sorted(self.bn.parents(i)))
            print('\t'.join(chain((varnames[i],),parent_names)), file=f)

            if sparse:
                print(lenthti, file=f)
                for pcfg,dst in self.thti(i).items():
                    print('\t'.join(map(str,pcfg)),'\t'.join(map(str,dst)), file=f)
            else:
                for pcfg in self.pcfgs(i):
                    print('\t'.join(map(str, self.theta(i,pcfg))), file=f)

            print(file=f)
        f.close()


    def set_unifs(self):
        self.unif = [normalize([1]*vc) for vc in self.valcounts]
	
    def init_param_learning(self, nof_vals, ltype, ess=None):
        self.valcounts = [n for n in nof_vals]
        self.ss = [{} for vci in self.valcounts]
        self.thetas    = None
        self.type      = ltype
        self.set_unifs()

        
        if self.type == "ml": 
            ess = 0.0
        if self.type in ("bdeu", "dir", "ml", "bds", "bdq"):
            self.esss = [ess]*self.bn.varc
            if self.type == "bdeu":
                for i, vci in enumerate(self.valcounts):
                    pcc = self.nof_pcfgs(i)
                    self.esss[i] /= pcc*vci

    def add_d_to_ss(self,d):
        for i in range(self.bn.varc):
            self.add_di_to_ss(d,i)

    def del_d_from_ss(self,d):
        for i in range(self.bn.varc):
            self.del_di_from_ss(d,i)

    def add_di_to_ss(self,d,i,vci=None,pi=None):
        if vci is None: 
            vci = self.valcounts[i]
        if pi is  None: 
            pi  = list(sorted(self.bn.parents(i)))

        di = d[i]
        if di == -1 : 
            return

        pcfg = tuple(map(d.__getitem__, pi)) # maybe ()
        if -1 in pcfg: 
            return

        ssi = self.ss[i]
        if pcfg not in ssi :
            ssi[pcfg] = [0]*vci

        ssi[pcfg][di] += 1


    def del_di_from_ss(self,d,i,vci=None,pi=None):
        if vci is None: 
            vci = self.valcounts[i]
        if pi is None: 
            pi  = list(sorted(self.bn.parents(i)))

        di = d[i]
        if di == -1 : 
            return

        pcfg = tuple(map(d.__getitem__, pi)) # maybe ()
        if -1 in pcfg: 
            return

        ssi = self.ss[i]
        ssi[pcfg][di] -= 1
        if ssi[pcfg] == [0]*vci:
            del ssi[pcfg] # cleanup

    def add_dti_to_ss(self,i,dt):
        vci = self.valcounts[i]
        pi = list(self.bn.parents(i))
        pi.sort()

        for d in map(list, dt.dats()):
            self.add_di_to_ss(d,i,vci,pi)

        if self.type == "bds": # empirical prior of BDs
            self.esss[i] /= len(self.ss[i])*vci

    def learn_params(self, dt, calc_thetas=True):
        # you have to call init_params_learning first
        for i in self.bn.vars():
            self.add_dti_to_ss(i,dt)

        if calc_thetas:
            self.cache_thetas()

    def thti(self, i):

        if self.thetas:
            return self.thetas[i]
        else:
            ssi = self.ss[i]
            if self.type in ("bdeu", "dir", "ml", "bds", "bdq"): 
                return {pcfg : normalize(map(self.esss[i].__add__, freqs))
                             for pcfg, freqs in ssi.items()}
            elif self.type == "cnml":
                return {pcfg : normalize(map(cnml, freqs))
                             for pcfg, freqs in ssi.items()}
            else:
                raise "iiks"

    def cache_thetas(self):
        self.thetas = tuple(map(self.thti, self.bn.vars()))

    def theta(self, i, pcfg):
        return self.thti(i).get(pcfg, self.unif[i])

    def thetd(self, i, d):
        pi = list(self.bn.parents(i))
        pi.sort()
        pcfg = tuple(map(d.__getitem__, pi))
        return self.theta(i, pcfg)

    def logprob_di(self, i, d):
        di = d[i]
        p_di = self.thetd(i,d)[di]
        rng_di = self.valcs.ranges[i][di] if self.use_density else 1
        return math.log(p_di/rng_di)

    def logprob_d(self, d):
        dl = list(d)
        return sum(self.logprob_di(i, dl) for i in self.bn.vars())

    def logprob_D(self, dt):
        return sum(map(self.logprob_d, dt.dats()))

    def cfgs(self, vrs):
        vrsvls = (range(self.valcounts[vr]) for vr in  vrs)
        return product(*vrsvls)

    def pcfgs(self, i):
        return self.cfgs(sorted(self.bn.parents(i)))
         
    def nof_pcfgs(self, i):
        vcsps = (self.valcounts[vr] for vr in  self.bn.parents(i))
        return reduce(operator.mul, vcsps, 1)
        
    
def load(fn, valcs):
    self = BnModel(bn.bn.BN(valcs.nof_vars), valcs)
    self.valcounts = valcs.vcs
    thetas = [None] * valcs.nof_vars
    self.set_unifs()
    sparse = False
    
    f = open(fn)
    line = f.readline()
    while len(line)>0:
        if line.startswith('#') or len(line.strip()) == 0:
            if line.strip().upper() == '#@SPARSE@' : 
                sparse=True
            if line.strip().upper() == '#@DENSE@'  : 
                sparse=False

            line = f.readline()
            continue

        vars = line.strip().split('\t')
        varis = list(map(valcs.varnames.index, vars))
        i = varis.pop(0)
        for p in varis: 
            self.bn.addarc((p,i))
        if sparse:
            nof_ps = len(varis)
            pcc = int(f.readline().strip())
            pdict = {}
            for j in range(pcc):
                fields = f.readline().split()
                pcfg = tuple(map(int,fields[:nof_ps]))
                dst  = map(float,fields[nof_ps:])
                pdict[pcfg] = tuple(dst)
            thetas[i] = pdict
        else:
            thetas[i] = {pcfg : tuple(map(float, f.readline().split()))
                        for pcfg in self.pcfgs(i)} 

        line = f.readline()

    self.thetas = thetas
    f.close()
    return self

def bnt(bnm): # strangely needed for inout
    return bnm.bn

# maybe learning should be put to another file
def main(args):
    valcs = bn.vd.load(args.vdfile)
    bns = bn.bn.load(args.bnfile, do_pic=False)
    dat = disdat.RowData(args.vdfile, args.datfile)
    bnm = BnModel(bns, valcs)
    bnm.init_param_learning(valcs.vcs, args.type.lower(), args.ess)
    bnm.learn_params(dat)
    bnm.save(valcs.varnames, args.outfile)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('vdfile', help='VD file')
    parser.add_argument('bnfile', help='BN file')
    parser.add_argument('datfile', help='Data file')
    parser.add_argument('outfile', help='Output file')
    parser.add_argument('-t', '--type', default='bdeu', choices=['bdeu', 'cnml', 'dir', 'ml', 'bds', 'bdq'], help='Type of model (default: bdeu)')
    parser.add_argument('-e', '--ess', type=float, default=1.0, help='Evidence strength (default: 1.0)')

    args = parser.parse_args()

    main(args)
