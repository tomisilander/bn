
# You can choose not to cache data to memory if you like

class ColData:
    
    def __init__(self, vdfile, tdtfile, cache_all=True):
        self.vdfile  = vdfile
        self.tdtfile = tdtfile

        self.coldata   = None
        self.rowdata   = None
        self.n         = None
        self.valcounts = None

        if cache_all:
            self.cache_format()
            self.cache_coldata()
            self.cache_rowdata()

    def cache_coldata(self):
        self.coldata = list(map(list,self.vars()))

    def cache_rowdata(self):
        self.rowdata = list(map(list,self.dats()))

    def cache_format(self):
        self.valcounts = list(self.nof_vals())
        self.n = self.N()


    def nof_vals(self):
        if self.valcounts is not None:
            return self.valcounts 
        else:
            return (line.count("\t") for line in open(self.vdfile))

    def vars(self):
        if self.coldata is not None:
            return self.coldata
        else:
            # lines = (map(int, line.split()) for line in open(self.tdtfile)) 
            # for line in lines:
            #     print(list(line))
            lines = (map(int, line.split()) for line in open(self.tdtfile)) 
            return lines
            
            return (map(int, line.split()) for line in open(self.tdtfile))

    def dats(self):
        if self.rowdata is not None:
            return self.rowdata
        else:
            return zip(*self.vars())

    def N(self):
        if self.n is not None:
            return self.n
        else:
            return sum(1 for _ in self.dats())

class RowData:
    
    def __init__(self, vdfile, datfile):
        self.vdfile  = vdfile
        self.datfile = datfile

    def nof_vals(self):
        for line in open(self.vdfile):
            yield line.count("\t")

    def vars(self):
        return zip(*self.dats())

    def dats(self):
        for line in open(self.datfile):
            yield map(int, line.split())

    def N(self):
        return sum(1 for _ in self.dats())
