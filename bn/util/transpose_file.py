#!/usr/bin/env python3

import sys, os, tempfile, shutil
import typer
from typing import Optional

def rows2cols(linetbls, osep, tfn):
    # write transposed columns to tfn (Python 3)
    with open(tfn, "w", newline='') as tf:
        icols = zip(*linetbls)
        itlns = map(osep.join, icols)
        for tln in itlns:
            tf.write(tln + "\n")

def paste(filenames, outfilename, sep, workdir):

    while len(filenames) > 1:

        fns_64    = filenames[   : 64]
        filenames = filenames[64 :]

        outfd, outfn_64 = tempfile.mkstemp(dir=workdir)
        outf = os.fdopen(outfd, "w")

        # READ LINES FROM EACH FILE AND WRITE TO OUTFILE

        files = [open(fn, "r", newline=None) for fn in fns_64]
        lastfile = files.pop(-1)
        try:
            while True:
                lastline = lastfile.readline()
                if not lastline:
                    break

                for f in files:
                    # remove trailing newline safely, then write sep
                    outf.write(f.readline().rstrip("\n"))
                    outf.write(sep)
                outf.write(lastline)
        finally:
            outf.close()
            for f in files:
                f.close()
            lastfile.close()

        filenames.insert(0,outfn_64)

    if outfilename == '-':
        with open(filenames[0], "r", newline=None) as src:
            for l in src:
                sys.stdout.write(l)
    else:
        shutil.move(filenames[0], outfilename)

def transpose(ifn: str, ofn: str, delim: Optional[str] = None, buffersize: int = 1000000):

    # SPLIT ROWS TO SMALLER PIECES AND TRANSPOSE THEM TO TEMP FILES

    workdir = tempfile.mkdtemp()

    if delim == "\\t": delim = "\t"
    odelim = ' ' if delim is None else delim

    f = open(ifn, "r", newline=None)
    try:
        i = 0
        colfns = []
        while True:
            ls = f.readlines(buffersize)
            if not ls: break
            linetbls = [l.rstrip("\n").split(delim) for l in ls]
            colfns.append(os.path.join(workdir, "cols_%.8d" % i))
            rows2cols(linetbls, odelim, colfns[-1])
            i += 1
    finally:
        f.close()

    # PASTE PIECES

    paste(colfns, ofn, odelim, workdir)

    # CLEAN IT

    shutil.rmtree(workdir)

if __name__ == "__main__":
    typer.run(transpose)