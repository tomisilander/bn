from bn.infer.pot import Potential
from bn.vd import load as vdload
from bn.model.bnmodel import load as bnmload
from bn.infer.ifr import load as ifrload
from bn.util.fishim import lognorm
from itertools import combinations_with_replacement
from itertools import chain
import array
import os
import sys


def gen_subsets(xs):
    sxs = sorted(xs)
    if gen_subsets.use_just_one_set:
        yield tuple(sxs)
        return

    nof_xs = len(xs)
    if nof_xs == 0:
        yield()
        return
    masks = [1 << o for o in range(nof_xs)]

    for i in range((1 << nof_xs)-1, -1, -1):
        yield tuple(p for (p, m) in zip(sxs, masks) if i & m)


def gen_subsets_with_fix(xs, fix):
    fixtuple = (fix,)
    for ss in gen_subsets(xs):
        yield tuple(sorted(chain(ss, fixtuple))), ss


def get_cfgextractors(i, bnm):

    def build_cfgx(famsubset, parsubset):
        return lambda d: (tuple(map(d.__getitem__, famsubset)),
                          tuple(map(d.__getitem__, parsubset)))
    return [build_cfgx(famsubset, parsubset)
            for famsubset, parsubset in
            gen_subsets_with_fix(bnm.bn.parents(i), i)]


def gen_subpots(valcs, bnm, ifr, varix):
    parents = list(bnm.bn.parents(varix))
    family = parents + [varix]
    nof_parents = len(parents)

    pots = [None]*(nof_parents+1)

    for famsubset, parsubset in gen_subsets_with_fix(parents, varix):
        nof_subpars = len(parsubset)
        if nof_subpars == nof_parents:
            cpot = ifr.pots[ifr.vclqs[varix]]
            subpot_p = (cpot >> Potential(parents, valcs, 0.0)).normalize()
            subpot_f = (cpot >> Potential(family, valcs, 0.0)).normalize()
        else:
            subpot_p = pots[nof_subpars+1] >> Potential(parsubset, valcs, 0.0)
            subpot_f = pots[nof_subpars+1] >> Potential(famsubset, valcs, 0.0)
        yield (subpot_f, subpot_p)
        pots[nof_subpars] = subpot_f


def get_parsetscores(i, resdir, bnm):
    if len(bnm.bn.parents(i)) == 0 or resdir is None:
        return [1.0]

    statinfo = os.stat(os.path.join(resdir, str(i)))
    fsize = statinfo.st_size
    nof_nums = 1 << (bnm.bn.varc-1)
    bits_per_num = fsize / nof_nums
    typecode = 'f' if bits_per_num == 4 else 'd'
    scores = array.array(typecode)

    f = open(os.path.join(resdir, str(i)))
    scores.fromfile(f, nof_nums)
    psscores = [scores[sum(1 << p if p < i else 1 << (p-1) for p in parsubset)]
                for parsubset in gen_subsets(bnm.bn.parents(i))]

    return lognorm(psscores)


def vrsims(x, y, cfgxss, psscoress, potss):
    for (cfgxs, psscores, pots) in zip(cfgxss, psscoress, potss):
        for (cfgx, psscore, pot) in zip(cfgxs, psscores, pots):
            (xf, xp), (yf, yp) = map(cfgx, (x, y))
            # print(psscore)
            # print(xf, xp, yf, yp)
            if xp != yp:
                yield 0.0
            else:  # parents match
                pp = pot[1][xp]
                # print('pp', pp)
                if xf != yf:
                    yield -psscore/pp
                else:
                    pxvl = pot[0][xf] / pot[1][xp]
                    # print("pxvl", pxvl)
                    yield psscore*(1-pxvl)/pxvl/pp
            # print('END SUBSET')
        # print('END VAR')


def sim(x, y, cfgextractors, parsetscores, potss):
    return sum(vrsims(x, y, cfgextractors, parsetscores, potss))


def main(vdfile, bnmfile, ifrdir, resdir=None, cix=None, matrix=False):
    valcs = vdload(vdfile)
    bnm = bnmload(bnmfile, valcs)
    ifr = ifrload(ifrdir)

    gen_subsets.use_just_one_set = resdir is None
    parsetscores = [get_parsetscores(i, resdir, bnm) for i in bnm.bn.vars()]
    potss = [list(gen_subpots(valcs, bnm, ifr, i)) for i in bnm.bn.vars()]
    cfgextractors = [get_cfgextractors(i, bnm) for i in bnm.bn.vars()]

    dats = [map(int, l.split()) for l in sys.stdin]
    combs = combinations_with_replacement(enumerate(dats), 2)

    if matrix:
        K = [[0.0]*bnm.bn.varc for i in bnm.bn.vars()]
        for((i1, d1), (i2, d2)) in combs:
            K[i1][i2] = K[i2][i1] = sim(d1, d2, cfgextractors, parsetscores, potss)

        for i in bnm.bn.vars():
            print(' '.join(map(str, K[i])))
    else:
        for((i1, d1), (i2, d2)) in combs:
            print(i1, i2, sim(d1, d2, cfgextractors, parsetscores, potss))


if __name__ == '__main__':
    from coliche import che
    che(main, """vdfile; bnmfile; ifrdir
    -r --resdir resdir: directory to get the subsetscores
    -c --cix cix (int) : class index counting from 0 : default None
    -m --matrix : print in matrix form""")
