#!/usr/bin/env python3
import sys, os
import typer
from typing import Optional

def bn2dot(bnfile, outfile, vdfile=None, loners=False, center=None,
           awfile=None):
    # give None to outfile to get string back

    dotbuffer = []

    bns = bn.bn.load(bnfile, False)
    varc = bns.varc
    arcs = bns.arcs()

    names = vdfile \
            and list(l.split("\t",1)[0] for l in open(vdfile)) \
            or map(str, range(varc))

    lonerset = range(varc)
    
    if center:
        try:
            center = int(center)
        except:
            center = names.index(center)

    showvars = bns.mbnodes(center) if center != None else set(range(varc))

    aws = {}
    if awfile != None:
        for l in open(awfile):
            t = l.split()
            x,y = map(int,t[0:2])
            w = float(t[2])
            aws[(x,y)]=w


    dotbuffer.append("digraph BN {")

    for x,y in arcs:
        if x in showvars and y in showvars:
            wstr = ''
            if (x,y) in aws:
                wstr = ' [label="%.2g"]' % aws[(x,y)]

            nx, ny = names[x], names[y]
            dotbuffer.append('  "%s" -> "%s"%s;' % (nx, ny,wstr))

        if x in lonerset:
            lonerset.remove(x)
        if y in lonerset:
            lonerset.remove(y)

    if loners:
        for l in sorted(lonerset):
            if l in showvars: dotbuffer.append('"%s";' % names[l])
            
    dotbuffer.append("}")
    dotstr = '\n'.join(dotbuffer)
    if outfile:
        open(outfile,"w").write(dotstr)
    else:
        return dotstr
        

def main(bnfile: str, outfile: Optional[str] = None, vdfile: Optional[str] = None,
         loners: bool = False, center: Optional[str] = None, awfile: Optional[str] = None):
    bn2dot(bnfile, outfile, vdfile, loners, center, awfile)


if __name__ == "__main__":
    typer.run(main)
