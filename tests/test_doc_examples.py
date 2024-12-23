import datetime as dt
from collections.abc import Generator

import time_machine

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
