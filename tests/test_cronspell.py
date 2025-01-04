import datetime as dt
from unittest.mock import MagicMock, Mock
from zoneinfo import ZoneInfo

import pytest
import time_machine

from cronspell import Cronspell, parse
from cronspell.exceptions import CronpellMathException


def test_iso_date():
    assert parse("2024-12-29T19:28:42+00:00").isoformat() == "2024-12-29T19:28:42+00:00"


def test_tz_now():
    assert parse("now[Europe/Berlin] / m +3d /W").isoformat().rpartition("+")[-1] in {
        "01:00",
        "02:00",
    }


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42:471100+00:00"), tick=False)
def test_day_math():
    expected = "2025-01-01T19:28:42+00:00"
    assert parse("+3days").isoformat() == expected
    assert parse("+3day").isoformat() == expected
    assert parse("+3d").isoformat() == expected
    assert parse("+ 3days").isoformat() == expected
    assert parse("+ 3day").isoformat() == expected
    assert parse("+ 3d").isoformat() == expected
    assert parse("+ 3 days").isoformat() == expected
    assert parse("+ 3 day").isoformat() == expected
    assert parse("+ 3 d").isoformat() == expected
    assert parse("+3 days").isoformat() == expected
    assert parse("+3 day").isoformat() == expected
    assert parse("+3 d").isoformat() == expected


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42:471100+00:00"), tick=False)
def test_hour_math():
    expected = "2024-12-29T22:28:42+00:00"
    assert parse("+3hours").isoformat() == expected
    assert parse("+3hour").isoformat() == expected
    assert parse("+3Hrs").isoformat() == expected
    assert parse("+3hrs").isoformat() == expected
    assert parse("+3H").isoformat() == expected
    assert parse("+ 3hours").isoformat() == expected
    assert parse("+ 3hour").isoformat() == expected
    assert parse("+ 3Hrs").isoformat() == expected
    assert parse("+ 3hrs").isoformat() == expected
    assert parse("+ 3H").isoformat() == expected
    assert parse("+ 3 hours").isoformat() == expected
    assert parse("+ 3 hour").isoformat() == expected
    assert parse("+ 3 Hrs").isoformat() == expected
    assert parse("+ 3 hrs").isoformat() == expected
    assert parse("+ 3 H").isoformat() == expected
    assert parse("+3 hours").isoformat() == expected
    assert parse("+3 hour").isoformat() == expected
    assert parse("+3 Hrs").isoformat() == expected
    assert parse("+3 hrs").isoformat() == expected
    assert parse("+3 H").isoformat() == expected


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42:471100+00:00"), tick=False)
def test_minute_math():
    expected = "2024-12-29T19:31:42+00:00"
    assert parse("+3minutes").isoformat() == expected
    assert parse("+3minute").isoformat() == expected
    assert parse("+3min").isoformat() == expected
    assert parse("+3Min").isoformat() == expected
    assert parse("+3M").isoformat() == expected
    assert parse("+ 3 minutes").isoformat() == expected
    assert parse("+ 3 minute").isoformat() == expected
    assert parse("+ 3 min").isoformat() == expected
    assert parse("+ 3 Min").isoformat() == expected
    assert parse("+ 3 M").isoformat() == expected
    assert parse("+ 3minutes").isoformat() == expected
    assert parse("+ 3minute").isoformat() == expected
    assert parse("+ 3min").isoformat() == expected
    assert parse("+ 3Min").isoformat() == expected
    assert parse("+ 3M").isoformat() == expected
    assert parse("+3 minutes").isoformat() == expected
    assert parse("+3 minute").isoformat() == expected
    assert parse("+3 min").isoformat() == expected
    assert parse("+3 Min").isoformat() == expected
    assert parse("+3 M").isoformat() == expected


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42:471100+00:00"), tick=False)
def test_second_math():
    expected = "2024-12-29T19:28:45+00:00"
    assert parse("+3seconds").isoformat() == expected
    assert parse("+3second").isoformat() == expected
    assert parse("+3S").isoformat() == expected
    assert parse("+3sec").isoformat() == expected
    assert parse("+ 3seconds").isoformat() == expected
    assert parse("+ 3second").isoformat() == expected
    assert parse("+ 3S").isoformat() == expected
    assert parse("+ 3sec").isoformat() == expected
    assert parse("+3 seconds").isoformat() == expected
    assert parse("+3 second").isoformat() == expected
    assert parse("+3 S").isoformat() == expected
    assert parse("+3 sec").isoformat() == expected
    assert parse("+ 3 seconds").isoformat() == expected
    assert parse("+ 3 second").isoformat() == expected
    assert parse("+ 3 S").isoformat() == expected
    assert parse("+ 3 sec").isoformat() == expected


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42:471100+00:00"), tick=False)
def test_hour_floor():
    assert parse("/hour").isoformat() == "2024-12-29T19:00:00+00:00"


