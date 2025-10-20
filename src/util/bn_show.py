#!/usr/bin/env python3
import os
import typer
from .bn_picture import bn2pic
app = typer.Typer()

@app.command()
def bn_show(bnfile: str, 
            format: str = "gif", 
            viewer: str = "display", 
            vdfile: str|None = None, 
            loners: bool = False, 
            center: str|None = None, 
            awfile: str|None = None):
    picfile = "/tmp/%d.%s" % (os.getpid(), format)
    bn2pic(bnfile, picfile, format, vdfile, loners, center, awfile)
    os.system("%s %s" % (viewer, picfile))
    os.unlink(picfile)

if __name__ == "__main__":
    app()
