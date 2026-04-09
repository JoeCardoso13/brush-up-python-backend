The `any` function returns `True` if any element in a collection is truthy, `False` if all of the elements are falsy.
```python
collection1 = [False, False, False]
collection2 = (False, True, False)
collection3 = {True, True, True}

print(any(collection1))       # False
print(any(collection2))       # True
print(any(collection3))       # True
print(any([]))                # False
```
