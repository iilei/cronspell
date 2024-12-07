from pathlib import Path
from typing import Annotated

import typer
from yamlpath.exceptions import UnmatchedYAMLPathException

from cronspell.cli.yaml import get_processor
from cronspell.resolve import resolve


class CronspellPreflightException(BaseException): ...


def preflight(
    files: Annotated[
        list[Path],
        typer.Argument(
            ...,
            help="One or more Paths.",
        ),
    ],
    yamlpath: Annotated[
        str,
        typer.Option("--yamlpath", "-p", show_default=False, help="yamlpath YAML_PATH"),
    ],
):
    """
    * Takes a list of paths
    * validates expressions
    """

    for file in files:
        processor = get_processor(file)

        try:
            for token in processor.get_nodes(yamlpath, mustexist=True):
                resolve(str(token).strip())
        except UnmatchedYAMLPathException as ex:
            msg = f"yamlpath {yamlpath} does not exist in {file}!"
            raise CronspellPreflightException(file, msg) from ex
