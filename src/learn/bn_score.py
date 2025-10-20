#!/usr/bin/env python
import bn.bn, data, scorefactory
import coliche

def main(bnfile, bdtfile, scoretype='BDeu', ess=1.0, cachefile=None):

    bns = bn.bn.load(bnfile, do_pic=False)
    bdt = data.Data(bdtfile)
    sc = scorefactory.getscorer(bdt,scoretype,ess,cachefile=cachefile)
    sc.score_new(bns)
    print sc.score()

if __name__ == '__main__':
    
    coliche.che(main,
                ''' bnfile; bdtfile
                -g --goodness scoretype BDeu|fNML|AIC|BIC : default: BDeu
                -e --ess ess (float) : default 1.0
                -m --cachefile cachefile: local scores
''')
