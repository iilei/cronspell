# CLI Usage

## Help

Get Help

```shell
cronspell --help
```

## Commands

The following commands are available:

  * parse
  * dot
  * locate

### Parse

Arguments:

  * `*<date expression>`

Invokes the parser on a given date expression

### dot

Arguments:

  * `*[<date expression>]`
  * `--out <dir>`

Generates GraphViz Dot diagrams based on a list of expressions. Writes to `--out`.

### locate

Arguments:

  *None*

Returns the path of the MetaModel utilized in TextX.
