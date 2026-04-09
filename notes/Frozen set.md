Frozen sets are merely immutable [[Set]]s. They do not have a [[Literal]] syntax, so you must use `frozenset` [[Function]] to create one. Examples:
```python
>>> s5 = frozenset([1, 2, 3]) 
>>> print(s5) 
frozenset({1, 2, 3}) 

>>> s6 = frozenset((1, 2, 3)) 
>>> print(s6)
frozenset({1, 2, 3}) 

>>> s7 = frozenset({1, 2, 3}) 
>>> print(s7) 
frozenset({1, 2, 3}) 

>>> s8 = frozenset(range(1, 4)) 
>>> print(s8) 
frozenset({1, 2, 3})
```
