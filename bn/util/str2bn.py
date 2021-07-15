#!/usr/bin/env python
import coliche, bn.bn

def main(strfile, bnfile):

    strf = file(strfile)
    varc = int(strf.readline())
    
    arcs = []
    for i,l in enumerate(strf):
        arcs.extend([(p,i) for p in map(int, l.split()[2:])])

    bn.bn.BN(varc, arcs, do_pic=False).save(bnfile)

if __name__ == '__main__':
    coliche.che(main,'strfile; bnfile')
