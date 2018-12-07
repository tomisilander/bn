#!/usr/bin/python

"""
The idea is to cast this as a planning problem. The state is the objects
you have and you have to find your way to goal state. 
"""

import sys, re

# THE RULES, THEIR PARSING AND INSTANTIATION

rules = """
    vd_o   = bn.vd.load(vdfile)
    bn_o   = bn.bn.load(bnfile)
    bnm_o  = bn.model.bnmodel.load(bnmfile, vd_o)
    dat_o = disdat.RowData(vdfile, datfile)
    sss_o = sdt.load(sssfile)
    dpa_o = sdt.load(dpafile)
    tht_o = sdt.load(thtfile)
    mrl_o = udg.load(mrlfile)
    elo_o = elo.load(elofile)
    clx_o = trg.clx_load(clxfile)
    jtr_o = udg.load(jtrfile)
    vcx_o = vcx.load(vcxfile)
    pot_o = pot.load(potfile, clx_o, vd_o)
    ifr_o = ifr.load(ifrfile)

    bn_o       = bn.model.bnmodel.bnt(bnm_o)
    ess_o      = ess.one()
    sss_o      = sss.sss(bn_o, dat_o)
    dpa_o      = dpa.dpa(sss_o, ess_o, bn_o, vd_o)
    tht_o      = tht.tht(dpa_o)
    tht_o      = bnm2tht.tht(bnm_o)
    mrl_o      = mrl.moralize(bn_o)
    elo_o      = elo.elo(mrl_o, vd_o)
    jtr_o      = jtr.jtr(clx_o,vd_o)
    clx_o      = trg.triangulate(mrl_o, vd_o, elo_o)
    vcx_o      = vcx.vclqs(bn_o, clx_o)
    pot_o      = pot.get_pots(bn_o, tht_o, vd_o, clx_o, vcx_o)
    ifr_o      = ifr.Inferer(vd_o, jtr_o, clx_o, pot_o, vcx_o)

    vdsave   = bn.vd.save(vd_o, new_vdfile)
    ssssave  = sdt.save(sss_o, new_sssfile)
    dpasave  = sdt.save(dpa_o, new_dpafile)
    thtsave  = sdt.save(tht_o, new_thtfile)
    mrlsave  = udg.save(mrl_o, new_mrlfile)
    elosave  = elo.save(elo_o, new_elofile)
    clxsave  = trg.clx_save(clx_o, new_clxfile)
    jtrsave  = udg.save(jtr_o, new_jtrfile)
    vcxsave  = vcx.save(vcx_o, new_vcxfile)
    potsave  = pot.save(pot_o, new_potfile)
    ifrsave  = ifr.save(ifr_o, new_ifrfile)
"""

def parse_rules(rs):
    acts = []
    mods = set()
    for r in rs.split("\n"):
        if '=' not in r: continue
        postc, aprecs = r.split("=") # remember to strip them
        (a,precs) = re.split("\(|\)", aprecs)[:2]
        prec = re.findall('[a-z_]+', precs)
        acts.append((a.strip(),tuple(prec),postc.strip()))
	for i in xrange(a.count('.')):
            mods.add('.'.join(a.strip().split('.')[0:i+1]))
    return acts, mods


acts,mods = parse_rules(rules)

# BUILDING THE HASH OF NEEDED MODULES SO THAT THEY CAN BE FOUND

modules = {}
for mod in mods:
    exec('import %s; modules["%s"] = %s' % (mod, mod, mod))

# THE LOGIC ff-plan and bw-plan

# try actions until goal is reached
def ffplan(have, goal, path=[]):
    plan = []
    while not goal <= have:
        try:
            a = next(a for a in acts 
                     if (set(a[1]) <= have) and (a[2] not in have))
            have.add(a[2])
            plan.append(a)
        except:
            return None
    return plan

# track backward the steps that are really used for a goal
def track(plan, goal, haved, used):
    if goal in haved: return

    # otherwise something must have produced it
    try:
        act = next(a for a in plan if a[2] == goal)
        if act in used: return 
        used.add(act)    
    except:
        print "No", goal, 'in', plan
        raise

    subgoals = act[1]
    for subgoal in subgoals:
        track(plan,subgoal, haved, used)

def exec_plan(plan, havenv):
    # for (k,v) in havenv.iteritems(): print k, '=', repr(v)
    for (a,precs,postc) in plan:
        func = '%s(%s)' % (a, ', '.join(precs))
        # print postc, '=', func
        # print modules
        havenv[postc]=eval(func,modules,havenv)

def inout(needed, havenv):
    haved = set(havenv.iterkeys())
    plan = ffplan(haved.copy(),needed)
    if plan == None:
        print "No plan found to get", needed, 'from', havenv.keys()
        return

    used = set()
    execed = set()
    for goal in needed: # think multiple goals better
        track(plan, goal, haved, used)
        cplan = [p for p in plan if p in used-execed]
        exec_plan(cplan, havenv)
        execed.update(used)

if __name__ == '__main__':

    needed, havenv = set(), {}
    
    if '-e' in sys.argv:
        eix = sys.argv.index('-e')
        havenv['ess_o'] = float(sys.argv[eix+1])
        del sys.argv[eix:eix+2]
    
    for a in sys.argv[1:] :
        if a.startswith('+'):
            a = a[1:]
            if '.' in a:
                ext = a.split('.')[1]
                needed.add(ext + 'save')
                havenv['new_'+ext+'file'] = a
            else:
                needed.add(a+"_o")
        else:
            havenv[a.split('.')[1]+'file'] = a

    inout(needed, havenv)