def test_blank():
    assert parse("").isoformat().rpartition("+")[-1] == "00:00"


def test_comment():
    assert (
        parse("2024-11-29T12:12:00+00:00 / month + 32 days / m -1 day /* get last day of this month */").isoformat()
        == "2024-11-30T00:00:00+00:00"
    )


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T20:28:42:471100+01:00"), tick=False)
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
        parse("@cw 54").isoformat()


def test_year_modulo_bad_input():
    with pytest.raises(CronpellMathException, match=r".*Year Modulo needed lower than .*Got.*"):
        parse("@year 10000").isoformat()


def test_month_modulo_bad_input():
    with pytest.raises(CronpellMathException, match=r".*Month Modulo needed lower than .*Got.*"):
        parse("@m 13").isoformat()


def test_now_fun():
    dtmock = MagicMock()
    dtmock.return_value = dt.datetime.fromisoformat("2022-12-29T20:28:42+00:00")
    cronspell = Cronspell()
    cronspell.now_func = dtmock
    assert cronspell.now_func == dtmock


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42:471100+00:00"), tick=False)
def test_year_floor():
    assert parse("/year").isoformat() == "2024-01-01T00:00:00+00:00"


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42:471100+00:00"), tick=False)
def test_month_floor():
    assert parse("/month").isoformat() == "2024-12-01T00:00:00+00:00"
    assert parse("/m").isoformat() == "2024-12-01T00:00:00+00:00"


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42:471100+00:00"), tick=False)
def test_day_floor():
    assert parse("/day").isoformat() == "2024-12-29T00:00:00+00:00"


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42+00:00"), tick=False)
def test_timezone_now():
    assert parse("now[UTC]").isoformat() == "2024-12-29T19:28:42+00:00"


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42+00:00"), tick=False)
def test_floor_operation():
    assert parse("now /d").isoformat() == "2024-12-29T00:00:00+00:00"


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42+00:00"), tick=False)
def test_plus_operation():
    assert parse("now +3d").isoformat() == "2025-01-01T19:28:42+00:00"


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42+00:00"), tick=False)
def test_minus_operation():
    assert parse("now -3d").isoformat() == "2024-12-26T19:28:42+00:00"


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42+00:00"), tick=False)
def test_cw_modulo():
    assert parse("now @cw").isoformat() == "2024-12-23T00:00:00+00:00"
    assert parse("now %cw").isoformat() == "2024-12-23T00:00:00+00:00"


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42+00:00"), tick=False)
def test_y_modulo():
    assert parse("now @y").isoformat() == "2024-01-01T00:00:00+00:00"
    assert parse("now %y").isoformat() == "2024-01-01T00:00:00+00:00"


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42+00:00"), tick=False)
def test_weekday_parsing():
    assert parse("now /sat").isoformat() == "2024-12-28T00:00:00+00:00"


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42+00:00"), tick=False)
def test_parse_anchor_with_tznow():
    cronspell = Cronspell()
    cronspell.model = MagicMock()
    cronspell.model.anchor = MagicMock()
    cronspell.model.anchor.tznow = MagicMock()
    cronspell.model.anchor.tznow.tz = "Europe/Berlin"
    cronspell.model.anchor.isodate = None

    with time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42+00:00"), tick=False):
        result = cronspell.parse_anchor()
        assert result.isoformat() == "2024-12-29T20:28:42+01:00"


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42+00:00"), tick=False)
def test_parse_anchor_with_isodate():
    cronspell = Cronspell()
    cronspell.model = MagicMock()
    cronspell.model.anchor = MagicMock()
    cronspell.model.anchor.tznow = None
    cronspell.model.anchor.isodate = "2024-12-29T19:28:42+00:00"

    result = cronspell.parse_anchor()
    assert result.isoformat() == "2024-12-29T19:28:42+00:00"


def test_parse_anchor_passed_timezone():
    assert Cronspell(timezone=ZoneInfo("Asia/Kathmandu")).parse("now").tzinfo.key == "Asia/Kathmandu"


def test_parse_anchor_passed_timezone_conficting():
    cronspell = Cronspell(timezone=ZoneInfo("Asia/Kathmandu"))

    assert cronspell.parse("now[Europe/Berlin]").tzinfo.key == "Europe/Berlin"


