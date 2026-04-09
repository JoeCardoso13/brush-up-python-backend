`all` returns `True` if all of the elements are truthy, `False` otherwise.
```python
collection1 = [False, False, False]
collection2 = (False, True, False)
collection3 = {True, True, True}

print(all(collection1))       # False
print(all(collection2))       # False
print(all(collection3))       # True
print(all([]))                # True
```
