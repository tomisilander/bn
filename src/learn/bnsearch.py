#!/usr/bin/env python
from src.learn.data import Data
from src.bn import BN
from src.learn.scorefactory import getscorer
from src.learn.constraints import Constraints
from random import choice
import time

#import cycheck


def can_addarc(bn, arc):
    (v1, v2) = arc 
    try:
        return v1 != v2 and not bn.is_ancestor_of(v1, v2, use_pic=True)
    except:
        print (v1, v2, bn.arcs())
        raise

def can_revarc(bn, arc):
    (v1, v2) = arc
    v2sibs = set(bn.children(v1))
    v2sibs.remove(v2)
    v2ancs = bn.ancestors(v2,use_pic=True)
    return (len(v2sibs & v2ancs) == 0)


class NoAction(Exception): 
    pass

def try_add(bn, cache = None, cstrs=None, maxtries = 20):

    for t in range(maxtries) :
        (v1, v2) = a = (choice(bn.vars()), choice(bn.vars()))
        if a in bn.arcs() : 
            continue
        if cstrs and a in cstrs.no : 
            continue

        if cache and cache[v2]: # only try new things - why ???
            v2ps = set(bn.parents(v2))
            v2ps.add(v1)
            if frozenset(v2ps) in cache[v2]:
                # print "chit for add", v2, v2ps
                continue

        if can_addarc(bn, a) :
            bn.addarc(a, False) # NB. needs commit to update pic
            return a, (v2,)
    raise NoAction

def try_del(bn, cache=None, cstrs=None, maxtries = 20):
    if len(bn.arcs()) == 0: 
        raise NoAction

    for t in range(maxtries) :

        (v1, v2) = a = choice(tuple(bn.arcs()))
        if cstrs and a in cstrs.must : 
            continue

        if cache and cache[v2]: # only try new things - why ???
           v2ps = set(bn.parents(v2))
           v2ps.remove(v1)
           if frozenset(v2ps) in cache[v2]:
               # print "chit for del", v2, v2ps
               continue

        bn.delarc(a, do_pic = False) # NB. needs commit to update pic
        return a, (v2,)
    raise NoAction

def try_rev(bn, cache = None, cstrs=None, maxtries = 20):
    if len(bn.arcs()) == 0: 
        raise NoAction

    for t in range(maxtries):

        (v1, v2) = a = choice(tuple(bn.arcs()))
        if cstrs and (a in cstrs.must or (v2,v1) in cstrs.no): 
            continue

        if cache and cache[v1] and cache[v2]: # why only try new things??
            v2ps = set(bn.parents(v2))
            v2ps.remove(v1)
            v1ps = set(bn.parents(v1))
            v1ps.add(v2)
            if frozenset(v1ps) in cache[v1] \
                   and frozenset(v2ps) in cache[v2]:
                continue

        if can_revarc(bn,a):
            bn.revarc(a, do_pic=False)
            # print "reversing", a, "in", bn.arcs()
            # map(bn.ancestors, bn.vars())
            return a, (v1,v2)
    raise NoAction


def fix_add(bn, arc): bn.pic_add(arc)
def fix_del(bn, arc): bn.pic_del(arc)
def fix_rev(bn, arc): bn.picall(set(bn.descendants(arc[1])))

def cancel_add(bn, arc): bn.delarc(arc, do_pic=False)
def cancel_del(bn, arc): bn.addarc(arc, do_pic=False)
def cancel_rev(bn, arc): 
    (v1,v2) = arc
    bn.revarc((v2,v1), do_pic=False)

acts ={"tryacts": {'add' : try_add,   'del' : try_del,   'rev' : try_rev},
       "commits": {'add' : fix_add,   'del' : fix_del,   'rev' : fix_rev} ,
       "cancels": {'add' : cancel_add,'del' : cancel_del,'rev' : cancel_rev}
       }

def score_arcs(bn,scr):
    sarcs = []
    refscore = scr.score()
    for a in bn.arcs():
        v = a[1]
        bn.delarc(a,False)
        scr.storevar(v)
        scr.score_new_v(bn, v)
        sarcs.append((scr.score() - refscore, a))
        scr.restore()
        bn.addarc(a, False)
    sarcs.sort()
    return sarcs

