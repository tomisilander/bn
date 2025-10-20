#!/dev/bin/python

from bn_naivecause import naivecause, rorient

# Recursively produce all structures equivalent to bn 
def eqvclasses(bn, urcs=None):

    if urcs == None:
        bns = bn.copy()
        bn,urcs  = naivecause(bns)

    if len(urcs) == 0:
        yield bn
    else:
        (x,y) = urcs.pop()
        urcs.remove((y,x))

        # yield bns with (x,y) arc
        nbn=bn.copy()
        nurcs=urcs.copy()
        nbn.addarc((x,y))
        rorient(nbn,nurcs) 
        for b in eqvclasses(nbn,nurcs):
            yield b

        # yield bns with (x,y) arc
        nbn=bn.copy()
        nurcs=urcs.copy()
        nbn.addarc((y,x))
        rorient(nbn,nurcs)
        for b in eqvclasses(nbn,nurcs):
            yield b
