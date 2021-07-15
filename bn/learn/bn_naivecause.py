#!/usr/bin/env pythonfrom itertools import product

# The system is represented as a pair (bn,urcs) where bn contains the
# directed arcs and urcs is a set of undirected arcs represented with
# both (x,y) and (y,x) belonging to urcs. 

def orient(x,y, urcs, bns):
    urcs.remove((x,y))
    urcs.remove((y,x))
    bns.addarc((x,y),do_pic=False)

def deorient(x,y, urcs, bns):
    urcs.add((x,y))
    urcs.add((y,x))
    bns.delarc((x,y),do_pic=False)

def adj(x,y,urcs,bns):
    return ((x,y) in urcs) or (x in bns.parents(y)) or (x in bns.children(y))

# (R1) orient b--c into b->c whenever there is an arrow a->b such that
# a and c are nonadjacent. Explanation: if a and c are nonadjacent
# a->b--c has to be oriented to a->b->c, othewise new v-structure were
# created.

# a->b--c to a->b->c if nonadj(a,c)

def r1(bns,urcs): 
    for (b,c) in urcs:
        for a in bns.parents(b):
            if not adj(a,c,urcs,bns):
                orient(b,c,urcs,bns)
                return True
    return False


# (R2) orient a--b into a->b whenever there is a chain
# a->c->b. Explanation: othewise a directed cycle would be created.

def r2(bns,urcs): 
    for (a,b) in urcs:
        for c in bns.children(a):
            if b in bns.children(c):
                orient(a,b,urcs,bns)
                return True
    return False

# (R3) orient a--b into a->b whenever there is are two chains a--c->b
# and a--d->b such that c and d are non adjacent. Explanation:
# orienting b->a would force orientations c->a and d->a to avoid
# cycles, but this would create a new v-structure c->a<-d.

def r3(bns,urcs): 
    for (a,b) in urcs:
        bps = bns.parents(b)
        for (c,d) in product(bps, bps):
            if c !=d and not adj(c,d,urcs,bns) and (a,c) in urcs and (a,d) in urcs:
                orient(a,b, urcs, bns)
                return True
    return False

# Apply r123 as much as you can
def rorient(bns,urcs):
    while r1(bns,urcs) or r2(bns,urcs) or r3(bns,urcs):
        pass


# undirect non-v-structure arcs from bns
def naivecause(bns):
    # find v-structure arcs
    dirarcs = set()
    for v in bns.vars():
        vps = bns.parents(v)
        for (p1,p2) in product(vps, vps):
            if p1 > p2 and p1 not in bns.neighbours(p2):
                dirarcs.add((p1,v))
                dirarcs.add((p2,v))

    # move v-structure arcs to urcs
    urcs = set()
    for (x,y) in bns.arcs():
        if (x,y) not in dirarcs:
            deorient(x,y,urcs,bns)

    # orient what you can
    rorient(bns,urcs)

    return bns, urcs

def main(bnfile):
    bns = bn.bn.load(bnfile)
    return naivecause(bns)

if __name__ == '__main__':
    import bn, coliche
    
    (bns, urcs) = coliche.che(main,'bnfile')

    for a in bns.arcs():
        print "%d -> %d" % a

    for (u1,u2) in urcs:
        if u1>u2:
            print "%d -- %d" % (u1,u2)
        