def test_parse_anchor_default_timezone():
    assert Cronspell().parse("now").tzinfo.key == "UTC"


def test_edge_case_no_anchor():
    cronspell = Cronspell()
    cronspell.model = MagicMock()
    cronspell.model.anchor = None

    assert cronspell.parse("/d").hour == 0


def test_edge_case_no_tznow_tz():
    cronspell = Cronspell()
    cronspell.model = MagicMock()
    cronspell.model.anchor = MagicMock()
    cronspell.model.anchor.tznow = Mock()
    cronspell.model.anchor.isodate = "2024-12-29T19:28:42+00:00"

    assert cronspell.parse("/d").hour == 0


def test_property_now_func():
    now_fun = MagicMock()
    now_fun.return_value = dt.datetime.fromisoformat("2024-12-29T00:00:00:000000+01:23")

    cronspell = Cronspell()
    cronspell.now_func = now_fun
    cronspell.now_func()
    assert len(now_fun.mock_calls) == 1

    assert cronspell.parse("now") == now_fun.return_value


@time_machine.travel(dt.datetime.fromisoformat("2024-12-21T19:28:42+00:00"), tick=False)
def test_cw_modulo_big():
    assert parse("@cw 4").strftime("%G-W%V") == "2024-W48"
    assert parse("@cw 5").strftime("%G-W%V") == "2024-W50"
    assert parse("@cw 6").strftime("%G-W%V") == "2024-W48"
    assert parse("@cw 7").strftime("%G-W%V") == "2024-W49"
    assert parse("@cw 11").strftime("%G-W%V") == "2024-W44"
    assert parse("@cw 12").strftime("%G-W%V") == "2024-W48"
    assert parse("@cw 13").strftime("%G-W%V") == "2024-W39"
    assert parse("@cw 14").strftime("%G-W%V") == "2024-W42"
    assert parse("@cw 15").strftime("%G-W%V") == "2024-W45"
    assert parse("@cw 16").strftime("%G-W%V") == "2024-W48"


@time_machine.travel(dt.datetime.fromisoformat("2024-12-21T19:28:42+00:00"), tick=False)
def test_cw_modulo_and_floor_to_day_name():
    assert parse("@cw 4 / sat").strftime("%a %G-W%V") == "Sat 2024-W47"


