import typer

from src.vd import load as vdload
from src.bn import BN

app = typer.Typer()


def naive_bayes(variables: str, class_var: str) -> BN:
    """Constructs a naive bayes structure.

    Each variable (except the class variable) has an edge from the class variable.

    Args:
        variables: Number of variables in the data or a vdfile.
        class_var: Index or name of the class variable.
    Returns:
        A BN object representing the naive bayes structure.
    """

    if isinstance(variables, str):
        valdes = vdload(variables)
        varc = valdes.nof_vars()
        class_idx = valdes.varnames.index(class_var)
    else:
        varc = int(variables)
        class_idx = int(class_var)

    assert isinstance(class_idx, int) and 0 <= class_idx < varc

    bn = BN(varc)
    for i in range(varc):
        if i != class_idx:
            bn.addarc((class_idx, i), do_pic=False)
    return bn

@app.command("naive_bayes")
def main(variables: str, class_var: str, outfile: str):
    bn = naive_bayes(variables, class_var)
    bn.save(outfile)


if __name__ == "__main__":
    app()
