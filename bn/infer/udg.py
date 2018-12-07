#!/usr/bin/python

class Udg:

    """
    For building a quantified joint tree for a Bayesian network
    we need an undiregred graph with an ability to add nodes and edges.
    Also finding neighbours of any node is needed.

    Nodes are any object than can be sorted.
    Edges are not explicitly stored, but as an input they are taken to
    be pairs of nodes and as an output they are ordered pairs.
    """
    
    def __init__(self, nodes=[], edges=[]):
        self.ns = set()
        self.neighboursets = {}
        self.addnodes(nodes)
        self.addedges(edges)
            
    def copy(self):
        return Udg(self.nodes(), self.edges())
    
    def nodes(self):
        return iter(self.ns)

    def nof_nodes(self):
        return len(self.ns)

    def addedge(self, x, y):
        self.neighboursets[x].add(y)
        self.neighboursets[y].add(x)

    def addedges(self, es):
        for e in es:
            self.addedge(*e)

    def neighbours(self, n):
        return iter(self.neighboursets[n])

    def nof_neighbours(self, n):
        return len(self.neighboursets[n])

    def edges(self):
        for n, nns in self.neighboursets.iteritems():
            for nn in nns:
                if n < nn:
                    yield (n, nn)

    def nof_edges(self):
        i = -1
        for i,e in enumerate(self.edges()):
            pass
        return i+1

    def delnode(self, n):
        for nn in self.neighbours(n):
            self.neighboursets[nn].remove(n)
        del self.neighboursets[n]
        self.ns.remove(n)

    def delnodes(self, ns):
        for n in ns:
            self.delnode(n)

    def addnode(self,n):
        self.ns.add(n)
        self.neighboursets[n] = set()

    def addnodes(self, ns):
        for n in ns:
            self.addnode(n)

    def join_with(self, other, e=None): # for join tree construction
        self.ns.update(other.ns)
        self.neighboursets.update(other.neighboursets)
        if e: self.addedge(*e)

    def save(self, filename):
        f = file(filename, "w")
        print >>f, len(list(self.nodes()))
        for (x,y) in self.edges():
            print >>f, x, y
        f.close()

def load(filename):
    f = file(filename)
    nof_nodes = int(f.readline())
    return Udg(xrange(nof_nodes), [map(int, l.split()) for l in f])

def save(g, filename):
    g.save(filename)
