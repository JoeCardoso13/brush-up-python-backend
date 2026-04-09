It's using the less than, greater than with the optional or equal. Examples:
```python
print(42 < 41)           # False
print(42 < 42)           # False
print(42 <= 42)          # True
print(42 < 43)           # True

print('abcdf' < 'abcef') # True
print('abc' < 'abcdef')  # True
print('abcdef' < 'abc')  # False
print('abc' < 'abc')     # False
print('abc' <= 'abc')    # True
print('abd' < 'abcdef')  # False
print('A' < 'a')         # True
print('Z' < 'a')         # True

print('3' < '24')        # False
print('24' < '3')        # True
```
Note that [[String]]s are compared [[Lexicographically]].

You can also compare lists and tuples: like [[String]] comparisons (compared [[Lexicographically]]), [[List]] and [[Tuple]] comparison goes element by element to determine which object is less than or greater than the other:
```python
print({3, 1, 2} < {2, 4, 3, 1})         # True
print({3, 1, 2} > {2, 4, 3, 1})         # False
print({2, 4, 3, 1} > {3, 1, 2})         # True

print([1, 2, 3] < [1, 2, 3, 4])         # True
print([1, 4, 3] < [1, 3, 3])            # False
print([1, 3, 3] < [1, 4, 3])            # True
```
