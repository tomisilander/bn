#!/usr/bin/env python
import bn
import coliche

def main(bnfile, strfile):

    bns = bn.load(bnfile)
    strf = file(strfile,"w")

    print >>strf, bns.varc
    
    for v in bns.vars():
        ps = sorted(bns.parents(v))
        print >>strf, len(bns.children(v)), len(ps), " ".join(map(str,ps))
    strf.close()

if __name__ == '__main__':
    coliche.che(main,'bnfile; strfile')
