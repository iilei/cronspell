# CLI Usage

## Help

Get Help

```shell
cronspell --help
```

## Commands

The following commands are available:

  * parse
  * pre-commit
  * dot
  * locate

### parse

Arguments:

  * `*<date expression>`

Invokes the parser on a given date expression

### pre-commit

See documentation on [Pre-Commit](../pre_commit_hook)

### dot

Arguments:

  * `*[<date expression>]`
  * `--out <dir>`

Generates GraphViz Dot diagrams based on a list of expressions. Writes to `--out`.

### locate

Arguments:

  *None*

Returns the path of the MetaModel utilized in TextX.


### upcoming

Arguments:

  * `<expression>`: The date expression to evaluate.
  * `--interval-days, -d <int>`: Interval of days to examine (default: 1).
  * `--initial-now, -n <str>`: What to consider as 'now' (default: current date and time).
  * `--end, -e <str>`: End of the date range to examine (default: 321 days from now).

Prints upcoming moments matched by the given expression.
