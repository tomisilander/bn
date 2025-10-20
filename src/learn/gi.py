#!/usr/bin/env python
import bnsearch

def main(bdtfile, scoretype='BDeu', ess=1.0, outfile=None, cachefile=None):

    bn, sc = bnsearch.empty_net(bdtfile, scoretype, ess, cachefile=cachefile)

    if outfile:
        bn.save(outfile)

    print sc.score()

if __name__ == '__main__':

    import coliche

    coliche.che(main,
                ''' bdtfile;
                -g --goodness scoretype BDeu|fNML|AIC|BIC : default: BDeu
                -e --ess ess (float) : default 1.0
                -o outfile : file to save the model found
                -m --cachefile cachefile: local scores
''')

