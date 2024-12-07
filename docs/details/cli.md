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
