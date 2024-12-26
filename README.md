
# Cronspell Python Package / CLI Tool
***Chronometry Spelled Out***


[![Github Pages][Github Pages]][Github Pages Link]


|          |                                                                                                                                                                                                                                   |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Details  | [![Tests][Tests-image]][Tests-link] [![License - MIT][MIT-image]][MIT-link]                                                                                                                                                       |
| Features | [![linting - Ruff][ruff-image]][ruff-link] [![types - mypy][mypy-image]][mypy-link] [![test - pytest][pytest-image]][pytest-link]  [![Pre-Commit][precommit-image]][precommit-link] [![docs - mkdocs][mkdocs-image]][mkdocs-link] |

Date-expression domain specific language (DSL) parsing. A neat way to express things like "First Saturday of any year", or "3rd thursdays each month" and such.


## Status

CronSpell is currently in Beta. While it is considered well tested and stable for most use cases, there may still be some edge cases and bugs that need to be addressed. The maintainer encourages users to try it out and [provide feedback to help improving the library.](https://github.com/iilei/cronspell/issues)

Your contributions and bug reports are highly appreciated.

## Features

Cronspell is heavily inspired by Grafana's relative Date picker user interface. It was designed for the cases when configuration is needed to reflect irregular date-distances.

Use it within your Python project or via command line interface.

### Python

Installation: `pip install cronspell`

### Cli

The same interface, exposed to the command line. Formatted via `isodate` by default -- which is
open for coniguration using the `--format` option.

Installation with cli-specific dependencies: `pip install cronspell[cli]`


## Syntax

### Comments
```cpp
// a comment
```

```cpp
/*
    multi-line
    comment ...
*/
```


### Datetime Designators
```cpp
/m -1d /sat
```

The same, more verbose:

```cpp
/month -1day /sat
```

### Datetime Designator Sets

By enclosing a set in curly braces (`{}`), a comma seperated list of datetime designators is evaluated.

```cpp
// here comes a set of datetime designators
{
    // first saturday of the month:
    /m -1d /sat + 7d,

    // sunday of every second calendar week:
    @cw 2 + 6d
}
```

Timezone Designation

```cpp
// `now` is the default anchor for subsequent designators.
// passing a timezone name to get the results with the same timezone:

now[Europe/Berlin] {
    // first saturday of the month:
    /m -1d /sat + 7d,

    // sunday of every second calendar week:
    @cw 2 + 6d
}
```


## Credits

* Domain-Specific-Language Parser: [TextX]
* This package was created with [The Hatchlor] project template.

[TextX]: https://textx.github.io/textX/
[The Hatchlor]: https://github.com/florianwilhelm/the-hatchlor



[Tests-image]: https://github.com/iilei/cronspell/actions/workflows/tests.yml/badge.svg?branch=master
[Tests-link]: https://github.com/iilei/cronspell/actions/workflows/tests.yml
[hatch-image]: https://img.shields.io/badge/%F0%9F%A5%9A-hatch-4051b5.svg
[hatch-link]: https://github.com/pypa/hatch
[ruff-image]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
[ruff-link]: https://github.com/charliermarsh/ruff
[mypy-image]: https://img.shields.io/badge/Types-mypy-blue.svg
[mypy-link]: https://mypy-lang.org/
[pytest-image]: https://img.shields.io/static/v1?label=‎&message=Pytest&logo=Pytest&color=0A9EDC&logoColor=white
[pytest-link]:  https://docs.pytest.org/
[mkdocs-image]: https://img.shields.io/static/v1?label=‎&message=mkdocs&logo=Material+for+MkDocs&color=526CFE&logoColor=white
[mkdocs-link]: https://www.mkdocs.org/
[precommit-image]: https://img.shields.io/static/v1?label=‎&message=pre-commit&logo=pre-commit&color=76877c
[precommit-link]: https://pre-commit.com/
[MIT-image]: https://img.shields.io/badge/License-MIT-9400d3.svg
[MIT-link]: LICENSE.txt
[Github Pages]: https://img.shields.io/badge/github%20pages-121013?style=for-the-badge&logo=github&logoColor=teal
[Github Pages Link]: https://iilei.github.io/cronspell/
