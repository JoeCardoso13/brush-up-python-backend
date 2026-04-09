When used without arguments, the `dir` function returns a list of all identifiers in the current local scope:
```
>>> dir() 
['__builtins__', '__name__', 'struct']
```
When used with an argument, `dir()` returns a list of the object's attributes (typically, the object's methods and instance variables):
```
>>> dir(5) 
['__abs__', '__add__', '__and__', '__bool__', 
... a bunch of stuff omitted ... ,
'__xor__', 'as_integer_ratio', 'bit_count', 'bit_length', 'conjugate', 'denominator', 'from_bytes', 'imag', 'numerator', 'real', 'to_bytes']
```
Many of the names shown by `dir` begin and end with two underscores. These are names for the so-called **dunder** (double-underscore) or [[Magic method]]s and [[Magic variable]]s.

---
**Helpful Hint**: Use the `sorted` function with the output of `dir`:
```
>>> sorted(dir(range(1)))
['__bool__', '__class__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', 
... a bunch of stuff omitted ..., 
'count', 'index', 'start', 'step', 'stop']
```
**Another Helpful Hint**: Use pretty print to print the output in an easier to read format:
```
>>> from pprint import pp 
>>> names = sorted(dir(range(1))) 
>>> pp(names)
['__bool__', 
'__class__', 
'__contains__', 
'__delattr__', 
... a bunch of stuff omitted ..., 
'count', 
'index', 
'start', 
'step', 
'stop']
```
**Yet Another Helpful Hint**: Use a [[Comprehension]] to limit the output to just the names that don't contain `__`:
```
>>> names = sorted(dir(range(1)))
>>> names = [name for name in names 
...          if '__' not in name] 
>>> print(names) 
['count', 'index', 'start', 'step', 'stop']
```
