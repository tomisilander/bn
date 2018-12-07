#!/usr/bin/python

import math, operator
from itertools import imap, product
import disdat, bn.vd, bn.bn

def normalize(xs):
    s = sum(xs)
    if s == 0:
        xs = [1]*len(xs)
    return map((1.0/s).__mul__, xs)

def cnml(frq):
    if frq:
        return (frq+1) * pow((frq+1.0)/frq, frq)
    else:
        return 1.0

class BnModel:

    def __init__(self, bn):
        self.bn = bn


    def save(self, varnames, fn):

        f = open(fn,'w')

        for i in self.bn.vars():
            pcc = self.nof_pcfgs(i)
            lenthti = len(self.thti(i))
            sparse = lenthti < 0.8*pcc
            
            print >>f, '#@SPARSE@' if sparse else '#@DENSE@'

            print >>f, '\t'.join([varnames[i]]
                                 + map(varnames.__getitem__, 
                                       sorted(self.bn.parents(i))))

            if sparse:
                print >>f, lenthti
                for pcfg,dst in self.thti(i).iteritems():
                    print >>f, '\t'.join(map(str,pcfg)),'\t'.join(map(str,dst)) 
            else:
                for pcfg in self.pcfgs(i):
                    print >>f, '\t'.join(map(str, self.theta(i,pcfg)))

            print >>f
        f.close()


    def set_unifs(self):
	self.unif = [normalize([1]*vc) for vc in self.valcounts]
	
    def init_param_learning(self, nof_vals, ltype, ess=None):
        self.valcounts = [n for n in nof_vals]
        self.ss = [{} for vci in self.valcounts]
        self.thetas    = None
        self.type      = ltype
	self.set_unifs()

        
        if self.type == "ml": ess = 0.0
        if self.type in ("bdeu", "dir", "ml", "bds", "bdq"):
            self.esss = [ess]*self.bn.varc
            if self.type == "bdeu":
                for i, vci in enumerate(self.valcounts):
                    pcc = self.nof_pcfgs(i)
                    self.esss[i] /= pcc*vci

    def add_d_to_ss(self,d):
        for i in xrange(self.bn.varc):
            self.add_di_to_ss(d,i)

    def del_d_from_ss(self,d):
        for i in xrange(self.bn.varc):
            self.del_di_from_ss(d,i)

    def add_di_to_ss(self,d,i,vci=None,pi=None):
        if vci == None: vci = self.valcounts[i]
        if pi ==  None: pi  = list(sorted(self.bn.parents(i)))

        di = d[i]
        if di == -1 : return

        pcfg = tuple(map(d.__getitem__, pi)) # maybe ()
        if -1 in pcfg: return

        ssi = self.ss[i]
        if pcfg not in ssi :
            ssi[pcfg] = [0]*vci

        ssi[pcfg][di] += 1


    def del_di_from_ss(self,d,i,vci=None,pi=None):
        if vci == None: vci = self.valcounts[i]
        if pi ==  None: pi  = list(sorted(self.bn.parents(i)))

        di = d[i]
        if di == -1 : return

        pcfg = tuple(map(d.__getitem__, pi)) # maybe ()
        if -1 in pcfg: return

        ssi = self.ss[i]
        ssi[pcfg][di] -= 1
        if ssi[pcfg] == [0]*vci:
            del ssi[pcfg] # cleanup

    def add_dti_to_ss(self,i,dt):
        vci = self.valcounts[i]
        pi = list(self.bn.parents(i))
        pi.sort()

        for d in imap(list, dt.dats()):
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
                return dict([(pcfg, normalize(map(self.esss[i].__add__, freqs)))
                             for pcfg, freqs in ssi.iteritems()])
            elif self.type == "cnml":
                return dict([(pcfg, normalize(map(cnml, freqs)))
                             for pcfg, freqs in ssi.iteritems()])
            else:
                raise "iiks"

    def cache_thetas(self):
        self.thetas = map(self.thti, self.bn.vars())


    def theta(self, i, pcfg):
        return self.thti(i).get(pcfg, self.unif[i])

    def thetd(self, i, d):
        pi = list(self.bn.parents(i))
        pi.sort()
        pcfg = tuple(map(d.__getitem__, pi))
        return self.theta(i, pcfg)


    def logprob_d(self,d):
        dl = list(d)
        logthtd = lambda i: math.log(self.thetd(i,dl)[dl[i]])
        return sum(imap(logthtd, self.bn.vars()))

    def logprob_D(self, dt):
        return sum(imap(self.logprob_d, dt.dats()))

    def cfgs(self, vrs):
        vrsvls = (xrange(self.valcounts[vr]) for vr in  vrs)
        return product(*vrsvls)

    def pcfgs(self, i):
        return self.cfgs(sorted(self.bn.parents(i)))
         
    def nof_pcfgs(self, i):
        vcsps = (self.valcounts[vr] for vr in  self.bn.parents(i))
        return reduce(operator.mul, vcsps, 1L)
        
    
def load(fn, valcs):
    self = BnModel(bn.bn.BN(valcs.nof_vars))
    self.valcounts = valcs.vcs
    thetas = [None] * valcs.nof_vars
    self.set_unifs()
    sparse = False
    
    f = open(fn)
    l = f.readline()
    while len(l)>0:
        if l.startswith('#') or len(l.strip()) == 0:
            if l.strip().upper() == '#@SPARSE@' : sparse=True
            if l.strip().upper() == '#@DENSE@'  : sparse=False

            l = f.readline()
            continue

        vars = l.strip().split('\t')
        varis = map(valcs.varnames.index, vars)
        i = varis.pop(0)
        for p in varis: self.bn.addarc((p,i))
        if sparse:
            nof_ps = len(varis)
            pcc = int(f.readline().strip())
            pdict = {}
            for j in xrange(pcc):
                fields = f.readline().split()
                pcfg = tuple(map(int,fields[:nof_ps]))
                dst  = map(float,fields[nof_ps:])
                pdict[pcfg]=dst
            thetas[i] = pdict
        else:
            thetas[i] = dict((pcfg,map(float,f.readline().split()))
                             for pcfg in self.pcfgs(i))

        l = f.readline()

    self.thetas = thetas
    f.close()
    return self

def bnt(bnm): # strangely needed for inout
    return bnm.bn

# maybe learning should be put to another file
def main(vdfile, bnfile, datfile, outfile, ess=1.0, type="bdeu"):
    valcs = bn.vd.load(vdfile)
    bns = bn.bn.load(bnfile, do_pic=False)
    dat = disdat.RowData(vdfile, datfile)
    bnm = BnModel(bns)
    bnm.init_param_learning(valcs.vcs, type.lower(), ess)
    bnm.learn_params(dat)
    bnm.save(valcs.varnames,outfile)

if __name__ == '__main__':
    from coliche import che
    che(main,
        ''' vdfile; bnfile; datfile; outfile
        -t --type type bdeu|cnml|dir|ml|bds|bdq : bdeu, bds, bdq, ml, cnml or dir: default bdeu
        -e --ess ess (float) : a parameter if needed: default 1.0
        ''')
