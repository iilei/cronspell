# Pre-Commit Hook

For use with [pre-commit](https://pre-commit.com/) hooks, there is a cli command to
perform a pre-flight check on `cronspell` date expressions available.

Under the hood, depending on the configuration, the following is executed when the pre-commit hook
triggers for changes in a file named `docs/assets/demo.cfg.yaml`:

`cronspell preflight --yamlpath '/*/rel_date*' docs/assets/demo.cfg.yaml`

Example `.pre-commit-config.yaml`;

```yaml
repos:
  - repo: https://github.com/iilei/cronspell
    # git sha or latest tag ({{ cronspell.version if cronspell.version is not none else '0.0.0-rc15' }})
    rev: 542403ac19195dba36020fdd09db4c8788783117
    hooks:
      - id: cronspell
        files: .*\/cfg\.ya?ml$
        args: ["--yamlpath", "/*/rel_date*" ]

```

Note the [yamlpath](https://github.com/wwkimball/yamlpath?tab=readme-ov-file#supported-yaml-path-segments) argument: this tells the pre-commit hook where to
look for expressions to check.

Configuration objects like follows pass the pre commit check:

```yaml
- type: first_saturday
  rel_date: /month -1day /sat + 1 week
- type: first_friday
  rel_date: /month -1day /fri + 1 week
  rel_date_time: +1 Hour


```

The following example in contrast does not pass the pre-commit checks, as the calendar
week designated to *floor* to needs to be in range `1..52`;

```yaml
- type: "should not pass"
  cronspell: "@CW 77"
```
