class Constraints:
      def __init__(self, fn=""):
            self.must = set()
            self.no   = set()

            if fn:
                  for l in file(fn):
                        a,b,x = l.split()
                        if x == "+":
                              s = self.must
                        elif x == "-":
                              s = self.no
                        else :
                              print >>sys.stderr, "+/- expected, found %s." % x
                        s.add((int(a),int(b)))
