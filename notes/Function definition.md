Basic syntax:
```python
def func_name():
    func_body
```
If the [[Function]]'s body has a `return` [[Statement]], it has an *explicit return value*, otherwise it returns `None` implicitly.

---
Python programmers often add a triple-quoted [[String]] at the beginning of a [[Function]]'s block. This [[String]] is a documentation comment -- a **docstring** -- that Python can access with its [[Help]] [[Function]] and the `__doc__` property. It has no effect on your code unless your program is somehow interested in the comments (which can happen):
```python
def say():
    """
    The say function prints "Hi!"
    """
    print('Hi!')

print('-' * 60)
print(say.__doc__)
print('-' * 60)
help(say)
```
Outputs:
```
------------------------------------------------------------

    The say function prints "Hi!"

------------------------------------------------------------
Help on function say in module \_\_main\_\_:

say()
    The say function prints "Hi!"
```
