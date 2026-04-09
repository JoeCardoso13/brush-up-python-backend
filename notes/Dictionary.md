A **dictionary** (**dict**) is a [[Collection]] of key-value pairs. A **dict** is similar to a [[List]] but uses keys instead of indexes to access specific elements. Other languages use different names for similar structures: hashes, mapping, objects, and associative arrays are the most common terms. Example:
```
>>> my_dict = { 
... 'dog': 'barks', 
... 'cat': 'meows', 
... 'pig': 'oinks', 
... } 
{'dog': 'barks', 'cat': 'meows', 'pig': 'oinks'}
```
They are unordered [[Collection]]s in which *insertion order is preserved* (since Python 3.7).

The only requirement for an [[Object]] to be allowed as a key is that it is *hashable*. immutable [[Object]]s are always hashable (so technically you can use a [[Tuple]] as a key provided all its elements are immutable and hashable). 

---
If you don't want a [[KeyError]] to be raised when querying a dictionary with an absent key, you use `dict.get`:
```python
my_dict = {
    'a': 'abc',
    37: 'def',
    (5, 6, 7): 'ghi',
    frozenset([1, 2]): 'jkl',
}

print(my_dict.get('a'))                 # abc
print(my_dict.get('nothing'))           # None
print(my_dict.get('nothing', 'N/A'))    # N/A
print(my_dict.get('nothing', 100))      # 100
```
