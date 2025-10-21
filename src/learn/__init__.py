"""
A typer module for data-related commands.
"""

import typer
import src.learn.stocgreedy as stochgreedy

app = typer.Typer(help="Structure learning related commands.")
app.add_typer(stochgreedy.app, help="Stochastic greedy structure learning.")

if __name__ == "__main__":
    app()