############ LOCAL SEARCH #############
#
# Local search starts somewhere, randomly selects an action
# to change the current candidate, accepts the change by some
# policy and stops by some policy.
# The status of the search is maintained in a hashtable
# containing current bn, scr for it, current_score
# and best_bn, best_score. Also some summary variables
# are recorded: time_without_finding a legal action,
# time without making any improvement, time without accepting
# any actions, number of iterations.

def stopper_f(max_iters     = None,
              limit_no_acts = None,
              limit_no_impr = None,
              limit_no_acps = None,
              max_time      = None):

    end_time = None
    if max_time is not None:
        end_time = time.time() + max_time

    def stopf(search_status):
        iter_crit = max_iters     and search_status["iters"]    >=max_iters
        acts_crit = limit_no_acts and search_status["t_no_acts"]>=limit_no_acts
        impr_crit = limit_no_impr and search_status["t_no_impr"]>=limit_no_impr
        acps_crit = limit_no_acps and search_status["t_no_acps"]>=limit_no_acps
        time_crit = max_time is not None and time.time() >= end_time

        return iter_crit or acts_crit or impr_crit or acps_crit or time_crit

    return stopf

def stepper_f(actions, better, accept, cstrs=None):

    if not cstrs:
        cstrs = Constraints()

    def stepf(search_status):
        scr = search_status["scr"]
        bn =  search_status["curr_bn"]

        #print 'stepin', bn.arcs()
        #for v in bn.vars(): print v, bn.path_in_counts[v]

        #if not cycheck.is_dag(search_status["curr_bn"]): raise Exception('cyc')
        #if not cycheck.is_dag(search_status["best_bn"]): raise Exception('cyc')

        search_status["iters"] += 1
        try:
            aname, action = choice(tuple(acts["tryacts"].items()))
            changes, avars = action(bn, cstrs=cstrs)
            search_status["t_no_acts"] = 0

            for avar in avars: 
                scr.storevar(avar)

            for avar in avars: 
                scr.score_new_v(bn, avar)

            new_score = scr.score()

            if better(new_score, search_status["best_score"]):
                search_status["best_score"] = new_score
                search_status["best_bn"]   = bn.copy()
                search_status["t_no_impr"] = 0
            else:
                search_status["t_no_impr"] += 1

            if accept(new_score, search_status):
                search_status["curr_score"] = new_score
                scr.clearstore()
                acts["commits"][aname](bn, changes)
                search_status["t_no_acps"] = 0
            else :
                search_status["t_no_acps"] += 1
                acts["cancels"][aname](bn,changes)
                scr.restore()

        except NoAction :
            search_status["t_no_acts"] += 1

        #if not cycheck.is_dag(search_status["curr_bn"]):
        #    print aname, changes, avars, bn.arcs()
        #    for v in bn.vars(): print v, bn.path_in_counts[v]
        #    raise Exception('cyc')
        #if not cycheck.is_dag(search_status["best_bn"]):
        #    raise Exception('cyc')

    return stepf


def initial_search_status(bn, scr):
    curr_score = scr.score()
    return {"scr" : scr,                # scorer
            "curr_bn" : bn,
            "curr_score" : curr_score,  # actual score
            "best_bn" : bn.copy(),
            "best_score" : curr_score,
            "iters" : 0,
            "t_no_acts" : 0,
            "t_no_acps" : 0,
            "t_no_impr" : 0}

def localsearch(search_status, stepping, stopping):
    while True :
        stepping(search_status)
        if stopping(search_status) : 
            break

# So often we also want the scorer so let us allow that

def empty_net(bdtfile, scoretype=None, params=None, cachefile=None):
    data  = Data(bdtfile)
    bn = BN(data.nof_vars())
    if scoretype is not None:
        sc = getscorer(data, scoretype, params, cachefile=cachefile)
        sc.score_new(bn)
        return (bn, sc)
    else:
        return bn
