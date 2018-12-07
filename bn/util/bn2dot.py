#!/usr/bin/python
import coliche, os
import bn.bn

def bn2dot(bnfile, outfile, vdfile=None, loners=False, center=None,
           awfile=None):
    # give None to outfile to get string back

    dotbuffer = []

    bns = bn.bn.load(bnfile, False)
    varc = bns.varc
    arcs = bns.arcs()

    names = vdfile \
            and list(l.split("\t",1)[0] for l in file(vdfile)) \
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
        for l in file(awfile):
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
        file(outfile,"w").write(dotstr)
    else:
        return dotstr
        

if __name__ == "__main__":
    coliche.che(bn2dot,
                """bnfile; outfile
                -n --vdfile vdfile     : to add names to the picture
                -l --loners            : show orphan nodes too
                --mb center            : draw only markov blanket of center
                -w --arcweights awfile : draw arcweights
                """)
