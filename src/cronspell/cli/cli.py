import enum
import logging
import sys

import typer
import typer.rich_utils

from cronspell import __version__
from cronspell.cli import locate, parse, pre_commit, to_dot


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
app.command(name="parse")(parse.parse)
app.command(name="dot")(to_dot.to_dot)
app.command(name="locate")(locate.locate)
app.command(name="pre-commit")(pre_commit.pre_commit)

if __name__ == "__main__":
    app()
