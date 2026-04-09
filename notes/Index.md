Returns the index of the first element in the [[Sequence]] that matches a given [[Object]].
```python
names = ['Karl', 'Grace', 'Clare', 'Victor',
         'Antonina', 'Allison', 'Trevor']
print(names.index('Clare'))   # 2
print(names.index('Trevor'))  # 6
print(names.index('Chris')) # ValueError: 'Chris' is not in list
```
It also works with strings. It searches for the first matching substring of a string:
```python
names = 'Karl Grace Clare Victor Antonina Trevor'
print(names.index('Clare'))   # 11
print(names.index('Trevor'))  # 33
print(names.index('Chris')) # ValueError: substring not found
```
