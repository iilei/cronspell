import datetime as dt
from datetime import timedelta
from zoneinfo import ZoneInfo

import time_machine

from cronspell.upcoming import moments


@time_machine.travel(dt.datetime.fromisoformat("2025-01-21"), tick=False)
def test_upcoming_moments():
    assert [*moments("/month", stop_at=dt.datetime(2025, 3, 1, tzinfo=ZoneInfo("UTC")))] == [
        dt.datetime(2025, 2, 1, 0, 0, tzinfo=ZoneInfo(key="UTC")),
        dt.datetime(2025, 3, 1, 0, 0, tzinfo=ZoneInfo(key="UTC")),
    ]


@time_machine.travel(dt.datetime.fromisoformat("2024-12-07"), tick=False)
def test_upcoming_moments_cwmod():
    assert [
        x.strftime("%G-W%V") for x in moments("@cw 2", stop_at=dt.datetime(2025, 3, 1, tzinfo=ZoneInfo("UTC")))
    ] == [
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
        "2025-02-01T01:00:00+00:00",
        "2025-02-01T02:00:00+00:00",
        "2025-02-01T03:00:00+00:00",
        "2025-02-01T04:00:00+00:00",
    ]


def test_upcoming_moments_for_fixed_date():
    assert next(moments("2024-11-29T12:12:04+03:00 /sat"), None) is None


@time_machine.travel(dt.datetime.fromisoformat("2025-01-21T19:28:42+00:00"), tick=False)
def test_upcoming_moments_interval_cw_modulo_gt_current():
    assert [
        x.strftime("%G-W%V")
        for x in moments(
            "@cw 5", stop_at=dt.datetime(2026, 1, 30, 1, 0, tzinfo=ZoneInfo("UTC")), interval=timedelta(days=7)
        )
    ] == [
        "2025-W05",
        "2025-W10",
        "2025-W15",
        "2025-W20",
        "2025-W25",
        "2025-W30",
        "2025-W35",
        "2025-W40",
        "2025-W45",
        "2025-W50",
        "2026-W05",
    ]


@time_machine.travel(dt.datetime.fromisoformat("2024-12-30T00:00:00+00:00"), tick=False)
def test_python_example_next_cw3_b():
    cw3 = moments("@cw 3")

    """
    In the 21st century, the 53-week broadcasting calendar years are
    2006, 2012, 2017, 2023, 2028, 2034, 2040, 2045, 2051, 2056, 2062, 2068, 2073, 2079, 2084, 2090 and 2096.

    Hence, this test case covers an edgge case with determining upcoming occurrences.
    """
    # info: start is 2024-12-30 which is iso week 2025-W01
    assert dt.datetime.fromisoformat("2024-12-30").strftime("%G-W%V") == "2025-W01"

    assert next(cw3).strftime("%G-W%V") == "2025-W03"
    assert next(cw3).strftime("%G-W%V") == "2025-W06"
    assert next(cw3).strftime("%G-W%V") == "2025-W09"
