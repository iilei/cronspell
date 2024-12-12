import typer
import typer.rich_utils

from cronspell import __version__
from cronspell.cli import locate, parse, preflight, to_dot, upcoming

app = typer.Typer(
    name=f"CronSpell {__version__}",
    help="Date-expression domain specific language parsing. "
    'A neat way to express things like "First Saturday of any year", '
    'or "3rd thursdays each month" and such',
    pretty_exceptions_enable=False,
)
app.command(name="parse")(parse.parse)
app.command(name="dot")(to_dot.to_dot)
app.command(name="locate")(locate.locate)
app.command(name="preflight")(preflight.preflight)
app.command(name="upcoming")(upcoming.upcoming)

if __name__ == "__main__":
    app()
