#!/usr/bin/env python
# import cycheck

from typing import Dict

class BN:
    def __init__(self, varc, arcs=[], do_pic = True):
        # self.valcs = tuple(valcounts)
        self.varc = varc
        self.arcset = set()
        self.parentsets = [set() for v in self.vars()]
        self.childsets  = [set() for v in self.vars()]
        self.path_in_counts  = [{} for v in self.vars()]
        
        for a in arcs: 
            self.addarc(a, do_pic = False)
        self.picall()

    def copy(self):
        new_bn = BN(self.varc, do_pic=False)
        new_bn.arcset = self.arcset.copy()
        new_bn.parentsets = list(map(set.copy, self.parentsets))
        new_bn.childsets  = list(map(set.copy, self.childsets))
        new_bn.path_in_counts = list(map(dict.copy, self.path_in_counts))
        return new_bn
        
    def addarc(self, arc, do_pic = True):
        (v1,v2) = arc
        #print arc, self.ancestors(v1), 'pre1'
        #print self.arcs(),'pre2'
        #print self.parents(v2), 'pre3'
        
        self.arcset.add(arc)
        self.parentsets[v2].add(v1)
        self.childsets[v1].add(v2)
        
        #if  not cycheck.is_dag(self):
        #    print arc
        #    print self.arcs()
        #    raise Exception('what')

        if do_pic: 
            self.pic_add(arc)

        #if  not cycheck.is_dag(self): raise 'what'

        #print 'after adding', arc, 'parents of', v2, 'are', self.parents(v2)

    def delarc(self, arc, do_pic = True):
        (v1,v2) = arc
        self.arcset.remove(arc)
        self.parentsets[v2].remove(v1)
        self.childsets[v1].remove(v2)
        #if  not cycheck.is_dag(self): raise 'what'
        if do_pic: 
            self.pic_del(arc)
        #if  not cycheck.is_dag(self): raise 'what'

    def revarc(self, arc, do_pic = True):
        (v1,v2) = arc
        self.delarc(arc, do_pic)
        self.addarc((v2,v1), do_pic)
    
    def parents(self, v):
        return frozenset(self.parentsets[v])

    def nof_parents(self, v): 
        return len(self.parentsets[v])

    def children(self, v):
        return frozenset(self.childsets[v])

    def nof_children(self, v): 
        return len(self.childsets[v])

    def neighbours(self,v):
        return self.parents(v) | self.children(v)
    
    def is_ancestor_of(self, v, va, use_pic = False):
        return va in self.ancestors(v, use_pic)
        
    def ancestors(self, v, use_pic = False):
        if use_pic:
            return frozenset(self.path_in_counts[v])
        else : # DFS using stack
            ancs = set()
            stack = list(self.parents(v))
            while len(stack)>0:
                v = stack.pop(-1)
                if v not in ancs:
                    ancs.add(v)
                    stack.extend(self.parents(v))
            return frozenset(ancs)

    def descendants(self, v): # DFS : including v
            stack = [v]
            descs = set()
            while len(stack)>0:
                v = stack.pop(-1)
                if v not in descs:
                    descs.add(v)
                    stack.extend(self.children(v))
            return frozenset(descs)

    def nonancestors(self, v, use_pic = False):
        return frozenset(self.vars()) - self.ancestors(v, use_pic)
            
    def mbnodes(self, v):
        partners = (self.parents(c) for c in self.children(v))
        return frozenset((v,)).union(self.neighbours(v), *partners)

    def markovblanket(self,v,do_pic=True):
        mbns = self.mbnodes(v)
        mbarcs = set((v1,v2) for (v1,v2) in self.arcset
                      if v1 in mbns and v2 in mbns)

        return BN(self.varc, mbarcs, do_pic)

    def has_arc(self,a)   : return a in self.arcset
    def arcs(self)   : return frozenset(self.arcset)
    def vars(self)   : return range(self.varc)

    def __eq__(self, other):
        return self.arcs() == other.arcs()
    
    def __neq__(self, other):
        return self.arcs() != other.arcs()

    def cyclarcs_from(self,v):
        return frozenset([(v,v_anc)
                          for v_anc in self.path_in_counts[v].iterkeys()]
                         + [(v,v)])

    def cyclarcs(self) :
        return frozenset([(v,v_anc)
                          for v in self.vars()
                          for v_anc in self.path_in_counts[v].iterkeys()]
                         + [(v,v) for v in self.vars()])

    def dagarcs(self) :
        allvars = set(self.vars())
        s = [(v,v_nonanc)
             for v in self.vars()
             for v_nonanc in allvars - set(self.path_in_counts[v].iterkeys())] 
        return frozenset(set(s) - set([(v,v) for v in self.vars()]))

    def new_dagarcs(self) :
        return self.dagarcs() - self.arcs()

    # PATH_IN_COUNT (pic) handling

    def pic_add(self, edge):
        # v2 decendants pics change
        self.picall(set(self.descendants(edge[1])))

    def pic_del(self, edge):
        # v2 decendants pics change
        # print 'updating pics for', set(self.descendants(v2))
        self.picall(set(self.descendants(edge[1])))

    def pic1(self,v):
        vpic = {}
        for p in self.parents(v):
            vpic[p] = vpic.get(p,0) + 1 # arc from p to v
            ppic:Dict = self.path_in_counts[p]
            for (a,c) in ppic.items():
                vpic[a] = vpic.get(a,0) + c
                
        self.path_in_counts[v] = vpic
        #print 11, v, self.path_in_counts[v]

    # Most of time spent here - consider non-recursive version
    def picup (self, v, unpiced):
        # ensure parents are piced #
        for p in self.parents(v):
            #print v,p, unpiced
            if p in unpiced:
                unpiced.remove(p)
                self.picup(p,unpiced)

        self.pic1(v)
        #print 12, v, self.path_in_counts[v]
    
    def picall(self, init=None):
        unpiced = set(self.vars()) if init is None else init
        while len(unpiced)>0:
            v = unpiced.pop()
            self.picup(v,unpiced)
            
    def save(self, filename):
        f = open(filename, "w")
        print(self.varc, file=f)
        for a in self.arcs():
            print("%d %d" % a, file=f)
        f.close()
        
    def __hash__(self):
        return hash(self.arcs())

