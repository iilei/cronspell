import datetime as dt
from zoneinfo import ZoneInfo

import time_machine

from cronspell import parse, upcoming


def test_irregular_schedules():
    with time_machine.travel(dt.datetime(2024, 12, 25, tzinfo=ZoneInfo("UTC"))):
        assert parse("{/sun, /m+5d, /m+10d}").isoformat() == "2024-12-22T00:00:00+00:00"
        assert parse("{/m+5d, /m+10d, /sun}").isoformat() == "2024-12-22T00:00:00+00:00"
        assert parse("{/m+5d, /sun, /m+10d}").isoformat() == "2024-12-22T00:00:00+00:00"
        assert parse("{/m+10d, /m+5d, /sun}").isoformat() == "2024-12-22T00:00:00+00:00"

        assert parse("{/m+5d, /m+10d}").isoformat() == "2024-12-11T00:00:00+00:00"

    with time_machine.travel(dt.datetime(2024, 12, 7, tzinfo=ZoneInfo("UTC"))):
        assert parse("{/sun, /m+4d}").isoformat() == "2024-12-05T00:00:00+00:00"


def test_irregular_schedules_upcoming():
    stop_at = dt.datetime(2025, 1, 13, tzinfo=ZoneInfo("UTC"))
    with time_machine.travel(dt.datetime(2024, 12, 7, tzinfo=ZoneInfo("UTC"))):
        assert [
            x.strftime("%G-W%V, %a %m-%d") for x in upcoming.moments("{/sun, /sat, @cw 3 + 2d}", stop_at=stop_at)
        ] == [
            "2024-W49, Sun 12-08",
            "2024-W50, Sat 12-14",
            "2024-W50, Sun 12-15",
            "2024-W51, Wed 12-18",
            "2024-W51, Sat 12-21",
            "2024-W51, Sun 12-22",
            "2024-W52, Sat 12-28",
            "2024-W52, Sun 12-29",
            "2025-W01, Sat 01-04",
            "2025-W01, Sun 01-05",
            "2025-W02, Sat 01-11",
            "2025-W02, Sun 01-12",
        ]


def test_irregular_schedules_upcoming_edge_case():
    stop_at = dt.datetime(2025, 6, 1, tzinfo=ZoneInfo("UTC"))
    with time_machine.travel(dt.datetime(2024, 12, 24, tzinfo=ZoneInfo("UTC"))):
        assert [
            x.strftime("%G-W%V, %a %m-%d")
            for x in upcoming.moments("{@cw 3 /sun + 7d, @cw 5 /fri + 7d}", stop_at=stop_at)
        ] == [
            "2025-W03, Sun 01-19",
            "2025-W05, Fri 01-31",
            "2025-W06, Sun 02-09",
            "2025-W09, Sun 03-02",
            "2025-W10, Fri 03-07",
            "2025-W12, Sun 03-23",
            "2025-W15, Sun 04-13",
            "2025-W18, Sun 05-04",
            "2025-W20, Fri 05-16",
            "2025-W21, Sun 05-25",
        ]
