You can use the `sorted` [[Function]] to create a sorted [[List]] from any [[Iterable]] [[Collection]], mutable or immutable. It creates and returns a sorted [[List]] from the elements in the [[Collection]]. The original [[Collection]] is unchanged.
```python
names = ('Grace', 'Clare', 'Allison', 'Trevor')
print(sorted(names)) # ['Allison', 'Clare', 'Grace', 'Trevor']
print(names) # ('Grace', 'Clare', 'Allison', 'Trevor')
```

By default, it does an ascending sort using the `<` operator to compare elements from the [[Collection]]. You can reverse the sort by adding a `reverse=True` **keyword argument** to the argument list

You can also pass a `key=func` keyword argument to tell `sort` or `sorted` how to determine what values it should sort. With `key=str.casefold`:
```python
words = ['abc', 'DEF', 'xyz', '123']
print(sorted(words))
# ['123', 'DEF', 'abc', 'xyz']

print(sorted(words, key=str.casefold))
# ['123', 'abc', 'DEF', 'xyz']
```
