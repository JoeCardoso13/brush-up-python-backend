A.k.a F-[[String]]s.

Their basic syntax is:
```python
f'Blah {expression} blah.'
```
Python replaces the `{expression}` substring with the value of the expression inside the braces: it **interpolates** the expression's value.

You can escape the interpolation by using double curly braces instead.

---
They have interesting properties when dealing with numeric [[Type]]s:
```python
print(f'{123456789:_}')       # 123_456_789
print(f'{123456789:,}')       # 123,456,789
print(f'{123456.7890123:_}')  # 123_456.7890123
print(f'{123456.7890123:,}')  # 123,456.7890123
```
