#!/usr/bin/python

import sys, re

# THE RULES, THEIR PARSING AND INSTANTIATION

load_rules = """
    vd_o  = vd.load(vdfile)
    bn_o  = bn.load(bnfile)
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

"""

creat_rules = """
    ess_o      = ess.one()
    sss_o      = sss.sss(bn_o, dat_o)
    dpa_o      = dpa.dpa(sss_o, ess_o, bn_o, vd_o)
    tht_o      = tht.tht(dpa_o)
    mrl_o      = mrl.moralize(bn_o)
    elo_o      = elo.elo(mrl_o, vd_o)
    jtr_o      = jtr.jtr(clx_o,vd_o)
    clx_o      = trg.triangulate(mrl_o, vd_o, elo_o)
    vcx_o      = vcx.vclqs(bn_o, clx_o)
    pot_o      = pot.get_pots(bn_o, tht_o, vd_o, clx_o, vcx_o)

    ifr_o      = ifr.Inferer(vd_o, jtr_o, clx_o, pot_o, vcx_o)

    vdsave   = vd.save(vd_o, new_vdfile)
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

save_rules = """
"""

def parse_rules(rs):
    rulemap = {}
    for r in rs.split("\n"):
        if '=' not in r: continue
        h, t = r.split("=") # remember to strip them
        hneeds = re.findall('[a-z_]+', re.split("\(|\)", t)[1])
        rulemap[h.strip()] = (hneeds, t.strip())
    return rulemap


load_map  = parse_rules(load_rules)
creat_map = parse_rules(creat_rules)

# BUILDING THE HASH OF NEEDED MODULES SO THAT THEY CAN BE FOUND

modules = {}
mods = """bn ess mrl trg jtr vcx udg vd
          disdat sss tht clx pot elo ifr dpa sdt"""

for mod in mods.split():
    exec('import %s; modules["%s"] = %s' % (mod, mod, mod))


# HELPERS FOR THE MAIN LOGIC

def create(need, haved):
    if need in load_map and need[:-2]+'file' in haved:
        haved[need] = eval(load_map[need][1], modules, haved)
    elif need in creat_map:
        haved[need] = eval(creat_map[need][1], modules, haved)
    else:
        sys.exit("cannot create: %s !"% need)
    

def required_for(need, haved):
    if need in load_map and need[:-2]+'file' in haved:
        return set(load_map[need][0])
    elif need in creat_map:
        return set(creat_map[need][0])
    else:
        sys.exit("cannot satisfy need: %s !"% need)


# THE LOGIC

def inout(needed, haved):
    needed = needed[:]
    
    while needed:
        # print "N", needed
        # print "H", haved
        need = needed.pop()

        if need in haved: continue

        reqs = required_for(need, haved) - set(haved.iterkeys())

        if reqs:
            needed.append(need)
            for req in reqs:
                needed.append(req)
        else:
            create(need, haved)
            

if __name__ == '__main__':

    needed, haved = [],{}

    if '-e' in sys.argv:
        eix = sys.argv.index('-e')
        del sys.argv[eix]
        haved['ess_o'] = float(sys.argv.pop(eix))
    
    for a in sys.argv[1:] :
        if a.startswith('+'):
            a = a[1:]
            if '.' in a:
                ext = a.split('.')[1]
                needed.append(ext + 'save')
                haved['new_'+ext+'file'] = a
            else:
                needed.append(a+"_o")
        else:
            haved[a.split('.')[1]+'file'] = a

    inout(needed, haved)
