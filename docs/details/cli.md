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

Intended to be used with pip pre-commit hooks.

Arguments:

  * `*[<yaml file paths>]`
  * `--query <yamlpath>`


Given there are config files containing a list of configuration objects like follows:

```yaml
- type: first_saturday
  cronspell: /month -1day /sat + 1 week
- type: first_friday
  cronspell: /month -1day /fri + 1 week
```

And a `--query` argument `/*/cronspell` is provided, the command exits without errors.

The following example in contrast will lead to failure as the calendar week modulo is
not accepted:

```yaml
- type: first_saturday
  cronspell: "@cw 77"
```


### dot

Arguments:

  * `*[<date expression>]`
  * `--out <dir>`

Generates GraphViz Dot diagrams based on a list of expressions. Writes to `--out`.

### locate

Arguments:

  *None*

Returns the path of the MetaModel utilized in TextX.
