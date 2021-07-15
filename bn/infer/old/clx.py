#!/usr/bin/env python
def clx(wcx):
    return [clq for (w,clq) in wcx]
    
def load(clxfile): 
    return [set(map(int,l.split())) for l in file(clxfile)]

def save(clx, clxfile):
    clxf = file(clxfile, "w")
    for clq in clx:
        print >>clxf, " ".join(map(str, clq))
    clxf.close()
