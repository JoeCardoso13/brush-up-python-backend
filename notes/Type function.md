It can be called on any [[Object]]:
```python
print(type(1))         # <class 'int'>
print(type(3.14))      # <class 'float'>
print(type(True))      # <class 'bool'>
print(type('abc'))     # <class 'str'>
print(type([1, 2, 3])) # <class 'list'>
print(type(None))      # <class 'NoneType'>

foo = 42               # Variables work, too
print(type(foo))       # <class 'int'>
```
To get a more succinct answer:
```python
print(type('abc').__name__)   # str
print(type(False).__name__)   # bool
print(type([]).__name__)      # list
```
You can also use it along with the [[Is operator]]:
```python
print(type('abc') is str)     # True
print(type('abc') is int)     # False
print(type(False) is bool)    # True
print(type([]) is list)       # True
print(type([]) is set)        # False
```
Note that this former way of identifying [[Type]] discount effects of [[Inheritance]]. If you want to account for use use [[Isinstance]] instead.
