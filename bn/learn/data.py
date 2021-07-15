#!/usr/bin/python 

from ctypes import *
import os

class Data:

    def __init__(self, filename) :
        d = os.path.dirname(os.path.abspath(__file__))
        self.libcdata = CDLL(os.path.join(d,"cdata.so"))


        c_cread = self.libcdata.data_cread
        c_cread.restype = c_void_p

        self.libcdata.data_nof_vars.argtypes = [c_void_p]

        self.libcdata.data_nof_vals.argtypes = [c_void_p, c_int]

        open(filename).close() # throws exception if not working
        self.dt = c_cread(filename)

    def __del__(self):
        if self.dt:
            pass
            # libcdata.data_free(pointer(self.dt))

    def nof_vars(self):
        return self.libcdata.data_nof_vars(self.dt)

    def nof_vals(self, v):
        return self.libcdata.data_nof_vals(self.dt, v)

import coliche

def test(bdtfile):
    dt = Data(bdtfile)
    print dt.nof_vars(), [dt.nof_vals(v) for v in xrange(dt.nof_vars())]    
    

coliche.che(test,'bdtfile')
