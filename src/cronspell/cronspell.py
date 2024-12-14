# SPDX-FileCopyrightText: 2024-present iilei • jochen preusche <922226+iilei@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT


import calendar
import functools
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Optional
from zoneinfo import ZoneInfo

from textx import metamodel_from_file

from cronspell.exceptions import CronpellMathException

with calendar.different_locale(locale=("EN_US", "UTF-8")):
    # first day of the week: Monday as per ISO Standard
    WEEKDAYS = [*calendar.day_abbr]


TIME_UNITS_SHORT = ["Y", "m", "CW", "W", "d", "H", "M", "S"]
TIME_RESETS = [
    ("year", 1970),
    ("month", 1),
    None,
    None,
    ("day", 1),
    ("minute", 0),
    ("hour", 0),
    ("second", 0),
]
TIME_RESETS_MAP = [[TIME_UNITS_SHORT[k], v] for k, v in enumerate(TIME_RESETS) if v]
FLOOR_CW_MAX = 52
FLOOR_Y_MAX = 9999


class Cronspell:
    def __init__(self, timezone: Optional[ZoneInfo] = None):
        if timezone is None:
            timezone = ZoneInfo("UTC")

        self.meta_model_src = Path.joinpath(Path(__file__).parent, "cronspell.tx")
        self.meta_model = metamodel_from_file(self.meta_model_src, use_regexp_group=True)
        self.timezone = timezone
        self._now_fun = datetime.now

    def parse_anchor(self):
        if (anchor := getattr(self.model, "anchor", None)) and ((tznow := anchor.tznow) or (isodate := anchor.isodate)):
            return (
                self._now_fun().astimezone(ZoneInfo(tznow.tz))
                if (tznow and tznow.tz)
                else datetime.fromisoformat(isodate)
            )

        return self._now_fun(self.timezone)

    @property
    def now_func(self) -> Callable[..., datetime]:
        return self._now_fun

    @now_func.setter
    def now_func(self, fun: Callable[..., datetime]):
        self._now_fun = fun

    @staticmethod
    def get_time_unit(alias):
        return next(name for name in [*TIME_UNITS_SHORT, *WEEKDAYS] if getattr(alias, name, None))

    def step(self, current, step):
        # operation ~> Minus|Plus|Floor|Ceil
        operation = step.statement._tx_fqn.rpartition(".")[-1]

        # Year Modulo
        if operation == "YModulo":
            resolution = max(step.statement.value, 1)

            if resolution > FLOOR_Y_MAX:
                msg = f"Year Modulo needed lower than {FLOOR_Y_MAX + 1}! Got {resolution}."
                raise CronpellMathException(msg)

            year = current.isocalendar().year // resolution * resolution

            return datetime(year, 1, 1, tzinfo=self.timezone)

        # Calendar Week Modulo
        elif operation == "CwModulo":
            resolution = max(step.statement.value, 1)

            if resolution > FLOOR_CW_MAX:
                msg = f"Calendar Week Modulo needed lower than {FLOOR_CW_MAX + 1}! Got {resolution}."
                raise CronpellMathException(msg)

            # find date in isoweek matching the desired resolution
            current = next(
                filter(
                    lambda date: date.isocalendar().week % resolution == 0,
                    [current - timedelta(days=(7 * x)) for x in range(0, resolution + 1)],
                )
            )

            # operation "Floor" yet to be performed
            operation = "Floor"
            resolution = "WeekDay"
            time_unit = WEEKDAYS[0]
        else:
            resolution = step.statement.res._tx_fqn.rpartition(".")[-1]
            time_unit = self.get_time_unit(step.statement.res)

        if operation in {"Plus", "Minus"}:
            # special case: week ~> 7 days
            if time_unit == "W":
                delta = (datetime.strptime("2", "%d") - datetime.strptime("1", "%d")) * (
                    (-7 if operation == "Minus" else 7) * step.statement.steps
                )
            else:
                lower_value = [x for x in TIME_RESETS_MAP if x[0] == time_unit].pop()[1][1]

                delta = (
                    datetime.strptime(str(lower_value + 2), f"%{time_unit}")
                    - datetime.strptime(str(lower_value + 1), f"%{time_unit}")
                ) * ((-1 if operation == "Minus" else 1) * step.statement.steps)

            return current + delta

        elif operation == "Floor" and resolution == "WeekDay":
            offset_abs = (7 + (current.weekday() - WEEKDAYS.index(time_unit))) % 7
            offset = -1 * offset_abs if operation == "Floor" else 7 - offset_abs
            current += timedelta(days=offset)

            # operation "Floor" to be performed as per day
            time_unit = "d"

        if operation == "Floor":
            prune = TIME_UNITS_SHORT[TIME_UNITS_SHORT.index(time_unit) + 1 :]

            current = current.replace(**dict([x[1] for x in TIME_RESETS_MAP if x[0] in prune]))

            return current

    def parse(self, expression: str = "now") -> datetime:
        self.expression = expression
        self.model = self.meta_model.model_from_str(expression)
        self.anchor = self.parse_anchor().replace(microsecond=0)

        self.tz = self.anchor.tzname()

        result = functools.reduce(self.step, [*getattr(self.model, "date_math_term", [])], self.anchor)

        return result
