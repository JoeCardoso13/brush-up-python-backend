It's a syntactic notation that lets you represent an appropriately [[Type]]d [[Object]] directly in source code. Examples:
```python
'Hello, world!'   # str literal
3.141592          # float literal
True              # bool literal
{'a': 1, 'b': 2}  # dict literal
[1, 2, 3]         # list literal
(4, 5, 6)         # tuple literal
{7, 8, 9}         # set literal
```
Not all [[Object]]s have **literal** forms. In those cases, we use the [[Type]] [[Constructor]] to create [[Object]]s of the [[Type]]. For instance:
```python
range(10)         # Range of numbers: 0-9
range(1, 11)      # Range of numbers: 1-10
set()             # Empty set
frozenset([1, 2]) # Frozen set of values: 1 and 2
```
