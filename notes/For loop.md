`for` loops have the same purpose as [[While]] loops, but they use a condensed syntax that works well when iterating over [[List]]s and other [[Sequence]]s. A `for` loop lets you forget about indexing your [[Sequence]]s. You don't have to initialize or increment the index value or even need a [[Conditional expression]]. Moreover, `for` loops work on all built-in [[Collection]]s (including [[String]]s). Most loops you write in Python will be `for` loops. The basic syntax is:
```python
for element in collection:
    # loop body: do something with the element
```
Using a `for` loop with a [[Dictionary]] iterates over the `dict` keys by default. Or you can use [[Tuple]] unpacking without parenthesis like so:
```python
# Looping over a dictionary's key/value pairs
my_dict = {'a': 1, 'b': 2, 'c': 3}
for key, value in my_dict.items():
    print(f'{key} = {value}')
```
