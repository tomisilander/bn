#!/usr/bin/python
import sys
import ifr
import coliche

def infer_row(ir,d):
    ir.reset()

    for i,v in enumerate(d):
        if v != -1:
            ir.insert_evidence(i,v)

    return ir.infer()

def main(ifrdir,infile='',outfile=''):
    
    ir     = ifr.load(ifrdir)
    inf    = sys.stdin  if infile=='' else open(infile)
    ouf    = sys.stdout if outfile=='' else open(outfile,'w')

    for l in inf:
        row = map(int,l.split())
        dstrs = infer_row(ir,row)
        ouf.write('\t'.join(' '.join(map(str,dstr)) for dstr in dstrs)+'\n')

    if infile  != '': inf.close()
    if outfile != '': ouf.close()
    
coliche.che(main,"""ifrdir
    -i --infile  infile : default stdin
    -o --outfile outfile : default stdout
""")
