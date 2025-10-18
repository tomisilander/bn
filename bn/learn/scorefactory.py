from bn.learn.score import cscorefuncs
from bn.learn.bdeuscore import BDeuScore
from bn.learn.pen_ml_score import PenMLScore
from bn.learn.data import Data              

def getscorer(bdt, scoretype, param, 
              do_cache=True, do_storage=True, cachefile=None):
    # So that one does not need to load the data just to get scorer

    if isinstance(bdt, str):
        bdt = Data(bdt)
 
    if scoretype == 'BDeu':
        return BDeuScore(bdt, param, 
                         do_cache, do_storage, cachefile)
    elif scoretype in cscorefuncs:
        return PenMLScore(bdt,cscorefuncs[scoretype],
                          do_cache, do_storage, cachefile)
    else:
        print('Unknown scoretype', scoretype)

if __name__ == '__main__':
    from argparse import ArgumentParser
    from bn.bn import load as load_bn, BN
    
    def main(args):
        bns:BN = load_bn(args.bnfile)
        scr = getscorer(args.bdtfile, args.goodness, args.ess)
        scr.score_new(bns)
        print (scr.score(), bns.arcs())

    parser = ArgumentParser(description='Learn a Bayesian Network from data')
    parser.add_argument('bnfile',type=str, help='bn file')
    parser.add_argument('bdtfile',type=str, help='data file')
    parser.add_argument('-g', '--goodness', type=str, choices=['BDeu','fNML','AIC','BIC'], default='BDeu', help='score type')
    parser.add_argument('-e', '--ess', type=float, default=1.0, help='effective sample size')
    parser.add_argument('-m', '--cachefile', type=str, help='local scores')

    main(parser.parse_args())

