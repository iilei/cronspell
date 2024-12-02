import datetime as dt

import time_machine

from cronspell import cronspell


def test_iso_date():
    assert cronspell("2024-11-29T12:12:04+03:00 /sat -1 week +1d").isoformat() == "2024-11-17T00:00:00+03:00"


def test_tz_now():
    assert cronspell("now[Europe/Berlin] / m +3d /W").isoformat().rpartition("+")[-1] in {
        "01:00",
        "02:00",
    }


def test_blank():
    assert cronspell("").isoformat().rpartition("+")[-1] == "00:00"


def test_comment():
    assert (
        cronspell("2024-11-29T12:12:00+00:00 / month + 32 days / m -1 day /* get last day of this month */").isoformat()
        == "2024-11-30T00:00:00+00:00"
    )


def test_complex():
    assert (
        cronspell(
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
    assert cronspell("now[Asia/Kathmandu]").isoformat() == "2024-12-30T01:13:42+05:45"
    assert cronspell("now[Asia/Kathmandu] /d").isoformat() == "2024-12-30T00:00:00+05:45"
    assert cronspell("now[Asia/Kathmandu] /tue").isoformat() == "2024-12-24T00:00:00+05:45"
    assert cronspell("now[Asia/Kathmandu] /wed").isoformat() == "2024-12-25T00:00:00+05:45"
    assert cronspell("now[Asia/Kathmandu] /thu").isoformat() == "2024-12-26T00:00:00+05:45"
    assert cronspell("now[Asia/Kathmandu] /fri").isoformat() == "2024-12-27T00:00:00+05:45"
    assert cronspell("now[Asia/Kathmandu] /sat").isoformat() == "2024-12-28T00:00:00+05:45"

    assert cronspell("now[Asia/Kathmandu] /sun").isoformat() == "2024-12-29T00:00:00+05:45"

    assert cronspell("now[Asia/Kathmandu] /mon").isoformat() == cronspell("now[Asia/Kathmandu] /d").isoformat()


def test_cw_modulo():
    assert cronspell("2024-12-01T12:12:00+00:00 @cw 4").isoformat() == "2024-12-01T00:00:00+00:00"
    assert cronspell("2024-11-23T12:12:00+00:00 @ cw 4").isoformat() == "2024-11-02T00:00:00+00:00"
    assert cronspell(r"2024-11-23T12:12:00+00:00 % cw 4").isoformat() == "2024-11-02T00:00:00+00:00"
    assert cronspell(r"2024-11-23T12:12:00+00:00 % CW 4").isoformat() == "2024-11-02T00:00:00+00:00"


def test_examples():
    assert cronspell("2024-06-01T00:00:00+00:00 /sat").isoformat() == "2024-06-01T00:00:00+00:00"
    assert cronspell("2024-06-01T00:00:00+00:00 -1 day /sat + 1 week").isoformat() == "2024-06-01T00:00:00+00:00"
    assert cronspell("2024-06-01T00:00:00+00:00 -1 day /sun + 1 week").isoformat() == "2024-06-02T00:00:00+00:00"
    assert cronspell("2024-06-01T00:00:00+00:00 -1 day /mon + 1 week").isoformat() == "2024-06-03T00:00:00+00:00"
    assert cronspell("2024-06-01T00:00:00+00:00 -1 day /tue + 1 week").isoformat() == "2024-06-04T00:00:00+00:00"
    assert cronspell("2024-06-01T00:00:00+00:00 -1 day /wed + 1 week").isoformat() == "2024-06-05T00:00:00+00:00"
    assert cronspell("2024-06-01T00:00:00+00:00 -1 day /thu + 1 week").isoformat() == "2024-06-06T00:00:00+00:00"
    assert cronspell("2024-06-01T00:00:00+00:00 -1 day /fri + 1 week").isoformat() == "2024-06-07T00:00:00+00:00"
