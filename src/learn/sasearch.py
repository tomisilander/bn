#!/usr/bin/env python
import bnsearch, sigpool
import math, random, time as tim, greedysearch, operator
from constraints import Constraints

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
    import coliche
    
    def sa_accept(n,sss):
        c = sss["curr_score"]
        wp = math.exp((n-c)/sss["t"])
        apt = n > c or random.uniform(0,1) < wp
        return apt
    
    sa_step = bnsearch.stepper_f(bnsearch.acts, operator.__gt__, sa_accept)
    searchtime = 0

    def sa_stop(sss):
        endtime = sss["endtime"]
        currtime = tim.time()
        lefttime = endtime - currtime
        sss["t"] = sss["t0"] * lefttime / searchtime # update temperature
        return currtime >= endtime


    def main(bdtfile, scoretype='BDeu',
             ess=1.0, time=None, iters=None,
             outfile=None, constraint_file="", startbn = None,
             cachefile=None):

        global searchtime

        cstrs = Constraints(constraint_file)

        if startbn != None:
            bn = bnmodule.load(startbn,do_pic=False)
            sc = scorefactory.getscorer(bdtfile,scoretype,ess,
                                        cachefile=cachefile)
        else:
            bn, sc = bnsearch.empty_net(bdtfile, scoretype, ess, 
                                        cachefile=cachefile)
    
            if constraint_file: # should check if compatible with start
                for a in cstrs.must:
                    bn.addarc(a)

                    sc.score_new(bn)
                    bn.picall()
     
        searchtime = sigpool.str2time(time)
        endtime = tim.time() + searchtime               
        t0 = find_initial_temperature(bn, sc)

        isss = {"searchtime":searchtime, "endtime":endtime, "t0":t0, "t":t0}
        isss.update(bnsearch.initial_search_status(bn, sc))

        bnsearch.localsearch(isss, sa_step, sa_stop)

        if outfile:
            isss["best_bn"].save(outfile)

        print(isss["best_score"])

    coliche.che(main,
                ''' bdtfile;
                -g --goodness scoretype BDeu|fNML|AIC|BIC : default: BDeu
                -e --ess ess (float) : default 1.0
                -t time : like -t '4d 3h 5m 5[s]' (default till SIGUSR2)
                -i --iters iters (int) :number of iterations (default infinite)
                -c constraint_file : a file with arcs marked with + or -
                -o outfile : file to save the model found
                -s --start startbn : file to start search from
                -m --cachefile cachefile: local scores
                ''')
