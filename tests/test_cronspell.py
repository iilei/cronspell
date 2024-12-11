import datetime as dt
from zoneinfo import ZoneInfo

import pytest
import time_machine

from cronspell import parse
from cronspell.calendar_utils import map_matching_moments, matching_moments
from cronspell.exceptions import CronpellMathException


def test_iso_date():
    assert parse("2024-11-29T12:12:04+03:00 /sat -1 week +1d").isoformat() == "2024-11-17T00:00:00+03:00"


def test_tz_now():
    assert parse("now[Europe/Berlin] / m +3d /W").isoformat().rpartition("+")[-1] in {
        "01:00",
        "02:00",
    }


def test_blank():
    assert parse("").isoformat().rpartition("+")[-1] == "00:00"


def test_comment():
    assert (
        parse("2024-11-29T12:12:00+00:00 / month + 32 days / m -1 day /* get last day of this month */").isoformat()
        == "2024-11-30T00:00:00+00:00"
    )


def test_complex():
    assert (
        parse(
            """
                /* absurdly complex test case */
                2025-01-01
                / month + 32 days
                / m -1 day +1 second +3 minutes + 2 hours + 5 days
                    + 3 weeks
                /year /sat / sun /thu /mon /tue /fri /wed
                /week  /m /thu + 3 S + 169 M
            """
        ).isoformat()
        == "2024-11-28T02:49:03"
    )


# europe berlin equivalent for "2024-12-30T01:13:42+05:45"
@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T20:28:42+01:00"), tick=False)
def test_weekdays_and_timezones():
    assert parse("now[Asia/Kathmandu]").isoformat() == "2024-12-30T01:13:42+05:45"
    assert parse("now[Asia/Kathmandu] /d").isoformat() == "2024-12-30T00:00:00+05:45"
    assert parse("now[Asia/Kathmandu] /tue").isoformat() == "2024-12-24T00:00:00+05:45"
    assert parse("now[Asia/Kathmandu] /wed").isoformat() == "2024-12-25T00:00:00+05:45"
    assert parse("now[Asia/Kathmandu] /thu").isoformat() == "2024-12-26T00:00:00+05:45"
    assert parse("now[Asia/Kathmandu] /fri").isoformat() == "2024-12-27T00:00:00+05:45"
    assert parse("now[Asia/Kathmandu] /sat").isoformat() == "2024-12-28T00:00:00+05:45"

    assert parse("now[Asia/Kathmandu] /sun").isoformat() == "2024-12-29T00:00:00+05:45"

    assert parse("now[Asia/Kathmandu] /mon").isoformat() == parse("now[Asia/Kathmandu] /d").isoformat()


def test_cw_modulo():
    assert parse("2024-12-01T12:12:00+00:00 @cw 4").isoformat() == "2024-11-25T00:00:00+00:00"
    assert parse("2024-11-23T12:12:00+00:00 @ cw 4").isoformat() == "2024-10-28T00:00:00+00:00"
    assert parse(r"2024-11-23T12:12:00+00:00 % cw 4").isoformat() == "2024-10-28T00:00:00+00:00"
    assert parse(r"2024-11-23T12:12:00+00:00 % CW 4").isoformat() == "2024-10-28T00:00:00+00:00"


def test_y_modulo():
    assert parse("2024-12-01T00:00:00+00:00 @Y 4").isoformat() == "2024-01-01T00:00:00+00:00"
    assert parse("2024-12-01T00:00:00+00:00 @Y 5").isoformat() == "2020-01-01T00:00:00+00:00"


def test_examples():
    assert parse("2024-06-01T00:00:00+00:00 /sat").isoformat() == "2024-06-01T00:00:00+00:00"
    assert parse("2024-06-01T00:00:00+00:00 -1 day /sat + 1 week").isoformat() == "2024-06-01T00:00:00+00:00"
    assert parse("2024-06-01T00:00:00+00:00 -1 day /sun + 1 week").isoformat() == "2024-06-02T00:00:00+00:00"
    assert parse("2024-06-01T00:00:00+00:00 -1 day /mon + 1 week").isoformat() == "2024-06-03T00:00:00+00:00"
    assert parse("2024-06-01T00:00:00+00:00 -1 day /tue + 1 week").isoformat() == "2024-06-04T00:00:00+00:00"
    assert parse("2024-06-01T00:00:00+00:00 -1 day /wed + 1 week").isoformat() == "2024-06-05T00:00:00+00:00"
    assert parse("2024-06-01T00:00:00+00:00 -1 day /thu + 1 week").isoformat() == "2024-06-06T00:00:00+00:00"
    assert parse("2024-06-01T00:00:00+00:00 -1 day /fri + 1 week").isoformat() == "2024-06-07T00:00:00+00:00"


def test_cw_modulo_bad_input():
    with pytest.raises(CronpellMathException, match=r".*needed lower than 53.*"):
        assert parse("@cw 54").isoformat() == ""


@time_machine.travel(dt.datetime.fromisoformat("2025-01-21"), tick=False)
def test_matching_moments():
    assert matching_moments(
        map_matching_moments("/month", stop_at=dt.datetime(2025, 3, 1, tzinfo=ZoneInfo("UTC")))
    ) == [dt.datetime(2025, 1 + y, 1, tzinfo=ZoneInfo("UTC")) for y in range(0, 3)]
