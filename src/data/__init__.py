"""
A typer module for data-related commands.
"""

import typer
from src.data import transpose_file
from src.data import tdt2bdt

app = typer.Typer(help="Commands related to data management.")
app.add_typer(transpose_file.app, help="Transpose data files.")
app.add_typer(tdt2bdt.app, help="Convert TDT files to BDT format.")

if __name__ == "__main__":
    app()