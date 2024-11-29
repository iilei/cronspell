from cronspell import resolve

assert (
    resolve("2024-11-29T12:12:00+00:00 /sat -1 week +1d").isoformat()
    == "2024-11-17T00:00:00+00:00"
)

assert resolve("now[Europe/Berlin] / m +3d /W").isoformat().rpartition("+")[-1] in {
    "01:00",
    "02:00",
}

assert resolve("").isoformat().rpartition("+")[-1] == "00:00"
