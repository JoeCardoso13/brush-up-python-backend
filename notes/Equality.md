Uses double equal `==` and returns a [[Boolean]]. Examples:
```python
print(42 == 42)       # True
print(42 == 43)       # False
print('foo' == 'foo') # True (works with strings)
print('FOO' == 'foo') # False (Case matters)

print(42 != 42)       # False
print(42 != 43)       # True
print('foo' != 'foo') # False (works with strings)
print('FOO' != 'foo') # True (Case matters)
```
Mostly if you try to compare different [[Type]]s for equality, you get a `False` answer, however numbers are an exception. I.e. you can compare [[Integer]]s and [[Float]]s.

The [[Is operator]] provides a more strict criteria for equality.

---
For [[Iterable]]s, if two meet all of the following requirements, they are equal. Otherwise, they are unequal.

- They have the same [[Type]]: (list, tuple, set, etc.) Note that [[Set]]s and [[Frozen set]]s are considered the same for comparison purposes.
- They have the same number of elements.
- For [[Sequence]]s, each pair of corresponding elements compares as equal.
- For [[Set]]s, each [[Set]] has the same members (order doesn't matter).
- For [[Mapping]], each key/value pair must be present and identical in both [[Mapping]]s (order doesn't matter).
```python
print([2, 3] == [2, 3])    # True
print([2, 3] == [3, 2])    # False (diff sequence)
print([2, 3] == [2])       # False (diff lengths)
print([2, 3] == (2, 3))    # False (diff types)
print({2, 3} == {3, 2})    # True (same members)

dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 2, 'a': 1}
dict3 = {'a': 1, 'b': 2, 'c': 3}

print(dict1 == dict2)      # True (same pairs)
print(dict1 == dict3)      # False
```
