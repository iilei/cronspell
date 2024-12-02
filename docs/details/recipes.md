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
@cw 3
```
Or

```cpp
%cw 3
```

The result is just like `floor` to `monday`, just to the most recent calendar week that is divisible by `3`; `CW 3` , `CW 6` ... up to `CW 51`
