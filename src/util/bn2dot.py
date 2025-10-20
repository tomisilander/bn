#!/usr/bin/env python3
import typer
from src.bn import load as bnload

app = typer.Typer()

def bn2dot(bnfile:str, outfile:str|None=None, 
           vdfile:str|None=None, loners=False, center:int|str|None=None,
           awfile:str|None=None):

    # give None to outfile to get string back

    dotbuffer = []

    bns = bnload(bnfile, False)
    varc = bns.varc
    arcs = bns.arcs()

    names = list(line.split("\t",1)[0] for line in open(vdfile)) if vdfile \
            else list(map(str, range(varc)))

    lonerset = set(range(varc))

    ctr = -666
    if center is not None:
        if isinstance(center, int): 
            ctr:int = center
        else: 
            ctr:int = int(center) if str.isnumeric(center) else names.index(center)

    showvars = bns.mbnodes(ctr) if center is not None else set(range(varc))

    aws = {}
    if awfile is not None:
        for line in open(awfile):
            t = line.split()
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
        dotbuffer.extend([f'"{names[line]};"' 
                          for line in sorted(lonerset) 
                          if line in showvars])
            
    dotbuffer.append("}")

    dotstr = '\n'.join(dotbuffer)
    if outfile:
        open(outfile,"w").write(dotstr)
    else:
        return dotstr
        

@app.command("bn2dot")
def main(bnfile: str, outfile: str|None = None, vdfile: str|None = None,
         loners: bool = False, center: str|None = None, awfile: str|None = None):
    bn2dot(bnfile, outfile, vdfile, loners, center, awfile)


if __name__ == "__main__":
    app()
