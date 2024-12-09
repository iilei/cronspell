from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from cronspell.cronspell import WEEKDAYS, Cronspell

MAX_ITERATIONS = len(WEEKDAYS) * 53
MONDAY_IDX = WEEKDAYS.index("Mon")
SUNDAY_IDX = WEEKDAYS.index("Sun")


def _get_tzinfo(dt: datetime):
    return timetz.tzinfo if (timetz := dt.timetz()) else ZoneInfo(key="UTC")


def _get_day(dt: datetime):
    return datetime(*dt.timetuple()[0:3], tzinfo=_get_tzinfo(dt))


def dates_belonging_to(
    expression: str, stop_at: datetime | None = None, initial_now: datetime | None = None
) -> Iterable[datetime]:
    cronspell = Cronspell()

    interval: timedelta = timedelta(days=1)

    cronspell.now_func = lambda *_: initial_now or datetime.now(tz=ZoneInfo("UTC"))
    initial = cronspell.parse(expression)

    cronspell.now_func = lambda *_: initial
    candidate = cronspell.parse(expression)

    _stop_at = stop_at or initial + timedelta(days=MAX_ITERATIONS)

    counter = 1

    while _get_day(initial) == _get_day(candidate) and (candidate <= _stop_at):
        yield cronspell._now_fun()

        cronspell.now_func = lambda *_, anchor=candidate, tick=counter: anchor + interval * tick

        candidate = cronspell.parse(expression)
        counter += 1
