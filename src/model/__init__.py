"""
A typer module for parameter learning related commands.
"""

import typer
import src.model.bnmodel as bnmodel
import src.model.logprob as logprob


app = typer.Typer(help="parameter learning related commands.")
app.add_typer(bnmodel.app, help="Parameter learning.")
app.add_typer(logprob.app, help="Data log-probability computation.")

if __name__ == "__main__":
    app()
