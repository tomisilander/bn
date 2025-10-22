#!/usr/bin/env python
import bn.bn, data, scorefactory
import coliche
from bnsearch import empty_net
from constraints import Constraints

def gstep(bns,scr,params):
    
    # print params['candarcs']()
    for arc in params['candarcs']():
        if arc in params['tabuset']: continue
        (v1,v2)=arc
        # print 'try', arc
        sv2 = scr.score_ss_var(bns, v2)
        params['changef'](arc, False)
        schange = scr.score_ss_var(bns, v2) - sv2
        # print 'sch', schange
        params['cancelf'](arc, False)
        # print '1', bns.arcs()
        yield  schange, arc

def gsteps(bns,scr,params):
    while True:
        # print '0', bns.arcs() 
        chnglist = list(gstep(bns,scr,params))
        if len(chnglist) == 0: return
        bestsc, bestarc = max(chnglist)
        # print 'B', bns.arcs() 
        params['changef'](bestarc,do_pic=True)
        # print 'A', bns.arcs() 
        yield bestsc, bestarc

def main(bdtfile, scoretype='BDeu', ess=1.0, cachefile=None, bnfile=None,
         direction = 'up', constraint_file=""):

    cstrs = Constraints(constraint_file)

    if bnfile == None:
        bns,scr = empty_net(bdtfile,scoretype,ess,cachefile=cachefile)
    else:
        bns = bn.bn.load(bnfile, do_pic=True)
        bdt = data.Data(bdtfile)
        scr = scorefactory.getscorer(bdt,scoretype,ess,cachefile=cachefile)
        scr.score_new(bns)

    updown = {
        'up':{'changef':bns.addarc, 'cancelf':bns.delarc,
              'tabuset':cstrs.no, 'candarcs':bns.new_dagarcs,
              'actname':'add'},
        'down':{'changef':bns.delarc, 'cancelf':bns.addarc,
                'tabuset':cstrs.must, 'candarcs':bns.arcs,
                'actname':'del'}
    }

    print('init', -1, -1, scr.score())
    params = updown[direction]
    for sdiff, arc in gsteps(bns, scr, params):
        scr.score_new(bns) # needed?
        print(params['actname'], arc[0], arc[1], scr.score())

        
if __name__ == '__main__':
    
    coliche.che(main,
                ''' bdtfile               
                -g --goodness scoretype BDeu|fNML|AIC|BIC : default: BDeu
                -e --ess ess (float) : default 1.0
                -c constraint_file : a file with arcs marked with + or -
                -m --cachefile cachefile: local scores
                -i --initnet bnfile : starting point : defauly: empty net
                -d --dir direction up|down : default: up
''')
