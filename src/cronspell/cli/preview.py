import datetime
from datetime import time, timedelta
from functools import reduce
from typing import Annotated

import typer
from rich.console import Console

from cronspell.cronspell import Cronspell
from cronspell.parse import parse

console = Console()


def preview(
    expression: Annotated[
        str,
        typer.Argument(
            ...,
            help="Expression",
        ),
    ],
    style: Annotated[
        str,
        typer.Option(
            "--style",
            "-s",
            show_default=False,
            help="Style format template",
            default_factory=r"[bold red]%s[/bold red]",
        ),
    ],
    end: Annotated[
        str,
        typer.Option(
            "--end",
            "-e",
            show_default=False,
            help="end of date range to examine",
            default_factory=parse("/month + 340 days /month -1d").strftime(r"%Y-%m-%d"),
        ),
    ],
):
    """
    \b
    * prints a calendar with highlighted occurrences
    """
    cronspell = Cronspell()

    start = parse(f"{parse(expression).isoformat()} / month")
    end = parse(end).astimezone(start.timetz().tzinfo)

    days = range(0, ((end - start).days - 1))

    def calc(seq, curr):
        cronspell.now_func = lambda: datetime.datetime.combine(curr, time.max)
        is_match = curr.timetuple()[0:3] == cronspell.parse(expression).timetuple()[0:3]
        curr_styled = style % curr.day if is_match else curr.day
        is_m_end = (curr + timedelta(days=1)).day == 1

        if curr.day == 1:
            return [*seq, [*([""] * curr.weekday()), curr_styled]]

        pad = [""] * (6 - curr.weekday()) if is_m_end else []
        return [*seq[0:-1], [*seq[-1], curr_styled, *pad]]

    reduce(calc, [start + timedelta(days=x) for x in days], [])

    # (function: (_T@reduce, _S@reduce) -> _T@reduce, sequence: Iterable[_S@reduce], initial: _T@reduce, /) -> _T@reduce

    # table = Table("Name", "Item")
    # table.add_row("Rick", "Portal Gun")
    # table.add_row("Morty", "Plumbus")
    # console.print(table)
