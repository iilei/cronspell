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

<table>
	<tr>
		<td><b>Comment</b></td><td>\/\*(.|\n)*?\*\/|\/\/.*?$</td>
	</tr>
	<tr>
		<td><b>Fri</b></td><td>\bfri\b</td>
	</tr>
	<tr>
		<td><b>H</b></td><td>([hH]ours?|H\b)</td>
	</tr>
	<tr>
		<td><b>ISODate</b></td><td>\d+\S+</td>
	</tr>
	<tr>
		<td><b>M</b></td><td>([mM]inutes?|M\b)</td>
	</tr>
	<tr>
		<td><b>Mon</b></td><td>\bmon\b</td>
	</tr>
	<tr>
		<td><b>NaiveNow</b></td><td>now</td>
	</tr>
	<tr>
		<td><b>S</b></td><td>(?!sat$)([sS]econds?|S\b)</td>
	</tr>
	<tr>
		<td><b>Sat</b></td><td>\bsat\b</td>
	</tr>
	<tr>
		<td><b>Sun</b></td><td>\bsun\b</td>
	</tr>
	<tr>
		<td><b>Thu</b></td><td>\bthu\b</td>
	</tr>
	<tr>
		<td><b>Tue</b></td><td>\btue\b</td>
	</tr>
	<tr>
		<td><b>W</b></td><td>([wW]eeks?|W\b)</td>
	</tr>
	<tr>
		<td><b>Wed</b></td><td>\bwed\b</td>
	</tr>
	<tr>
		<td><b>Y</b></td><td>([Yy]ears?|Y\b)</td>
	</tr>
	<tr>
		<td><b>d</b></td><td>([dD]ays?|d\b)</td>
	</tr>
	<tr>
		<td><b>m</b></td><td>(?!mon\b)([mM]onths?|m\b)</td>
	</tr>
</table>
