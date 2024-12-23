from __future__ import annotations

from collections.abc import Generator
from datetime import datetime, timedelta
from typing import Any
from zoneinfo import ZoneInfo

from cronspell.cronspell import WEEKDAYS, Cronspell

MAX_ITERATIONS = 350
MONDAY_IDX = WEEKDAYS.index("Mon")
SUNDAY_IDX = WEEKDAYS.index("Sun")


def get_result_for(expression: str, date: datetime):
    cronspell = Cronspell()
    cronspell.now_func = lambda *_: date
    return cronspell.parse(expression)


MomentMap = tuple[datetime, datetime]


def has_isodate_anchor(expression: str):
    cronspell = Cronspell()
    cronspell.parse(expression)

    anchor = getattr(cronspell.model, "anchor", None)
    return bool(getattr(anchor, "isodate", False))


def map_moments(
    expression: str,
    interval: timedelta = timedelta(days=1),
    initial_now: datetime | None = None,
    stop_at: datetime | None = None,
) -> Generator[MomentMap, Any, Any]:
    cronspell = Cronspell()

    initial: datetime = get_result_for(expression, initial_now or datetime.now(tz=ZoneInfo("UTC")))

    candidate: datetime = initial
    cronspell.now_func = lambda *_: initial
    counter = 1

    stop_at = stop_at or initial + timedelta(days=MAX_ITERATIONS)

    while candidate <= stop_at:
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
    min_moment = datetime.now(tz=ZoneInfo("UTC"))
    all_same = has_isodate_anchor(expression)
    mapper = map_moments(expression=expression, interval=interval, initial_now=initial_now, stop_at=stop_at)

    exhausted = False
    while not exhausted:
        moment, comparison = next(mapper, [None, None])

        if all_same or not moment:
            exhausted = True
        if moment and moment == comparison and moment > min_moment:
            yield moment
