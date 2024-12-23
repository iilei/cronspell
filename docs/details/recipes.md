# Recipes

## First Saturday of month

The following expression determines the first saturday of the current month.

```cpp
/month -1 day /sat + 1 week
```

## Third Saturday of month

From there, simply adding 2 weeks does the trick.

```cpp
/month -1 day /sat + 3 weeks
```


## Calendar week clamped to `n`th

To perform a `modulo` operation on calendar week `n`, both of the follwing variants work:


```cpp
@CW 3
```
`@` and `%` are interchangeable and `cw` can be `CW` or `Cw` just as well. As an example, this is the same as the above

```cpp
%cw 3
```

The result is just like `floor` to `monday`, just to the most recent calendar week that is divisible by `3`; `CW 3` , `CW 6` ... up to `CW 51`

## Year clamped to `n`th

Similar to Calendar Week:

```cpp
@Y 3
```
Or

```cpp
%years 3
```

## Upcoming Occurrences

Find upcoming dates beginning of every 3rd calendar week


```python
from cronspell.upcoming import moments as upcoming

upcoming("@cw 3")


```
