#!/usr/bin/env python3

class Orient:

    def __init__(self, nof_vars, fix, free):
        
        self.fix  = fix.copy()
        self.free = free.copy()
        self.arcs = arcs = fix | free
        self.dirchild  = [set() for i in range(nof_vars)]
        self.dirparent = [set() for i in range(nof_vars)]
                 
        for (a, b) in fix:
            self.dirchild[a].add(b)
            self.dirparent[b].add(a)
        
        self.naivedo()

    def naivedo(self):
        cont = 1
        while cont:
            cont = 0
            for (b, c) in self.free.copy():
                if   self.R1(b, c): cont = 1
                elif self.R1(c, b): cont = 1
                elif self.R2(b, c): cont = 1
                elif self.R2(c, b): cont = 1
                elif self.R3(b, c): cont = 1
                elif self.R3(c, b): cont = 1
                elif self.R4(b, c): cont = 1
                elif self.R4(c, b): cont = 1


    def direct(self, a, b):
        if (a,b) in self.free:
            self.free.remove((a, b))
        else:
            self.free.remove((b, a))
        self.fix.add((a, b))
        self.dirchild[a].add(b)
        self.dirparent[b].add(a)

    def adj(self, a, b):
        return (a,b) in self.arcs or (b,a) in self.arcs

    def isundir(self, a, b):
        return (a,b) in self.free or (b,a) in self.free


    def R1(self, b, c):
        for a in self.dirparent[b]:
            if not self.adj(a, c):
                self.direct(b, c)
                return 1
        
    def R2(self, a, b):
        for c in self.dirchild[a]:
            if b in self.dirchild[c]:
                self.direct(a, b)
                return 1        

    def R3(self, a, b):
        
        cdlist = [x for x in self.dirparent[b]
                  if self.isundir(a, x)]
    
        for ci in range( len(cdlist) ):
            for di in range( ci+1, len(cdlist) ):
                c, d, = cdlist[ci], cdlist[di]
                if not self.adj(c, d):
                    self.direct(a, b)
                    return 1

    def R4(self, a, b):
        for d in self.dirparent[b]:
            for c in self.dirparent[d]:
                if self.adj(c,a) and not self.adj(c,b):
                    self.direct(a,b)
                    return 1