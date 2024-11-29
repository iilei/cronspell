# SPDX-FileCopyrightText: 2024-present iilei • jochen preusche <922226+iilei@users.noreply.github.com>
#
# SPDX-License-Identifier: MIT


import calendar
import functools
from datetime import datetime, timedelta
from pathlib import Path
from typing import Union
from zoneinfo import ZoneInfo

from textx import metamodel_from_file

with calendar.different_locale(locale=("EN_US", "UTF-8")):
    # first day of the week: Monday as per ISO Standard
    WEEKDAYS = [*calendar.day_abbr]


TIME_UNITS_SHORT = ["Y", "m", "W", "d", "H", "M", "S"]
TIME_RESETS = [
    ("year", 1970),
    ("month", 1),
    None,
    ("day", 1),
    ("minute", 0),
    ("hour", 0),
    ("second", 0),
]
TIME_RESETS_MAP = [[TIME_UNITS_SHORT[k], v] for k, v in enumerate(TIME_RESETS) if v]


class Cronspell:
    def __init__(self):
        self.meta_model = metamodel_from_file(
            Path.joinpath(Path(__file__).parent, "cronspell.tx"), use_regexp_group=True
        )

        self.timezone = ZoneInfo("UTC")
        self.now = datetime.now(self.timezone)
        self.result = self.now

    def parse_anchor(self):
        if (anchor := getattr(self.model, "anchor", None)) and ((tznow := anchor.tznow) or (isodate := anchor.isodate)):
            return datetime.now(ZoneInfo(tznow.tz)) if (tznow and tznow.tz) else datetime.fromisoformat(isodate)

        return datetime.now(ZoneInfo("UTC"))

    @staticmethod
    def get_time_unit(res):
        return [
            "d",
            *[y for y in [x for x in [*TIME_UNITS_SHORT, *WEEKDAYS] if getattr(res, x, None)] if y],
        ].pop()

    def step(self, current, step):
        if step._tx_fqn.rpartition(".")[-1] == "DateMathTerm":
            # operation ~> Minus|Plus|Floor|Ceil
            operation = step.statement._tx_fqn.rpartition(".")[-1]
            # "TimeUnitShort" or "Weekday"
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
                assert current.weekday() == WEEKDAYS.index(time_unit)

                # operation "Floor" to be performed as per day
                time_unit = "d"

            if operation == "Floor":
                prune = TIME_UNITS_SHORT[TIME_UNITS_SHORT.index(time_unit) + 1 :]

                current = current.replace(**dict([x[1] for x in TIME_RESETS_MAP if x[0] in prune]))

                return current

        return current

    def parse(self, expression: str = "now", now: Union[None, datetime] = None):
        self.expression = expression
        self.model = self.meta_model.model_from_str(expression)
        self.anchor = self.parse_anchor()

        result = functools.reduce(self.step, [*getattr(self.model, "date_math_term", [])], self.anchor)

        return result
