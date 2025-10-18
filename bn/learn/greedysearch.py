#!/usr/bin/env python
import sys
import operator
import bn.learn.bnsearch as bnsearch

def greedysearch(bn, scr, iters, cstr=None):
    gr_better = operator.__gt__

    def gr_accept(n,sss):
        return n > sss["curr_score"]
    
    gr_step = bnsearch.stepper_f(bnsearch.acts, gr_better, gr_accept, cstr)
    gr_stop = bnsearch.stopper_f(iters)
    gr_isss = bnsearch.initial_search_status(bn,scr)
    return bnsearch.localsearch(gr_isss, gr_step, gr_stop)
    

if __name__ == '__main__':
    bn, scr = bnsearch.sys2bnscr()
    greedysearch(bn,scr,int(sys.argv[4]))
    print (scr.score(), bn.arcs())
