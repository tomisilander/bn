#!/usr/bin/python

import sys, os, tempfile, itertools, shutil

def rows2cols(linetbls, osep, tfn):
    tf = file(tfn,"w")
    icols = itertools.izip(*linetbls)
    itlns = itertools.imap(osep.join, icols)
    for tln in itlns:
        print >>tf, tln
    tf.close()

def paste(filenames, outfilename, sep, workdir):

    while len(filenames) > 1:

        fns_64    = filenames[   : 64]
        filenames = filenames[64 :]

        outfd, outfn_64 = tempfile.mkstemp("","",workdir,"")
        outf = os.fdopen(outfd, "w")
        
        # READ LINES FROM EACH FILE AND WRITE TO OUTFILE
        
        files = [file(fn,"rU") for fn in fns_64]
        lastfile = files.pop(-1)
        while True:
            lastline = lastfile.readline()
            if not lastline: break
            
            for f in files:
                outf.write(f.readline()[:-1])
                outf.write(sep)
            outf.write(lastline)

        outf.close()
        for f in files: f.close()

        filenames.insert(0,outfn_64)

    if outfilename == '-':
        for l in file(filenames[0]):
            sys.stdout.write(l)
    else:
        shutil.move(filenames[0], outfilename)


def transpose(ifn, ofn, delim=None, buffersize=1000000):
    
    # SPLIT ROWS TO SMALLER PIECES AND TRANSPOSE THEM TO TEMP FILES
    
    workdir = tempfile.mkdtemp()

    if delim == "\\t": delim = "\t"
    odelim = (delim == None) and  ' ' or delim
    
    f = file(ifn, "rU")
    i = 0
    colfns = []
    while True:
        ls = f.readlines(buffersize)
        if not ls: break
        linetbls = [l[:-1].split(delim) for l in ls]
        colfns.append(os.path.join(workdir, "cols_%.8d" % i))
        rows2cols(linetbls, odelim, colfns[-1])
        i += 1
    
    # PASTE PIECES
                      
    paste(colfns, ofn, odelim, workdir)

    # CLEAN IT
    
    shutil.rmtree(workdir)

if __name__ == "__main__":
    from coliche import che
    che(transpose,
        """infile; outfile;
        -d --delim delim : field separator (default: whitespaces)""")
