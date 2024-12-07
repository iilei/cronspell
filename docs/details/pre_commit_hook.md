# Pre-Commit Hook

For use with [pre-commit](https://pre-commit.com/) hooks, there is a cli command to
perform a pre-flight check on `cronspell` date expressions available.

Example `.pre-commit-config.yaml`;

```yaml
repos:
  - repo: https://github.com/iilei/cronspell
    rev: {{ cronspell.version if cronspell.version is not none else 'a95a388' }}
    hooks:
      - id: cronspell
        # yamlpath is up to projects using cronspell. Default:
        # args: ["--yamlpath", "/*/cronspell" ]

```

Note the [yamlpath](https://github.com/wwkimball/yamlpath?tab=readme-ov-file#supported-yaml-path-segments) argument: this tells the pre-commit hook where to
look for expressions to check.

Configuration objects like follows pass the pre commit check:

```yaml
- type: "should pass"
  cronspell: "@CW 3"
- xyz: anything
  not_important: 42

```

The following example in contrast does not pass the pre-commit checks, as the calendar
week designated to *floor* to needs to be in range `1..52`;

```yaml
- type: "should not pass"
  cronspell: "@CW 77"
```
