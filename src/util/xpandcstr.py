#!/usr/bin/env python3
import sys
from typing import Dict, Set, Tuple
import typer
from bn import vd

app = typer.Typer()

@app.command("xpandcstr")
def main(vdfile:str):
    names:tuple[str,...] = vd.varnames(vdfile)
    names2ixs = {n:i for i,n in enumerate(names)}

    cstrs:Dict[str,Tuple[Set,Set]] = {name : (set(),set()) for name in names}

    for line in sys.stdin:
        ls = line.strip()
        if ls == '' or line.startswith('#'): 
            continue
        op,f,t = ls.split()
        
        # print op,f,t
        # remove any inline comment that got attached to t, and strip quotes/commas/whitespace
        t = t.split('#', 1)[0].strip()
        f = f.strip().strip(',').strip('"\'' )
        t = t.strip().strip(',').strip('"\'' )
        if f == '' or t == '':
            continue
        fis = map(names2ixs.get,f)
        tis = map(names2ixs.get,t)

        # print op,fis,tis

        for f in fis:
            assert isinstance(f, int)
            # assert f < len(names)
            (sf_must, sf_nope) = cstrs.get(names[f], (set(), set()))
            for t in tis:
                if f == t: 
                    continue

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
                    print('Whaaat?')

    for (fn, cs) in cstrs.items():
        fi = names.index(fn)
        for t in cs[0]:
            print ('+', fi, t)
        for t in cs[1]:
            print ('-', fi, t)


if __name__ == "__main__":
    app()
