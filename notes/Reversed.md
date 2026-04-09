You can use the `reversed` [[Function]] to reverse the order of elements in a [[Sequence]] or [[Dictionary]]. The returned value is a lazy [[Sequence]] that contains the elements in the [[Sequence]] or the keys from a [[Dictionary]]. Since the result is lazy, you need to iterate over the result or expand it with a function list `list` or `tuple`.
```python
names = ('Grace', 'Clare', 'Allison', 'Trevor')
reversed_names = reversed(names)
print(reversed_names)
# <reversed object at 0x102848e50>
print(tuple(reversed(names))) # Requires extra memory
# ('Trevor', 'Allison', 'Clare', 'Grace')
print(names)
# ('Grace', 'Clare', 'Allison', 'Trevor')

my_dict = {'abc': 1, 'xyz': 23, 'pqr': 0, 'jkl': 5}
reversed_dict = reversed(my_dict)
print(reversed_dict)
# <dict_reversekeyiterator object at 0x100d19f80>
print(list(reversed_dict))    # Requires extra memory
# ['jkl', 'pqr', 'xyz', 'abc']
```

You sometimes want to iterate over a [[Collection]] in reverse. `reversed` makes that easy:
```python
names = ('Grace', 'Clare', 'Allison', 'Trevor')
for name in reversed(names):
    print(name)
# Trevor
# Allison
# Clare
# Grace
```
