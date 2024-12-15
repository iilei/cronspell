import datetime as dt
from datetime import timedelta
from zoneinfo import ZoneInfo

import pytest
import time_machine

from cronspell.exceptions import CronpellInputException
from cronspell.upcoming import moments


@time_machine.travel(dt.datetime.fromisoformat("2025-01-21"), tick=False)
def test_upcoming_moments():
    assert [*moments("/month", stop_at=dt.datetime(2025, 3, 1, tzinfo=ZoneInfo("UTC")))] == [
        dt.datetime(2025, 1 + y, 1, tzinfo=ZoneInfo("UTC")) for y in range(0, 3)
    ]


@time_machine.travel(dt.datetime.fromisoformat("2024-12-07"), tick=False)
def test_upcoming_moments_cwmod():
    assert [
        x.strftime("%G-W%V") for x in moments("@cw 2", stop_at=dt.datetime(2025, 3, 1, tzinfo=ZoneInfo("UTC")))
    ] == [
        "2024-W48",
        "2024-W50",
        "2024-W52",
        "2025-W02",
        "2025-W04",
        "2025-W06",
        "2025-W08",
    ]


@time_machine.travel(dt.datetime.fromisoformat("2024-12-31T05:00:00+00:00"), tick=False)
def test_upcoming_moments_plus():
    assert [
        x.isoformat() for x in moments("/day + 3hours", stop_at=dt.datetime(2025, 1, 5, tzinfo=ZoneInfo("UTC")))
    ] == [
        "2024-12-31T03:00:00+00:00",
        "2025-01-01T03:00:00+00:00",
        "2025-01-02T03:00:00+00:00",
        "2025-01-03T03:00:00+00:00",
        "2025-01-04T03:00:00+00:00",
    ]


@time_machine.travel(dt.datetime.fromisoformat("2025-02-01T00:00:00+00:00"), tick=False)
def test_upcoming_moments_interval():
    assert [
        x.isoformat()
        for x in moments(
            "/hour", stop_at=dt.datetime(2025, 2, 1, 4, 0, tzinfo=ZoneInfo("UTC")), interval=timedelta(hours=1)
        )
    ] == [
        "2025-02-01T00:00:00+00:00",
        "2025-02-01T01:00:00+00:00",
        "2025-02-01T02:00:00+00:00",
        "2025-02-01T03:00:00+00:00",
        "2025-02-01T04:00:00+00:00",
    ]


def test_upcoming_moments_for_fixed_date():
    with pytest.raises(CronpellInputException, match=r".*"):
        next(moments("2024-11-29T12:12:04+03:00 /sat"))