@time_machine.travel(dt.datetime.fromisoformat("2024-11-21T19:28:42+00:00"), tick=False)
def test_month_modulo():
    assert parse("@month 4").isoformat() == "2024-08-01T00:00:00+00:00"
    assert parse("@months 12").isoformat() == "2023-12-01T00:00:00+00:00"
    assert parse("@month 12").isoformat() == "2023-12-01T00:00:00+00:00"
    assert parse("@m 12").isoformat() == "2023-12-01T00:00:00+00:00"


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42+00:00"), tick=False)
def test_floor_operation_jan():
    assert parse("/Jan").isoformat() == "2024-01-01T00:00:00+00:00"
    assert parse("/jan").isoformat() == "2024-01-01T00:00:00+00:00"
    assert parse("/ Jan").isoformat() == "2024-01-01T00:00:00+00:00"
    assert parse("/ jan").isoformat() == "2024-01-01T00:00:00+00:00"


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42+00:00"), tick=False)
def test_floor_operation_feb():
    assert parse("/Feb").isoformat() == "2024-02-01T00:00:00+00:00"
    assert parse("/feb").isoformat() == "2024-02-01T00:00:00+00:00"
    assert parse("/ Feb").isoformat() == "2024-02-01T00:00:00+00:00"
    assert parse("/ feb").isoformat() == "2024-02-01T00:00:00+00:00"


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42+00:00"), tick=False)
def test_floor_operation_mar():
    assert parse("/Mar").isoformat() == "2024-03-01T00:00:00+00:00"
    assert parse("/mar").isoformat() == "2024-03-01T00:00:00+00:00"
    assert parse("/ Mar").isoformat() == "2024-03-01T00:00:00+00:00"
    assert parse("/ mar").isoformat() == "2024-03-01T00:00:00+00:00"


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42+00:00"), tick=False)
def test_floor_operation_apr():
    assert parse("/Apr").isoformat() == "2024-04-01T00:00:00+00:00"
    assert parse("/apr").isoformat() == "2024-04-01T00:00:00+00:00"
    assert parse("/ Apr").isoformat() == "2024-04-01T00:00:00+00:00"
    assert parse("/ apr").isoformat() == "2024-04-01T00:00:00+00:00"


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42+00:00"), tick=False)
def test_floor_operation_may():
    assert parse("/May").isoformat() == "2024-05-01T00:00:00+00:00"
    assert parse("/may").isoformat() == "2024-05-01T00:00:00+00:00"
    assert parse("/ May").isoformat() == "2024-05-01T00:00:00+00:00"
    assert parse("/ may").isoformat() == "2024-05-01T00:00:00+00:00"


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42+00:00"), tick=False)
def test_floor_operation_jun():
    assert parse("/Jun").isoformat() == "2024-06-01T00:00:00+00:00"
    assert parse("/jun").isoformat() == "2024-06-01T00:00:00+00:00"
    assert parse("/ Jun").isoformat() == "2024-06-01T00:00:00+00:00"
    assert parse("/ jun").isoformat() == "2024-06-01T00:00:00+00:00"


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42+00:00"), tick=False)
def test_floor_operation_jul():
    assert parse("/Jul").isoformat() == "2024-07-01T00:00:00+00:00"
    assert parse("/jul").isoformat() == "2024-07-01T00:00:00+00:00"
    assert parse("/ Jul").isoformat() == "2024-07-01T00:00:00+00:00"
    assert parse("/ jul").isoformat() == "2024-07-01T00:00:00+00:00"


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42+00:00"), tick=False)
def test_floor_operation_aug():
    assert parse("/Aug").isoformat() == "2024-08-01T00:00:00+00:00"
    assert parse("/aug").isoformat() == "2024-08-01T00:00:00+00:00"
    assert parse("/ Aug").isoformat() == "2024-08-01T00:00:00+00:00"
    assert parse("/ aug").isoformat() == "2024-08-01T00:00:00+00:00"


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42+00:00"), tick=False)
def test_floor_operation_sep():
    assert parse("/Sep").isoformat() == "2024-09-01T00:00:00+00:00"
    assert parse("/sep").isoformat() == "2024-09-01T00:00:00+00:00"
    assert parse("/ Sep").isoformat() == "2024-09-01T00:00:00+00:00"
    assert parse("/ sep").isoformat() == "2024-09-01T00:00:00+00:00"


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42+00:00"), tick=False)
def test_floor_operation_oct():
    assert parse("/Oct").isoformat() == "2024-10-01T00:00:00+00:00"
    assert parse("/oct").isoformat() == "2024-10-01T00:00:00+00:00"
    assert parse("/ Oct").isoformat() == "2024-10-01T00:00:00+00:00"
    assert parse("/ oct").isoformat() == "2024-10-01T00:00:00+00:00"


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42+00:00"), tick=False)
def test_floor_operation_nov():
    assert parse("/Nov").isoformat() == "2024-11-01T00:00:00+00:00"
    assert parse("/nov").isoformat() == "2024-11-01T00:00:00+00:00"
    assert parse("/ Nov").isoformat() == "2024-11-01T00:00:00+00:00"
    assert parse("/ nov").isoformat() == "2024-11-01T00:00:00+00:00"


@time_machine.travel(dt.datetime.fromisoformat("2024-12-29T19:28:42+00:00"), tick=False)
def test_floor_operation_dec():
    assert parse("/Dec").isoformat() == "2024-12-01T00:00:00+00:00"
    assert parse("/dec").isoformat() == "2024-12-01T00:00:00+00:00"
    assert parse("/ Dec").isoformat() == "2024-12-01T00:00:00+00:00"
    assert parse("/ dec").isoformat() == "2024-12-01T00:00:00+00:00"


def test_floor_operation_demo_case():
    with time_machine.travel(dt.datetime.fromisoformat("2024-07-07T19:28:42+00:00"), tick=False):
        assert parse("{/Jun,/Dec}").isoformat() == "2024-06-01T00:00:00+00:00"
        assert parse("@month 6").isoformat() == "2024-06-01T00:00:00+00:00"

    with time_machine.travel(dt.datetime.fromisoformat("2025-03-07T19:28:42+00:00"), tick=False):
        assert parse("{/Jun,/Dec}").isoformat() == "2024-12-01T00:00:00+00:00"
        assert parse("@month 6").isoformat() == "2024-12-01T00:00:00+00:00"


def test_time_override():
    cronspell = Cronspell()
    cronspell.now_func = lambda: dt.datetime.fromisoformat("2023-07-07T17:18:11+00:00")
    assert cronspell.parse("now /d").isoformat() == "2023-07-07T00:00:00+00:00"
