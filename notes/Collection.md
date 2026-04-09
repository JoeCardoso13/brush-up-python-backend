These are called **collection** [[Type]]s since each collects multiple items in a single object.

| Data Type      | Class       | Category      | Kind          | Mutable |
| -------------- | ----------- | ------------- | ------------- | ------- |
| [[Range]]      | `range`     | [[Sequence]]s | Non-primitive | No      |
| [[Tuple]]      | `tuple`     | [[Sequence]]s | Non-primitive | No      |
| [[List]]       | `list`      | [[Sequence]]s | Non-primitive | **Yes** |
| [[Dictionary]] | `dict`      | [[Mapping]]   | Non-primitive | **Yes** |
| [[Set]]        | `set`       | [[Set]]s      | Non-primitive | **Yes** |
| [[Frozen set]] | `frozenset` | [[Set]]s      | Non-primitive | No      |
They can be further subdivided into [[Sequence]]s, [[Mapping]]s and [[Set]]s.

---
[[String]]s behave so similarly to collections that sometimes we can interpret them as such. If we were to add them to the table above they would be like:

| Type    | Class | Category       | Kind      | Mutable |
| ------- | ----- | -------------- | --------- | ------- |
| strings | `str` | text sequences | Primitive | No      |
However they are not collections, as the following lines of code prove:
```python
letters = ['a', 'b', 'θ', 'd', 'e']
char = letters[2]
print(char is letters[2])     # True
letters = 'abθde'
char = letters[2]
print(char is letters[2])     # False
```

---
All can be arguments of `len` [[Function]]:
```python
print(len('Launch School'))       # 13 (string)
print(len(range(5, 15)))          # 10 (range)
print(len(range(5, 15, 3)))       # 4 (range)
print(len(['a', 'b', 'c']))       # 3 (list)
print(len(('d', 'e', 'f', 'g')))  # 4 (tuple)
print(len({'foo': 42, 'bar': 7})) # 2 (dict)
print(len({'foo', 'bar', 'qux'})) # 3 (set)
```
