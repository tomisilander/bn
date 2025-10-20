#!/usr/bin/env python3
import sys
import os
import tempfile
import shutil
import typer

app = typer.Typer()

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
            for line in src:
                sys.stdout.write(line)
    else:
        shutil.move(filenames[0], outfilename)

@app.command("transpose")
def transpose(inputfile: str, outputfile: str, delim: str|None = None, buffersize: int = 1000000):

    # SPLIT ROWS TO SMALLER PIECES AND TRANSPOSE THEM TO TEMP FILES

    workdir = tempfile.mkdtemp()

    if delim == "\\t": 
        delim = "\t"
    odelim = ' ' if delim is None else delim

    f = open(inputfile, "r", newline=None)
    try:
        i = 0
        colfns = []
        while True:
            ls = f.readlines(buffersize)
            if not ls: 
                break
            linetbls = [line.rstrip("\n").split(delim) for line in ls]
            colfns.append(os.path.join(workdir, "cols_%.8d" % i))
            rows2cols(linetbls, odelim, colfns[-1])
            i += 1
    finally:
        f.close()

    # PASTE PIECES

    paste(colfns, outputfile, odelim, workdir)

    # CLEAN IT

    shutil.rmtree(workdir)

if __name__ == "__main__":
    app()