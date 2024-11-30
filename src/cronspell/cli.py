import enum
import logging
import sys
from typing import Annotated

import typer
import typer.rich_utils

from cronspell import __version__, cronspell


class LogLevel(str, enum.Enum):
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"


def setup_logging(log_level: LogLevel):
    """Setup basic logging"""
    log_format = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    numeric_level = getattr(logging, log_level.upper(), None)
    logging.basicConfig(
        level=numeric_level,
        stream=sys.stdout,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


app = typer.Typer(
    name=f"CronSpell {__version__}",
    help="Date-expression domain specific language parsing. "
    'A neat way to express things like "First Saturday of any year", '
    'or "3rd thursdays each month" and such',
)


@app.command()
def main(
    expression: Annotated[
        str,
        typer.Argument(
            ...,
            help="Date-Expression, e.g 'now /month",
            default_factory=lambda: "now",
        ),
    ],
    fmt: Annotated[
        str,
        typer.Option(
            ..., "--format", "-f", show_default=False, help="Optional format parameter.", default_factory=lambda: ""
        ),
    ],
):
    parsed = cronspell(expression)
    print(parsed.strftime(fmt) if len(fmt) > 0 else parsed.isoformat())  # noqa: T201


if __name__ == "__main__":
    app()
