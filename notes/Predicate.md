Are prefixed by 'is_' like so, for [[Function]]s:
```python
def is_digit(char):
    if char >= '0' and char <= '9':
        return True

    return False
```
And for [[Variable]]s:
```python
foo = None
bar = 'qux'
is_ok = bool(foo or bar)
```
