It's when the program doesn't evaluate the entire logical [[Expression]] as soon as it can guarantee the result. So, for instance, using the following [[Logical operator]]s:
```
is_red(item) and is_portable(item)
is_green(item) or has_wheels(item)
```
if `is_red` evaluates to `False` then `is_portable` is never run, and if `is_green` evaluates to `True` then `has_wheels` is never run.

Short circuit evaluations are mostly useful when associated with [[Truthiness]]. Like when creating this [[Predicate]]:
```python
foo = None
bar = 'qux'
is_ok = bool(foo or bar)
```
