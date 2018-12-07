# nsearch takes an initial network and tries to find 
# top N best networks around it at most level steps away.

from itertools import izip, combinations, product
from heapq import heappushpop
from bn.learn.constraints import Constraints
from bn.learn import scorefactory
from bn.learn import nsearch
from bn.util.eqvnets import eqvnets
import bn.learn


if __name__ == '__main__':
    import coliche, bn, os, sys

    def main(bnfile,bdtfile,level,topN,resdir,
             scoretype='BDeu', ess=1.0, constraint_file=""
             ):

        cstrs = Constraints(constraint_file)

        bn0 = bn.bn.load(bnfile)
        nof_vars = bn0.varc
        sc = scorefactory.getscorer(bn.learn.data.Data(bdtfile), scoretype, ess)

        elite =  [(-sys.float_info.max, None)] * topN
        for bne in eqvnets(bn0):
            sc.score_new(bne)
            for s,(bnw,seq) in nsearch.nsearch(bne,sc,level,topN, cstrs):
                if bnw.arcs() not in elite:
                    # print "in", bnw.arcs()
                    weakest = heappushpop(elite,(s,bnw.arcs()))
                    # print "out", weakest

        elite.sort(reverse=True)

        if not os.path.exists(resdir): os.mkdir(resdir)
        i=0
        for (s,bwe) in elite:
            if bwe != None:
                bn.bn.BN(nof_vars, bwe, False).save(os.path.join(resdir,'%d.bn'%i))
                i += 1
                print s

    coliche.che(main, 
    """bnfile; bdtfile; level (int); topN (int); resdir
    -g --goodness scoretype BDeu|fNML|AIC|BIC : default: BDeu
    -e --ess ess (float) : default 1.0
    -c constraint_file : a file with arcs marked with + or -
    """)
