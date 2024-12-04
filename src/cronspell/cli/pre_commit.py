from pathlib import Path
from typing import Annotated

import typer

from cronspell.cli.yaml import get_processor
from cronspell.resolve import resolve


def pre_commit(
    files: Annotated[
        list[Path],
        typer.Argument(
            ...,
            help="One or more Paths.",
        ),
    ],
    query: Annotated[
        str,
        typer.Option("--query", "-p", show_default=False, help="yamlpath YAML_PATH"),
    ],
):
    """
    * Takes a list of paths
    * validates expressions
    """

    for file in files:
        processor = get_processor(file)

        for token in processor.get_nodes(query):
            resolve(str(token).strip())
