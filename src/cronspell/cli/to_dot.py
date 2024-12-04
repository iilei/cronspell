import hashlib
from pathlib import Path
from typing import Annotated

import typer
from textx.export import model_export

from cronspell.cronspell import Cronspell


def to_dot(
    expressions: Annotated[
        list[str],
        typer.Argument(
            ...,
            help="One or more Date-Expressions, e.g 'now /month'",
        ),
    ],
    out: Annotated[
        Path,
        typer.Option("--out", "-o", show_default=False, help="Where to write output"),
    ],
    sha_len: Annotated[
        int,
        typer.Option(
            "--sha-len",
            "-s",
            show_default=True,
            help="Number of character to truncate the sha to",
            default_factory=lambda: 7,
        ),
    ],
    pad_len: Annotated[
        int,
        typer.Option(
            "--pad-len",
            "-p",
            show_default=True,
            help="Number of character to pad the leading number to",
            default_factory=lambda: 3,
        ),
    ],
):
    cronspell = Cronspell()
    pad = max(pad_len, len(str(len(expressions))))

    for idx, expression in enumerate(expressions):
        model = cronspell.meta_model.model_from_str(expression)
        sha = hashlib.sha3_224(f"{expression.replace(' ', '')}".encode()).hexdigest()[0:sha_len]
        destination = Path.joinpath(out, f"{idx:0{pad}}_{sha}.dot")
        model_export(model, destination)
