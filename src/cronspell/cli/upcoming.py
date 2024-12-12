import datetime
import sys
from typing import Annotated
from zoneinfo import ZoneInfo

import typer
from rich.console import Console

from cronspell.upcoming import moments

console = Console()


def upcoming(
    expression: Annotated[
        str,
        typer.Argument(
            ...,
            help="Expression",
        ),
    ],
    interval_days: Annotated[
        int,
        typer.Option(
            "--interval-days",
            "-d",
            help="interval of days to examine",
            default_factory=lambda: 1,
        ),
    ],
    initial_now: Annotated[
        str,
        typer.Option(
            "--initial-now",
            "-n",
            help="what to consider 'now'",
            default_factory=lambda: None,
        ),
    ],
    end: Annotated[
        str,
        typer.Option(
            "--end",
            "-e",
            help="end of date range to examine",
            default_factory=lambda: None,
        ),
    ],
):
    """
    \b
    * prints upcoming moments matched by expression
    """

    results = moments(
        expression=(expression or "/now"),
        interval=datetime.timedelta(days=interval_days),
        initial_now=(datetime.datetime.fromisoformat(initial_now) if initial_now else None),
        stop_at=(
            datetime.datetime.fromisoformat(end)
            if end
            else datetime.datetime.now(tz=ZoneInfo("UTC")) + datetime.timedelta(days=321)
        ),
    )

    for result in results:
        console.print(result.strftime("%G-W%V | %a %d %b %Y | %H:%M:%S %Z"))

    sys.exit(0)
