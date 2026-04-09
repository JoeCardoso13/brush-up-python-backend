We got:
* [[Logical operator]]s
* `is` for [[Equality]]
* `in` for [[Collection]] membership (also `not in`). Examples:
```python
seq = [4, 'abcdef', (True, False, None)]
print(4 in seq)                         # True
print(4 not in seq)                     # False
print('abcdef' in seq)                  # True
print('abcdef' not in seq)              # False
print('cde' in seq[1])                  # True
print('cde' not in seq[1])              # False
print('acde' in seq[1])                 # False
print('acde' not in seq[1])             # True
print((True, False, None) in seq)       # True
print((True, False, None) not in seq)   # False
print(3.14 in seq)                      # False
print(3.15 not in seq)                  # True
```
