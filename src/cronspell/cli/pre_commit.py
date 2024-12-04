from pathlib import Path
from typing import Annotated

import typer


def pre_commit(
    files: Annotated[
        list[Path],
        typer.Argument(
            ...,
            help="One or more Paths.",
        ),
    ],
):
    """
    * Takes a list of paths
    * validates expressions
    """
    ...
