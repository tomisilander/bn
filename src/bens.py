"""
The main typer entry for called "bens" for a tools for learning Bayesian networks.
"""

import typer
from src.data import app as data_app
from src.learn import app as learn_app
from src.model import app as model_app

app = typer.Typer(name="bens", help="Tools for learning Bayesian networks.")
app.add_typer(data_app, name="data", help="Commands related to data management.")
app.add_typer(learn_app, name="learn", help="Commands related to structure learning.")
app.add_typer(model_app, name="model", help="Commands related to Bayesian network models.")

if __name__ == "__main__":
    app()
