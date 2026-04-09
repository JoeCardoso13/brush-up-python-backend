A **range** is a [[Sequence]] of [[Integer]]s between two endpoints. **Ranges** are most commonly used to do iteration over an increasing or decreasing range of [[Integer]]s. Examples:
```python
>>> tuple(range(5)) 
(0, 1, 2, 3, 4)
>>> tuple(range(5, 10))
(5, 6, 7, 8, 9)
>>> list(range(1, 10, 2)) 
[1, 3, 5, 7, 9] 
>>> list(range(0, -5, -1)) 
[0, -1, -2, -3, -4]
```
Ranges are **lazy sequences**: they don't create any element values until your program needs them. One way to get those numbers is to convert the range to a [[List]] or [[Tuple]].

The `range` constructor comes in 3 forms:

- `range(start, stop, step)`
    
    This constructor generates a sequence of integers between `start` and `stop - 1` with an increment of `step` between each consecutive integer. You can use a negative step to generate a sequence in reverse order. In this case, the range ends at `stop + 1`. You can create empty ranges by giving values where `start >= stop` when `step` is positive or `start <= stop` when `step` is negative. Empty ranges are often bugs.
- `range(start, stop)`
    
    When you omit the `step` argument, Python uses a default value of `1`. Hence, `range(start, stop)` is identical to `range(start, stop, 1)`.
- `range(stop)`
    
    When you omit the `start` argument, Python uses a default value of `0` for `start`. Hence, `range(stop)` is identical to `range(0, stop, 1)`.
