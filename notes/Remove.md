`seq.remove` searches a [[Sequence]] for a specific [[Object]] and removes the first occurrence of that [[Object]]. It raises a `ValueError` if there is no such [[Object]].
```python
my_list = [2, 4, 6, 8, 10]

my_list.remove(8)
print(my_list)            # [2, 4, 6, 10]

my_list.remove(8)
# ValueError: list.remove(x): x not in list
```
