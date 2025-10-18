#!/usr/bin/env python3
import sys, os
import typer
from typing import Optional
from bn_picture import bn2pic

def main(bnfile: str, 
         format: str = "gif", 
         viewer: str = "display", 
         vdfile: Optional[str] = None, 
         loners: bool = False, 
         center: Optional[str] = None, 
         awfile: Optional[str] = None):
    picfile = "/tmp/%d.%s" % (os.getpid(), format)
    bn2pic(bnfile, picfile, format, vdfile, loners, center, awfile)
    os.system("%s %s" % (viewer, picfile))
    os.unlink(picfile)

if __name__ == "__main__":
    typer.run(main)
