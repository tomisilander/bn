#!/usr/bin/python

import sys, bn.vd


def names2ixs(n,names):
    if n == '*':
        return range(len(names))
    else:
	try:
		return [int(n)]
	except: # should be more specific
        	return [names.index(n)]

def main(vdfile):
    names = bn.vd.varnames(vdfile)

    cstrs = dict((name, [set(),set()]) for name in names)

    for l in sys.stdin:
        ls = l.strip()
        if ls == '' or l.startswith('#'): continue
        op,f,t = ls.split()
        
        # print op,f,t

        fis = names2ixs(f,names)
        tis = names2ixs(t,names)

        # print op,fis,tis

        for f in fis:
            (sf_must,sf_nope) = cstrs[names[f]]
            for t in tis:
                if f == t: continue

                if op == '+':
                    sf_must.add(t)
                    if t in sf_nope:
                        sf_nope.remove(t)
                elif op == '-':
                    sf_nope.add(t)
                    if t in sf_must:
                        sf_must.remove(t)
                elif op == '?':
                    if t in sf_must:
                        sf_must.remove(t)
                    if t in sf_nope:
                        sf_nope.remove(t)                    
                else:
                    print 'Whaaat?'

    for (fn, cs) in cstrs.iteritems():
        fi = names.index(fn)
        for t in cs[0]:
            print '+', fi, t
        for t in cs[1]:
            print '-', fi, t


if __name__ == "__main__":
    import coliche
    coliche.che(main,
                """vdfile
                """)
