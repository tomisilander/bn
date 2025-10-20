#!/usr/bin/env python
from ctypes import *

from bn import BN
from score import Score
from constraints import Constraints
from random import choice
import time
import vd
import coliche


def can_addarc(bn, (v1, v2)):
    try:
        return v1 != v2 and not bn.is_ancestor_of(v1, v2, True)
    except:
        print v1, v2, bn.arcs()
        raise
    
def can_revarc(bn, (v1, v2)):
    v2sibs = set(bn.children(v1))
    v2sibs.remove(v2)
    nof_sancs = sum([bn.is_ancestor_of(v2, v2s, True)
                     for v2s in v2sibs], 0)
    return (nof_sancs == 0)


class NoAction(Exception): pass

def try_add(bn, cache = None, cstrs=None):
    maxtries = 20
    for t in xrange(maxtries) :
        (v1, v2) = a = (choice(bn.vars()), choice(bn.vars()))
        if a in bn.arcs() : continue
        if cstrs and a in cstrs.no : continue
        
        if cache and cache[v2]:
            v2ps = set(bn.parents(v2))
            v2ps.add(v1)
            if frozenset(v2ps) in cache[v2]:
                # print "chit for add", v2, v2ps
                continue

        if can_addarc(bn, a) :
            bn.addarc(a, False) # NB. needs commit to update pic
            return a, (v2,)
    raise NoAction

def try_del(bn, cache=None, cstrs=None):
    maxtries = 20
    for t in xrange(maxtries) :
        if len(bn.arcs()) > 0:
            (v1, v2) = a = choice(tuple(bn.arcs()))
            if cstrs and a in cstrs.must : continue

            if cache and cache[v2]:
                v2ps = set(bn.parents(v2))
                v2ps.remove(v1)
                if frozenset(v2ps) in cache[v2]:
                    # print "chit for del", v2, v2ps
                    continue
            
            bn.delarc(a, False) # NB. needs commit to update pic
            return a, (v2,)
    raise NoAction

def try_rev(bn, cache = None, cstrs=None):
    maxtries = 20
    for t in xrange(maxtries):
        if len(bn.arcs()) > 0:
            (v1, v2) = a = choice(tuple(bn.arcs()))
            if cstrs and (a in cstrs.must or (v2,v1) in cstrs.no): continue

            if cache and cache[v1] and cache[v2]:
                v2ps = set(bn.parents(v2))
                v2ps.remove(v1)
                v1ps = set(bn.parents(v1))
                v1ps.add(v2)
                if frozenset(v1ps) in cache[v1] \
                        and frozenset(v2ps) in cache[v2]:
                    continue
            if can_revarc(bn,a):
                bn.revarc(a, True)
                # print "reversing", a, "in", bn.arcs()
                # map(bn.ancestors, bn.vars())
                return a, (v1,v2)
    raise NoAction


def fix_add(bn, arc): bn.pic_add(arc)
def fix_del(bn, arc): bn.pic_del(arc)
def fix_rev(bn, arc): pass

def cancel_add(bn, arc): bn.delarc(arc, False)
def cancel_del(bn, arc): bn.addarc(arc, False)
def cancel_rev(bn, (v1,v2)): bn.revarc((v2,v1))

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
    if max_time != None:
        end_time = time.time() + max_time

    def stopf(search_status):
        iter_crit = max_iters     and search_status["iters"]    >=max_iters
        acts_crit = limit_no_acts and search_ststus["t_no_acts"]>=limit_no_acts
        impr_crit = limit_no_impr and search_ststus["t_no_impr"]>=limit_no_impr
        acps_crit = limit_no_acps and search_ststus["t_no_acps"]>=limit_no_acps
        time_crit = max_time != None and time.time() >= end_time
        
        return iter_crit or acts_crit or impr_crit or acps_crit or time_crit
                
    return stopf

def stepper_f(actions, better, accept, cstrs=None):

    if not cstrs:
        cstrs = Constraints()

    def stepf(search_status):
        scr = search_status["scr"]
        bn =  search_status["curr_bn"]
        curr_score =  search_status["curr_score"]

        search_status["iters"] += 1
        try:
            aname, action = choice(acts["tryacts"].items())
            changes, avars = action(bn, cstrs=cstrs)
            search_status["t_no_acts"] = 0
            
            map(scr.storevar, avars)
            for avar in avars: scr.score_new_v(bn, avar)

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
        
    return stepf


def initial_search_status(bn, scr):
    curr_score = scr.score()
    return {"scr" : scr,
            "curr_bn" : bn,
            "curr_score" : curr_score,
            "best_bn" : bn.copy(),
            "best_score" : curr_score,
            "iters" : 0,
            "t_no_acts" : 0,
            "t_no_acps" : 0,
            "t_no_impr" : 0}

def localsearch(search_status, stepping, stopping):
    while True :
        stepping(search_status)
        if stopping(search_status) : break

def empty_net(bdtfile, ess):
    libdata = CDLL("/home/tsilande/projects/bn/learn_ctypes/data.so")
    data  = libdata.data_cread(bdtfile)
    bn = BN(libdata.nof_vars(data))
    scr = Score(bn, data, ess)
    return bn, scr

def main(bdtfile, ess):
    bn, scr = empty_net(bdtfile, ess)
    print scr.score(), bn.arcs()
    
if __name__ == '__main__':
    coliche.che(main, "bdtfile; ess (float)")
