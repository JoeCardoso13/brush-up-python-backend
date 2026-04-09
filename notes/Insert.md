`seq.insert` inserts an [[Object]] into a mutable [[Sequence]] before the element at a given index. If the given index is greater than or equal to the [[Sequence]]'s length, the [[Object]] is appended to the [[Sequence]]. If the index is negative, it is counts from the end of the [[Sequence]].
```python
numbers = [1, 2]

numbers.insert(0, 8)    # Insert 8 before numbers[0]
print(numbers)          # [8, 1, 2]
numbers.insert(2, 6)    # Insert 6 before numbers[2]
print(numbers)          # [8, 1, 6, 2]
numbers.insert(100, 55) # Insert 55 before numbers[100]
print(numbers)          # [8, 1, 6, 2, 55]
numbers.insert(-3, 33)  # Insert 33 before the 3rd element
                        # from the end.
print(numbers)          # [8, 1, 33, 6, 2, 55]
```
