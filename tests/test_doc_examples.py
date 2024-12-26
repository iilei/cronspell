import datetime as dt
from collections.abc import Generator

import time_machine

from cronspell import parse
from cronspell.upcoming import moments as upcoming


@time_machine.travel(dt.datetime.fromisoformat("2024-12-23T00:00:00+00:00"), tick=False)
def test_python_example_next_cw3_a():
    cw3: Generator = upcoming("@cw 3")

    assert next(cw3).strftime("%G-W%V") == "2025-W03"
    assert next(cw3).strftime("%G-W%V") == "2025-W06"
    assert next(cw3).strftime("%G-W%V") == "2025-W09"


@time_machine.travel(dt.datetime.fromisoformat("2025-01-01T00:00:00+00:00"), tick=False)
def test_python_example_next_cw3_c():
    cw3: Generator = upcoming("@cw 3")

    assert next(cw3).strftime("%G-W%V") == "2025-W03"
    assert next(cw3).strftime("%G-W%V") == "2025-W06"
    assert next(cw3).strftime("%G-W%V") == "2025-W09"


@time_machine.travel(dt.datetime.fromisoformat("2025-01-06T00:00:00+00:00"), tick=False)
def test_python_example_next_cw3_d():
    cw3: Generator = upcoming("@cw 3")

    assert next(cw3).strftime("%G-W%V") == "2025-W03"
    assert next(cw3).strftime("%G-W%V") == "2025-W06"
    assert next(cw3).strftime("%G-W%V") == "2025-W09"


@time_machine.travel(dt.datetime.fromisoformat("2025-01-13T00:00:00+00:00"), tick=False)
def test_python_example_next_cw3_e():
    cw3: Generator = upcoming("@cw 3")

    assert next(cw3).strftime("%G-W%V") == "2025-W06"


@time_machine.travel(dt.datetime.fromisoformat("2025-01-13T00:00:00+00:00"), tick=False)
def test_python_multimatch_a():
    mm: Generator = upcoming(
        """\
        {
            // first saturday of the month:
            /m -1d/sat + 7d,

            // sunday every second calendar week:
            @cw 2 + 6d
        }\
        """
    )

    assert next(mm).strftime("%a %G-W%V") == "Sun 2025-W04"
    assert next(mm).strftime("%a %G-W%V") == "Sat 2025-W05"
    assert next(mm).strftime("%a %G-W%V") == "Sun 2025-W06"
    assert next(mm).strftime("%a %G-W%V") == "Sun 2025-W08"
    assert next(mm).strftime("%a %G-W%V") == "Sat 2025-W09"
    assert next(mm).strftime("%a %G-W%V") == "Sun 2025-W10"


def test_python_multimatch_b():
    expression = """\
            now[Europe/Berlin] {
                // first saturday of the month:
                /m -1d /sat + 7d,

                // sunday of every second calendar week:
                @cw2 + 6d
            }\
            """
    with time_machine.travel(dt.datetime.fromisoformat("2025-01-13T00:00:00+00:00"), tick=False):
        mm: Generator = upcoming(expression)

        assert next(mm).isoformat() == "2025-01-26T00:00:00+01:00"
        assert next(mm).tzinfo.key == "Europe/Berlin"

    with time_machine.travel(dt.datetime.fromisoformat("2025-06-13T00:00:00+00:00"), tick=False):
        mm: Generator = upcoming(expression)

        assert next(mm).isoformat() == "2025-06-15T00:00:00+02:00"
        assert next(mm).tzinfo.key == "Europe/Berlin"


@time_machine.travel(dt.datetime.fromisoformat("2025-01-01T00:00:00+00:00"), tick=False)
def test_python_multimatch_c():
    assert parse("{/sun}").strftime("%a %Y-%m-%d") == "Sun 2024-12-29"
    assert parse("{/m+1d, /m+10d, /sun}").strftime("%a %Y-%m-%d") == "Sun 2024-12-29"
    assert parse("{/sun, -1d /m+30d}").strftime("%a %Y-%m-%d") == "Tue 2024-12-31"
