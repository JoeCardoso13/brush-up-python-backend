`zip` iterates through 0 or more [[Iterable]]s in parallel and returns a [[List]]-like [[Object]] of [[Tuple]]s. Each [[Tuple]] contains a single [[Object]] from each of the [[Iterable]]s. To illustrate:
```python
iterable1 = [1, 2, 3]
iterable2 = ('Kim', 'Leslie', 'Bertie')
iterable3 = [None, True, False]

zipped_iterables = zip(iterable1, iterable2, iterable3)
print(list(zipped_iterables))
# Pretty printed for clarity
# [
#   (1, 'Kim', None),
#   (2, 'Leslie', True),
#   (3, 'Bertie', False)
# ]
```
`zip`'s [[Collection]] arguments are usually the same length but don't have to be. If you want to enforce identical lengths, add a `strict=True` keyword argument to the invocation:
```python
zipped_iterables = zip(iterable1, iterable2, strict=True)
```
Note: the returned [[Object]] from `zip` can only be consumed once:
```python
result = zip(range(5, 10),    # length is 5
             range(1, 3),     # length is 2 (shortest)
             range(3, 7))     # length is 4
print(list(result)) # [(5, 1, 3), (6, 2, 4)]
print(list(result)) # []
```