def load(filename, do_pic=True):
    f = open(filename)
    varc = int(f.readline())
    return BN(varc, [tuple(map(int, line.split())) for line in f], do_pic)
        

#def check_cycles(bn):
#    reached = [set() for v in bn.vars()]
#    for i in xrange(bn.varc):
#        for (v,s) in enumerate(sets):
#            for c 



if  __name__ == "__main__":
# Test code for creating and manipulating DAGs using the BN class

    def test_bn(use_pic=False):
        # Create a new BN with 3 variables
        bn = BN(3)

        # Add some arcs to the BN
        bn.addarc((0,1), do_pic=use_pic)
        bn.addarc((0,2), do_pic=use_pic)
        bn.addarc((1,2), do_pic=use_pic)

        # Print the nodes and arcs of the BN
        print("Nodes:", bn.vars())
        print("Arcs:", bn.arcs())

        # Get the parents and children of a node
        print("Parents of node 1:", bn.parents(1))
        print("Children of node 0:", bn.children(0))

        # Check if one node is an ancestor of another
        print("Is node 1 an ancestor of node 2?", bn.is_ancestor_of(2, 1, use_pic=use_pic))
        print("Ancestors of node 2?", bn.ancestors(2, use_pic=use_pic))

        # Get the Markov blanket of a node
        mb = bn.markovblanket(1, do_pic=use_pic)
        print("Markov blanket of node 1:", mb.arcs())

        # Save the BN to a file
        bn.save("test_bn.txt")

    # Call the test function
    test_bn(use_pic=False)
    test_bn(use_pic=True)
