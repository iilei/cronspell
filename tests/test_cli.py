import datetime as dt
from pathlib import Path

import time_machine
from typer.testing import CliRunner

from cronspell.cli import app, to_dot

runner = CliRunner()


def test_app_isoformat():
    """CLI Tests"""
    # Simulate the command line invocation
    result = runner.invoke(app, ["now[Europe/Berlin] /m /sat"])

    # Check that the command executed successfully
    assert result.exit_code == 0, f"Error: {result.stdout}"

    # Capture the output
    out = result.stdout

    # Assert against the expected output
    assert "+01:00" in out or "+02:00" in out


def test_cronspell_to_dot(data_path):
    """CLI Tests"""
    out_file = Path.joinpath(data_path, "test-output.dot")
    # Simulate the command line invocation
    result = runner.invoke(to_dot, ["now[Europe/Berlin] /m /sat", "--out", out_file])

    # Check that the command executed successfully
    assert result.exit_code == 0, f"Error: {result.stdout}"

    # Capture the output
    assert out_file == ""

    # Assert against the expected output


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29"), tick=False)
def test_app_strformat():
    """CLI Tests"""
    # Simulate the command line invocation
    result = runner.invoke(app, ["now", "--format", r"%m/%d/%Y"])

    # Check that the command executed successfully
    assert result.exit_code == 0, f"Error: {result.stdout}"

    # Assert against the expected output
    assert result.stdout == "12/29/2024\n"
