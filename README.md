
# Cronspell Python Package / CLI Tool
***Chronometry Spelled Out***


[![Github Pages][Github Pages]][Github Pages Link]


|          |                                                                                                                                                                                                                                   |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Details  | [![Tests][Tests-image]][Tests-link] [![License - MIT][MIT-image]][MIT-link]                                                                                                                                                       |
| Features | [![linting - Ruff][ruff-image]][ruff-link] [![types - mypy][mypy-image]][mypy-link] [![test - pytest][pytest-image]][pytest-link]  [![Pre-Commit][precommit-image]][precommit-link] [![docs - mkdocs][mkdocs-image]][mkdocs-link] |

Date-expression domain specific language parsing. A neat way to express things like "First Saturday of any year", or "3rd thursdays each month" and such.

## Installation

### Just the python module

If you need just the python function to parse cronspell expressions:

```shell
pip install cronspell
```

### With cli tools

If you like to use it in your command line:

```shell
pip install cronspell[cli]
```


## Features


### Python

Cronspell is heavily inspired by Grafana's relative Date picker user interface. It shines when configuration is needed to reflect irregular date-distances such as in the example below.

`cronspell` lets you express relative dates such as "last saturday of last month" and converts it to a date object for use in your python project.

```python
from cronspell import cronspell

# Cronspell's purpose is mostly to parse configuration files written in yaml
# and therein express relative date times in a human friendly manner.

# here is but a simple demo:
last_saturday = cronspell("now/sat")
...
```

### Cli

The same interface, exposed to the command line. Formatted via `isodate` by default -- which is
open for configuration using the `--format` option.

This is how you get the last saturday of the current month, for example:

```bash
cronspell parse "now /month + 34 days /m -1d /sat"
```

## Example

To get the last saturday of last month:

```
"now /m -1d /sat"
```

The same, more verbose:
```
"now /month -1day /sat"
```


## Pre-Commit Hook: Validation

Cronspell comes with a pre-commit hook that validates configured date-expressions based on
yamlpath.

Check out the [documentation][Github Pages Link] for detailed instructions.

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
