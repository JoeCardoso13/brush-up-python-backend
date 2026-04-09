When comparing [[String]]s, Python stops as soon as it makes a decision. For instance, in `'abd' < 'abcdef'`, Python only needs to check the first 3 characters in both [[String]]s. When it reaches the 3rd character, it can see that `'abd'` is _not_ less than `'abcdef'` so it returns `False`. If it reaches the end of one [[String]] meanwhile all characters until then were the same, then the shorter is _less than_ the longer one. Examples:

```python
print('abcdf' < 'abcef') # True
print('abc' < 'abcdef')  # True
print('abcdef' < 'abc')  # False
print('abc' < 'abc')     # False
print('abc' <= 'abc')    # True
print('abd' < 'abcdef')  # False
print('A' < 'a')         # True
print('Z' < 'a')         # True

print('abcdf' > 'abcef') # False
print('abc' > 'abcdef')  # False
print('abcdef' > 'abc')  # True
print('abc' > 'abc')     # False
print('abc' >= 'abc')    # True
print('abcdef' > 'abd')  # False
print('A' > 'a')         # False
print('Z' > 'a')         # False
```

In general, numeric characters in a [[String]] are less than alphabetic characters, and uppercase letter characters are less than lowercase letters. Other characters appear at different points. For instance, `'#' < '5' < ';' < 'A' < '^' < 'a'`.

If the precise ordering of character values becomes sufficiently significant to matter, look them up in a [standard ASCII table](https://www.ascii-code.com/ASCII).
