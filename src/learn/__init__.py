"""
A typer module for structure learning related commands.
"""

import typer
import src.learn.stocgreedy as stochgreedy
import src.learn.naive_bayes as naive_bayes
import src.learn.gi as gi

app = typer.Typer(help="Structure learning related commands.")
app.add_typer(stochgreedy.app, help="Stochastic greedy structure learning.")
app.add_typer(naive_bayes.app, help="NaiveBayes structure.")
app.add_typer(gi.app,          help="Empty net structure.")

if __name__ == "__main__":
    app()
