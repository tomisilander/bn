import sys

class Constraints:
      def __init__(self, fn=""):
            self.must = set()
            self.no   = set()

            if fn:
                  for l in file(fn):
                        x,a,b = l.split()
                        if x == "+":
                              s = self.must
                        elif x == "-":
                              s = self.no
                        else :
                              print >>sys.stderr, "+/- expected, found %s." % x
                        s.add((int(a),int(b)))

      def empty(self): return len(self.must)+len(self.no) == 0

      def satisfied(self, arcs):
            return (self.must<=arcs) and len(arcs & self.no)==0

      def violated(self, arcs):
            return not self.satisfied(arcs)
