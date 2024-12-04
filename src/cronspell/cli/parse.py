from typing import Annotated

import typer

from cronspell import cronspell


def parse(
    expression: Annotated[
        str,
        typer.Argument(
            help="Date-Expression, e.g 'now /month",
            default_factory=lambda: "now",
        ),
    ],
    fmt: Annotated[
        str,
        typer.Option(
            "--format", "-f", show_default=False, help="Optional format parameter.", default_factory=lambda: ""
        ),
    ],
):
    parsed = cronspell(expression)
    print(parsed.strftime(fmt) if len(fmt) > 0 else parsed.isoformat())  # noqa: T201
