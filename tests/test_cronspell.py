import datetime as dt

import time_machine

from cronspell import resolve


def test_iso_date():
    assert resolve("2024-11-29T12:12:04+03:00 /sat -1 week +1d").isoformat() == "2024-11-17T00:00:00+03:00"


def test_tz_now():
    assert resolve("now[Europe/Berlin] / m +3d /W").isoformat().rpartition("+")[-1] in {
        "01:00",
        "02:00",
    }


def test_blank():
    assert resolve("").isoformat().rpartition("+")[-1] == "00:00"


def test_comment():
    assert (
        resolve("2024-11-29T12:12:00+00:00 / month + 32 days / m -1 day /* get last day of this month */").isoformat()
        == "2024-11-30T00:00:00+00:00"
    )


def test_complex():
    assert (
        resolve(
            """
                /* absurdly complex test case */
                2025-01-01
                / month + 32 days
                / m -1 day +1 second +3 minutes + 2 hours + 5 days
                    + 3 weeks + 2 months + 3 years
                /year /sat / sun /thu /mon /tue /fri /wed
                /week + 1 m /m /thu + 3 S + 169 M
            """
        ).isoformat()
        == "2027-11-25T02:49:03"
    )


@time_machine.travel(dt.datetime.fromisoformat("2024-12-31T01:13:42+05:45"), tick=False)
def test_weekdays():
    assert resolve("now").isoformat() == "2024-12-31T01:13:42+05:45"
    assert resolve("now /d").isoformat() == "2024-12-31T00:00:00+05:45"
    assert resolve("now /tue").isoformat() == "2024-12-31T00:00:00+05:45"
    assert resolve("now /mon").isoformat() == "2024-12-30T00:00:00+05:45"
    assert resolve("now /sun").isoformat() == "2024-12-29T00:00:00+05:45"
    assert resolve("now /sat").isoformat() == "2024-12-28T00:00:00+05:45"
    assert resolve("now /fri").isoformat() == "2024-12-27T00:00:00+05:45"
    assert resolve("now /thu").isoformat() == "2024-12-26T00:00:00+05:45"
    assert resolve("now /wed").isoformat() == "2024-12-25T00:00:00+05:45"
