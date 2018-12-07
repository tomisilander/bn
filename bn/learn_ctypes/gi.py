#!/usr/bin/python

import bnsearch
import coliche

def main(bdtfile, ess=1.0, outfile=None):

    bn, sc = bnsearch.empty_net(bdtfile, ess)

    if outfile:
        bn.save(outfile)

    print sc.score()

if __name__ == '__main__':
    
    coliche.che(main,
                ''' bdtfile;
                -e --ess ess (float) : default 1.0
                -o outfile : file to save the model found''')
    
