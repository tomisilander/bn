import bn.bn
from eqvnets import skeleton
from coliche import che

def main(bnfile1, bnfile2):
    bns1 = bn.bn.load(bnfile1)
    bns2 = bn.bn.load(bnfile2)
    fix1, free1 = skeleton(bns1)
    fix2, free2 = skeleton(bns2)

    # print map(frozenset,free1)
    samefree = frozenset(map(frozenset, free1)) == frozenset(map(frozenset, free2))
    print int(fix1 == fix2 and samefree)
    return

che(main,"""bnfile1; bnfile2""")
