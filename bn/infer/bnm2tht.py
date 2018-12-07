import utils
def tht(bnm):
    for i in bnm.bn.vars():
        vci = bnm.valcounts[i]
        uni = [1.0/vci] * vci
        thi = bnm.thti(i)
        yield utils.sparse_func(thi,uni)
