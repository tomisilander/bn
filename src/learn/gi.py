#!/usr/bin/env python

import typer
import src.learn.bnsearch as bnsearch

app = typer.Typer()

@app.command("empty_net")
def main(bdtfile, scoretype='BDeu', ess=1.0, outfile=None, cachefile=None):

    bn, sc = bnsearch.empty_net_n_score(bdtfile, scoretype, ess, cachefile=cachefile)

    if outfile:
        bn.save(outfile)

    print(sc.score())

if __name__ == '__main__':
    app()
