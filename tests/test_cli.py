import datetime as dt
from pathlib import Path

import pytest
import time_machine
from typer.testing import CliRunner

from cronspell.cli.cli import app
from cronspell.exceptions import CronpellMathException

runner = CliRunner()


def test_cli_isoformat():
    """CLI Tests"""
    # Simulate the command line invocation
    result = runner.invoke(app, ["parse", "now[Europe/Berlin] /m /sat"])

    # Check that the command executed successfully
    assert result.exit_code == 0, f"Error: {result.stdout}"

    # Capture the output
    out = result.stdout

    # Assert against the expected output
    assert "+01:00" in out or "+02:00" in out


def test_cronspell_to_dot_good_case(data_path):
    """CLI Tests"""

    # Simulate the command line invocation
    result = runner.invoke(app, ["dot", "now[Europe/Berlin] /m /sat", "now[Europe/Berlin] /m /fri", "--out", data_path])

    # Check that the command executed successfully
    assert result.exit_code == 0, f"Error: {result.stdout}"

    assert result.stdout == ""


def test_cronspell_to_dot_bad_case(data_path):
    """CLI Tests"""

    # Simulate the command line invocation
    result = runner.invoke(app, ["dot", "now[Europe/Berlin] @notatoken 9999", "--out", data_path])

    # Check that the command executed successfully
    assert result.exit_code == 1, f"Error: {result.stdout}"


def test_cronspell_locate():
    result = runner.invoke(app, ["locate"])
    # Check that the command executed successfully
    assert result.exit_code == 0, f"Error: {result.stdout}"

    assert "cronspell.tx" in result.stdout


def test_hook_good_expressions(data_path):
    test_file = Path(data_path).joinpath("testfile_a.yaml")
    test_file.write_text("""\
- type: first_saturday
  cronspell: /month -1day /sat + 1 week
- type: first_friday
  cronspell: /month -1day /fri + 1 week
""")

    result = runner.invoke(app, ["pre-commit", "--query", "/*/cronspell", test_file.as_posix()])
    # Check that the command executed successfully
    assert result.exit_code == 0, f"Error: {result.stdout}"


def test_hook_bad_expression(data_path):
    test_file = Path(data_path).joinpath("testfile_b.yaml")
    test_file.write_text("""\
- type: first_saturday
  cronspell: "@cw 77"
""")

    with pytest.raises(CronpellMathException, match=r".*needed lower than 53.*"):
        result = runner.invoke(app, ["pre-commit", "--query", "/*/cronspell", test_file.as_posix()])
        assert result.exit_code == 1, f"Error: {result.stdout}"


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29"), tick=False)
def test_cli_strformat():
    """CLI Tests"""
    # Simulate the command line invocation
    result = runner.invoke(app, ["parse", "now", "--format", r"%m/%d/%Y"])

    # Check that the command executed successfully
    assert result.exit_code == 0, f"Error: {result.stdout}"

    # Assert against the expected output
    assert result.stdout == "12/29/2024\n"
