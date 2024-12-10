from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from cronspell.cronspell import WEEKDAYS, Cronspell
from cronspell.exceptions import CronpellInputException

MAX_ITERATIONS = len(WEEKDAYS) * 53
MONDAY_IDX = WEEKDAYS.index("Mon")
SUNDAY_IDX = WEEKDAYS.index("Sun")


def _get_tzinfo(dt: datetime):
    return timetz.tzinfo if (timetz := dt.timetz()) else ZoneInfo(key="UTC")


def _get_day(dt: datetime):
    return datetime(*dt.timetuple()[0:3], tzinfo=_get_tzinfo(dt))


def get_result_for(expression: str, date: datetime):
    cronspell = Cronspell()
    cronspell.now_func = lambda *_: date
    return cronspell.parse(expression)


def matching_dates(
    expression: str, stop_at: datetime | None = None, initial_now: datetime | None = None
) -> Iterable[datetime]:
    cronspell = Cronspell()

    interval: timedelta = timedelta(days=1)

    cronspell.now_func = lambda *_: initial_now or datetime.now(tz=ZoneInfo("UTC"))
    initial = cronspell.parse(expression)

    cronspell.now_func = lambda *_: initial
    candidate = cronspell.parse(expression)

    _stop_at = stop_at or initial + timedelta(days=MAX_ITERATIONS)

    # fence for the event nothing else happens until the _stop_at
    if candidate == get_result_for(expression, _stop_at):
        msg = f"No 'next' match determined in time span {_stop_at.isoformat()}"
        raise CronpellInputException(msg)

    counter = 1

    while _get_day(initial) == _get_day(candidate) and (candidate <= _stop_at):
        yield cronspell._now_fun()

        cronspell.now_func = lambda *_, anchor=candidate, tick=counter: anchor + interval * tick

        candidate = cronspell.parse(expression)
        counter += 1
