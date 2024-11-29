from cronspell import resolve

assert resolve("2024-11-29T12:12:00+00:00 /sat -1 week +1d").isoformat() == "2024-11-17T00:00:00+00:00"

assert resolve("now[Europe/Berlin] / m +3d /W").isoformat().rpartition("+")[-1] in {
    "01:00",
    "02:00",
}

assert resolve("").isoformat().rpartition("+")[-1] == "00:00"

assert (
    resolve("2024-11-29T12:12:00+00:00 / month + 32 days / m -1 day /* get last day of this month */").isoformat()
    == "2024-11-30T00:00:00+00:00"
)

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
