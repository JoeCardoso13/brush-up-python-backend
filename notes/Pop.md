`seq.pop` removes and returns an indexed element from a mutable [[Sequence]]. If no index is given, it removes the **last** **element** in the [[Sequence]]. It raises an error if the index is out of range. `pop` only works with mutable _indexed_ sequences.
```python
my_list = [2, 4, 6, 8, 10]

print(my_list.pop(1))         # 4
print(my_list)                # [2, 6, 8, 10]

print(my_list.pop())          # 10
print(my_list)                # [2, 6, 8]

print(my_list.pop(4)) # IndexError: pop index out of range
```
