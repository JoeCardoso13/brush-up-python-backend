The indexing syntax also supports a **slicing** augmentation. Slicing can extract (or modify) any number of consecutive elements simultaneously. For instance, the syntax `seq[start:stop]` retrieves the elements from `seq` whose index is between `start` and `stop - 1`, inclusive. You can also use negative indexes for the slice. Finally, you can use the `seq[start:stop:step]` syntax to slice every "step-th" element.
```python
seq = 'abcdefghi'
print(seq[3:7])       # defg
print(seq[-6:-2])     # defg
print(seq[2:8:2])     # ceg
print(repr(seq[3:3])) # ''
print(seq[:])         # abcdefghi
print(seq[::-1])      # ihgfedcba

seq = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(seq[3:7])       # [4, 5, 6, 7]
print(seq[-6:-2])     # [5, 6, 7, 8]
print(seq[2:8:2])     # [3, 5, 7]
print(seq[3:3])       # []
print(seq[:])         # [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(seq[::-1])      # [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

seq = [[1, 2], [3, 4]]
seq_dup = seq[:]
print(seq[0] is seq_dup[0])   # True
```
