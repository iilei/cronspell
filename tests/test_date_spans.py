import datetime as dt

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
