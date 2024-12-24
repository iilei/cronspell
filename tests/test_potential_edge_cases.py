import datetime as dt
from zoneinfo import ZoneInfo

import time_machine

from cronspell import parse

date_x = dt.datetime.fromisoformat("2030-01-01T19:28:42:471100+00:00")


def test_long_term_usage_calendar_week_modulo():
    """
    Plausibility testing for executions within the next 25 years, about 13 times each year,
    finding calendar week modulo 23
    """
    for date in [date_x + dt.timedelta(days=x) for x in range(0, 365 * 25, 27)]:
        with time_machine.travel(date):
            assert None is not parse("@cw 23")
            assert parse("@cw") == parse("/mon")


def test_cet_to_cest_jump():
    with time_machine.travel(
        dt.datetime(2025, 3, 30, 1, 58, tzinfo=ZoneInfo("Europe/Berlin")), tick=False
    ) as traveller:
        assert parse("now[Europe/Berlin] + 1 minute").isoformat() == "2025-03-30T01:59:00+01:00"

        traveller.shift(60)
        assert parse("now[Europe/Berlin] + 1 minute").isoformat() == "2025-03-30T02:00:00+01:00"

        # note the applied offset due to cet / cest jump
        traveller.shift(60)
        assert parse("now[Europe/Berlin] + 1 minute").isoformat() == "2025-03-30T03:01:00+02:00"


def test_cest_to_cet_jump():
    initial = dt.datetime(2025, 10, 26, 2, 59, tzinfo=ZoneInfo("Europe/Berlin"))

    with time_machine.travel(initial, tick=False) as traveller:
        moment_a = parse("now[Europe/Berlin] -30 seconds + 30 seconds")
        assert moment_a.isoformat() == "2025-10-26T02:59:00+02:00"

        traveller.shift(dt.timedelta(minutes=61))
        moment_b = parse("now[Europe/Berlin] -30 seconds + 30 seconds")
        assert moment_b.isoformat() == "2025-10-26T03:00:00+01:00"

        assert (moment_b.astimezone(tz=ZoneInfo("UTC")) - moment_a.astimezone(tz=ZoneInfo("UTC"))) == dt.timedelta(
            minutes=61
        )

        assert moment_a.timetz().tzinfo.key == moment_b.timetz().tzinfo.key == "Europe/Berlin"
