#!/usr/bin/env python
# Check that all forsts have same score

if __name__ == '__main__':
    import coliche
    import bnsearch
    import bestforests

    def main(bdtfile, ess = 1.0, outfile=None, constraint_file=""):
        bn, sc = bnsearch.empty_net(bdtfile, ess)
        bestforests.kruskal(bn,sc)
        sc.score_new(bn)
        print sc.score()
        for forest in bestforests.Forest(bn):
            sc.score_new(forest)
            print sc.score()
            
    coliche.che(main,
                ''' bdtfile;
                -e --ess ess (float) : default 1.0
                ''')
