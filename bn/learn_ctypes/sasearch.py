#!/usr/bin/env python
import bnsearch
import math, random, time, greedysearch, operator

def find_initial_temperature(bn, sc):

    def it_accept(n,sss):
        d = n - sss["curr_score"]
        if d < 0:
            sss["dsum"] += d
            sss["k"] += 1
        return True
    
    it_step = bnsearch.stepper_f(bnsearch.acts, operator.__gt__, it_accept)
    it_stop = bnsearch.stopper_f(5000)
    isss = {"k":0, "dsum":0.0}
    isss.update(bnsearch.initial_search_status(bn, sc))
    bnsearch.localsearch(isss, it_step, it_stop)

    return isss["dsum"] / isss["k"] / math.log(0.8)


if __name__ == '__main__':
    import sys
    
    def sa_accept(n,sss):
        c = sss["curr_score"]
        wp = math.exp((n-c)/sss["t"])
        apt = n > c or random.uniform(0,1) < wp
        return apt
    
    sa_step = bnsearch.stepper_f(bnsearch.acts, operator.__gt__, sa_accept)

    def sa_stop(sss):
        endtime = sss["endtime"]
        currtime = time.time()
        lefttime = endtime - currtime
        sss["t"] = sss["t0"] * lefttime / searchtime # update temperature
        return currtime >= endtime

    bn, sc = bnsearch.sys2bnscr()
    searchtime = int(sys.argv[4])
    endtime = time.time() + searchtime               
    t0 = find_initial_temperature(bn, sc)

    isss = {"searchtime":searchtime, "endtime":endtime, "t0":t0, "t":t0}
    isss.update(bnsearch.initial_search_status(bn, sc))

    bnsearch.localsearch(isss, sa_step, sa_stop)

    print isss["best_score"], isss["best_bn"].arcs()
