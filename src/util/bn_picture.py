#!/usr/bin/env python3
import os
import typer
import bn2dot

app = typer.Typer()

@app.command()
def bn2pic(bnfile:str, 
           picfile:str, 
           format:str="gif", 
           vdfile:str|None=None, 
           loners:bool=False, 
           center:str|None=None, 
           awfile:str|None=None):
    dotfile = "/tmp/%d" % os.getpid()
    bn2dot.bn2dot(bnfile,dotfile,vdfile,loners,center,awfile)
    os.system("dot -T%s -o%s %s" % (format, picfile, dotfile))
    os.unlink(dotfile)

if __name__ == "__main__":
    app()
