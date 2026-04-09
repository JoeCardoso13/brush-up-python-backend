You can use the `min` and `max` functions to determine a collection's minimum and maximum values. The collection's objects must have an ordering that recognizes the `<` and `>` operators for comparing any pair of those objects.
```python
print(min(-10, 5, 12, 0, -20))      # -20
print(max(-10, 5, 12, 0, -20))      # 12

print(min('over', 'the', 'moon'))   # 'moon'
print(max('over', 'the', 'moon'))   # 'the'

print(max(-10, '5', '12', '0', -20))
# TypeError: '>' not supported between instances
# of 'str' and 'int'
```
You can also use `max` and `min` with a single [[Iterable]] argument, such as a list, set, or tuple:
```python
my_tuple = ('i', 'tawt', 'i', 'taw', 'a',
            'puddy', 'tat')
print(min(my_tuple)) # 'a'
print(max(my_tuple)) # 'tawt'
```
