"""
The main typer entry for called "bens" for a tools for learning Bayesian networks. 
"""

import typer
from .data import app as data_app
app = typer.Typer(name="bens", help="Tools for learning Bayesian networks.")
app.add_typer(data_app, name="data", help="Commands related to data management.")

if __name__ == "__main__":
    app()

