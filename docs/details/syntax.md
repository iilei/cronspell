# Syntax

***Structure of a relative-date-expression to be parsed with cronspell***

Expressions consist of an optional `anchor` at the start, from where to apply
the subsequent chain of operations.


```cpp
<anchor = now[UTC]> *<Operation>
```

## Comments


```cpp
// end-of-line comment, closed by a newline character
now[UTC]  /* inline comments */
```

## Anchor

If omitted, the Anchor equates to `now`, zero time zone offset.

### Relative datetime

The string `now`, optionally followed by a timezone name enclosed in square brackets:

```cpp
now
now[Europe/Berlin]          /* any timezone identifier compatible with ZoneInfo */
```

### Absolute datetime

If needed, absolute datetimes serve as anchors, too:

```text
2024-12-30T01:13:42+05:45   /* absolute time, timezone offset as of Asia/Kathmandu */
```

## Operation

Valid examples of operations, line by line:

```cpp
/ month          // beginning of the month
/ sat            // beginning of the most recent saturday
/ day            // beginning of the day
+ 3 hours        // add three hours
- 1 second       // minus one second
```

### Date-Floor

With Cronspell, a forward slash (`/`) indicates a `floor` operation. It follows the same logic as python math;

```python
math.floor(3.9) == math.floor(3.0)
```

That said, if you do a `now /sat` on a saturday, it yields the same each time it is evaluated as long as the next friday has not come to an end.


## Permissible expressions

The following expressions are recognized:

|                              |                    | Pattern                       |
| :--------------------------- | :----------------- | :---------------------------- |
| **mon**                      | monday             | `\bmon\b`                     |
| **tue**                      | tuesday            | `\btue\b`                     |
| **wed**                      | wednesday          | `\bwed\b`                     |
| **thu**                      | thursday           | `\bthu\b`                     |
| **fri**                      | friday             | `\bfri\b`                     |
| **sat**                      | saturday           | `\bsat\b`                     |
| **sun**                      | sunday             | `\bsun\b`                     |
|                              |                    |                               |
| **ISODate**                  | fixed date         | `\d+\S+`                      |
| **NaiveNow**                 | relative datetime  | `now`                         |
|                              |                    |                               |
| **Y**                        | year               | `([Yy]ears?\|Y\b)`            |
| **m**                        | month              | `(?!mon\b)([mM]onths?\|m\b)`  |
| **W**                        | week               | `([wW]eeks?\|W\b)`            |
| **d**                        | day                | `([dD]ays?\|d\b)`             |
| **H**                        | hour               | `([hH]ours?\|H\b)`            |
| **M**                        | minutes            | `([mM]inutes?\|M\b)`          |
| **S**                        | seconds            | `(?!sat$)([sS]econds?\|S\b)`  |
|                              |                    |                               |
| **Comment**                  |                    | `\/\*(.\|\n)*?\*\/\|\/\/.*?$` |
| **CalendarWeekModuloMarker** | Implicit *`floor`* | `[%,@]\s*\b(CW\|Cw\|cw)\b`    |
| **YearModuloMarker**         | Implicit *`floor`* | `[%,@]\s*\b(Y\|y)(ears?)?\b`  |
