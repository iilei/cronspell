from __future__ import annotations

from collections.abc import Generator
from datetime import datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

from cronspell.cronspell import WEEKDAYS, Cronspell
from cronspell.exceptions import CronpellInputException

MAX_ITERATIONS = 64
MONDAY_IDX = WEEKDAYS.index("Mon")
SUNDAY_IDX = WEEKDAYS.index("Sun")


def get_result_for(expression: str, date: datetime):
    cronspell = Cronspell()
    cronspell.now_func = lambda *_: date
    return cronspell.parse(expression)


MomentMap = tuple[datetime, datetime]


def map_moments(
    expression: str,
    interval: timedelta = timedelta(days=1),
    initial_now: datetime | None = None,
    stop_at: datetime | None = None,
) -> Generator[MomentMap, Any, Any]:
    cronspell = Cronspell()

    initial: datetime = get_result_for(expression, initial_now or datetime.now(tz=ZoneInfo("UTC")))
    candidate: datetime = get_result_for(expression, initial)

    cronspell.now_func = lambda *_: initial
    counter = 1

    # safeguard against the event of no difference at the end of the time span
    if candidate == get_result_for(expression, (_stop_at := (stop_at or initial + timedelta(days=MAX_ITERATIONS)))):
        msg = f"Not going to find a span of matching dates until {_stop_at.isoformat()} with `{expression}`"
        raise CronpellInputException(msg)

    while candidate <= _stop_at:
        yield (candidate, cronspell._now_fun())

        # alter the "now" function each iteration ~> time moving forward
        cronspell.now_func = lambda *_, anchor=initial, tick=counter: anchor + interval * tick

        candidate = cronspell.parse(expression)
        counter += 1


def moments(
    expression: str,
    interval: timedelta = timedelta(days=1),
    initial_now: datetime | None = None,
    stop_at: datetime | None = None,
) -> Generator[datetime, Any, Any]:
    mapper = map_moments(expression=expression, interval=interval, initial_now=initial_now, stop_at=stop_at)

    exhausted = False
    while not exhausted:
        moment, comparison = next(mapper, [None, None])
        if not moment:
            exhausted = True
        elif moment == comparison:
            yield moment
