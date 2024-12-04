import datetime as dt

import time_machine
from typer.testing import CliRunner

from cronspell.cli.cli import app

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


def test_hook():
    result = runner.invoke(app, ["pre-commit", "xyz"])
    # Check that the command executed successfully
    assert result.exit_code == 0, f"Error: {result.stdout}"
    # implementation pending


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29"), tick=False)
def test_cli_strformat():
    """CLI Tests"""
    # Simulate the command line invocation
    result = runner.invoke(app, ["parse", "now", "--format", r"%m/%d/%Y"])

    # Check that the command executed successfully
    assert result.exit_code == 0, f"Error: {result.stdout}"

    # Assert against the expected output
    assert result.stdout == "12/29/2024\n"
