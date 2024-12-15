import datetime
import sys
from typing import Annotated
from zoneinfo import ZoneInfo

import typer
from rich.console import Console

from cronspell.upcoming import moments

console = Console()


def upcoming(
    expression: str,
    interval_days: Annotated[
        int,
        typer.Option(
            "--interval-days",
            "-d",
            help="Interval of days to examine (default: 1)",
            default_factory=lambda: 1,
        ),
    ],
    initial_now: Annotated[
        str,
        typer.Option(
            "--initial-now",
            "-n",
            help="What to consider as 'now' (default: current date and time)",
            default_factory=lambda: None,
        ),
    ],
    end: Annotated[
        str,
        typer.Option(
            "--end",
            "-e",
            help="End of date range to examine (default: 321 days from now)",
            default_factory=lambda: None,
        ),
    ],
):
    """
    Prints upcoming moments matched by the given expression.

    Arguments:
        expression (str): The date expression to evaluate.
        interval_days (int): Interval of days to examine (default: 1).
        initial_now (str): What to consider as 'now' (default: current date and time).
        end (str): End of the date range to examine (default: 321 days from now).

    The function evaluates the given date expression over the specified interval and prints
    the upcoming moments that match the expression. The evaluation starts from the 'initial_now'
    date and continues until the 'end' date.
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
