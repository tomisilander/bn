import bn.bn
from eqvnets import vstructs
from coliche import che

def main(bnfile1, vdfile=None):
    bns1 = bn.bn.load(bnfile1)
    for (v,p1,p2) in vstructs(bns1):
        print v, p1, p2

# add support to vdfile
che(main,"""bnfile1""")
