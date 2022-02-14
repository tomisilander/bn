import sys

class Constraints:

      def __init__(self, fn=""):
            self.must = set()
            self.no   = set()

            if fn != "":
                  self.load(fn)

      def load(self, fn):
            for l in open(fn):
                  x,a,b = l.split()
                  if x == "+":
                        s = self.must
                  elif x == "-":
                        s = self.no
                  else :
                        print >>sys.stderr, "+/- expected, found %s." % x
                  s.add((int(a),int(b)))

      def save(self, fn):
            with open(fn, "w") as f:
                  for a in self.must:
                        f.write('+ %d %d\n' % a)
                  for a in self.no:
                        f.write('- %d %d\n' % a)
 
      def empty(self): return len(self.must)+len(self.no) == 0

      def satisfied(self, arcs):
            return (self.must<=arcs) and len(arcs & self.no)==0

      def violated(self, arcs):
            return not self.satisfied(arcs)
