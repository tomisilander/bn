#!/usr/bin/python

import utils
from itertools import imap

def pwln(f,*fields):
    print >>f, " : ".join(imap(repr,fields))

    
def prln(l):
    # print l
    return map(eval, l.split(" : "))


def save(sdt, sdtfile):

    sdtf = file(sdtfile, "w")
    
    for i, sdti in enumerate(sdt):
        print >>sdtf, "#### %d ####" % i
        pwln(sdtf, len(sdti.dict), sdti.default)
        for item in  sdti.dict.iteritems():
            pwln(sdtf, *item)

    sdtf.close()


def load(sdtfile):

    sdtf = file(sdtfile)
    l = sdtf.readline()

    while l:
        nof_keys, default = prln(sdtf.readline())
        sdt = dict([prln(sdtf.readline()) for x in xrange(nof_keys)])
        yield utils.sparse_func(sdt, default)
        
        l = sdtf.readline()
