# ​CronSpell

Date-expression domain specific language parsing. A neat way to express things like "First Saturday of any year", or "3rd thursdays each month" and such

## Status

CronSpell is currently in Beta. While it is considered well tested and stable for most use cases, there may still be some edge cases and bugs that need to be addressed. The maintainer encourages users to try it out and [provide feedback to help improving the library.](https://github.com/iilei/cronspell/issues)

Your contributions and bug reports are highly appreciated.

## Features

### Python

Cronspell is heavily inspired by Grafana's relative Date picker user interface. It shines when configuration is needed to reflect irregular date-distances such as in the example below.

`cronspell` lets you express relative dates such as "last saturday of last month" and converts it to a date object for use in your python project.

Installation: `pip install cronspell`

### Cli

The same interface, exposed to the command line. Formatted via `isodate` by default -- which is
open for coniguration using the `--format` option.

Installation with cli-specific dependencies: `pip install cronspell[cli]`


## Examples

To get the last saturday of last month:

```
"now /m -1d /sat"
```

The same, more verbose:
```
"now /month -1day /sat"
```

which instructs the parser to perform the following sequence of operations:

![](./assets/images/example.svg)


## Credits

* Domain-Specific-Language Parser: [TextX]
* This package was created with [The Hatchlor] project template.

[TextX]: https://textx.github.io/textX/
[The Hatchlor]: https://github.com/florianwilhelm/the-hatchlor


## Navigation

Documentation for specific `MAJOR.MINOR` versions can be chosen by using the dropdown on the top of every page.
The `dev` version reflects changes that have not yet been released. Shortcuts can be used for navigation, i.e.
<kbd>,</kbd>/<kbd>p</kbd> and <kbd>.</kbd>/<kbd>n</kbd> for previous and next page, respectively, as well as
<kbd>/</kbd>/<kbd>s</kbd> for searching.
