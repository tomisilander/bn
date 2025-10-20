#!/usr/bin/python 

from ctypes import CDLL, c_void_p, c_int, c_char_p
from pathlib import Path
class Data:

    def __init__(self, filename) :

        d = Path(__file__).parent.absolute()
        self.libcdata = CDLL(d/"cdata.so")


        c_cread = self.libcdata.data_cread
        c_cread.argtypes = [c_char_p]
        c_cread.restype = c_void_p

        self.libcdata.data_nof_vars.argtypes = [c_void_p]

        self.libcdata.data_nof_vals.argtypes = [c_void_p, c_int]

        filepath = Path(filename).resolve()
        assert filepath.exists() and filepath.is_file() 
        c_file = c_char_p(str(filepath).encode('ascii'))
        self.dt = c_cread(c_file)

    def __del__(self):
        if self.dt:
            pass
            # libcdata.data_free(pointer(self.dt))

    def nof_vars(self):
        return self.libcdata.data_nof_vars(self.dt)

    def nof_vals(self, v):
        return self.libcdata.data_nof_vals(self.dt, v)

if __name__ == '__main__':
    from argparse import ArgumentParser

    def test(bdtfile):
        dt = Data(bdtfile)
        print(dt.nof_vars(), [dt.nof_vals(v) for v in range(dt.nof_vars())])    
    
    parser = ArgumentParser(description='Test data module')
    parser.add_argument('bdtfile', type=str)
    args = parser.parse_args()
    test(args.bdtfile)