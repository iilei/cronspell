from __future__ import annotations

from collections.abc import Iterable
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from cronspell.cronspell import WEEKDAYS, Cronspell
from cronspell.exceptions import CronpellInputException

MAX_ITERATIONS = len(WEEKDAYS) * 53
MONDAY_IDX = WEEKDAYS.index("Mon")
SUNDAY_IDX = WEEKDAYS.index("Sun")


def get_result_for(expression: str, date: datetime):
    cronspell = Cronspell()
    cronspell.now_func = lambda *_: date
    return cronspell.parse(expression)


def map_matching_moments(
    expression: str,
    interval: timedelta = timedelta(days=1),
    initial_now: datetime | None = None,
    stop_at: datetime | None = None,
) -> Iterable[tuple[datetime, datetime]]:
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


def matching_moments(generator: Iterable[tuple[datetime, datetime]]):
    return [x[0] for x in [*generator] if x[0] == x[1]]
