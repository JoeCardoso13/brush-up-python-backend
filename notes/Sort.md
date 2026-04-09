It reorders the elements in the [[Collection]] caller (returns `None`).
```python
names = ('Grace', 'Clare', 'Allison', 'Trevor')
print(names) # ('Grace', 'Clare', 'Allison', 'Trevor')
print(names.sort())   # None
print(names) # ['Allison', 'Clare', 'Grace', 'Trevor']
```
It's worth noting that this [[Method]] is a bit faster and less memory intensive than the [[Built-in function]] [[Sorted]] since the [[Method]] does an in-place sort, so doesn't have to build a completely new list.

By default, it does an ascending sort using the `<` operator to compare elements from the [[Collection]]. You can reverse the sort by adding a `reverse=True` **keyword argument** to the argument list

You can also pass a `key=func` keyword argument to tell it how to determine what values it should sort. With `key=int`:
```python
numbers = ['1', '5', '100', '15', '534', '53']
numbers.sort()
print(numbers)   # ['1', '100', '15', '5', '53', '534']

numbers.sort(key=int)
print(numbers)   # ['1', '5', '15', '53', '100', '534']
```
