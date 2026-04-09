The basic ones are:

| Operator | Operation        |
| -------- | ---------------- |
| `+`      | Addition         |
| `-`      | Subtraction      |
| `*`      | Multiplication   |
| `/`      | Division         |
| `//`     | Integer division |
| `%`      | Modulo           |
| `**`     | Exponentiation   |
Some operations can be used on [[Type]]s other than [[Integer]] and [[Float]]:
* [[String]]s:
```
>>> 'foo' + 'bar' 
'foobar'

print('abc' * 3) # 'abcabcabc' 
print(3 * 'abc') # 'abcabcabc'
```
* [[Boolean]]s:
```
print(True + True + True)     # 3
print(True + 1 + 1.0)         # 3.0
print(False * 5000)           # 0
```
* [[List]]s:
```
>>> [1, 2, 3] + [4, 5, 6]
[1, 2, 3, 4, 5, 6]
```
* [[Set]]s:
```
>>> {1, 2, 3} | {2, 3, 4, 5}
{1, 2, 3, 4, 5}
```
