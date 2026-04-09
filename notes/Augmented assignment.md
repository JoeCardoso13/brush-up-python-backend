The shorthand [[Statement]] of utilizing and having the [[Variable]] undergo [[Variable reassignment]] at the same time, can be use for whichever valid [[Arithmetic operation]] desired:
```python
foo = 42            # foo is 42
foo -= 2            # foo is now 40
foo *= 3            # foo is now 120
foo += 5            # foo is now 125
foo //= 25          # foo is now 5
foo /= 2            # foo is now 2.5
foo **= 3           # foo is now 15.625
print(foo)          # prints 15.625
bar = 'xyz'          # bar is 'xyz'
bar += 'abc'         # bar is now 'xyzabc'
bar *= 2             # bar is now 'xyzabcxyzabc'
print(bar)           # prints xyzabcxyzabc
bar = [1, 2, 3]     # bar is [1, 2, 3]
bar += [4, 5]       # + with lists appends
print(bar)          # prints [1, 2, 3, 4, 5]
bar = {1, 2, 3}     # bar is {1, 2, 3}
bar |= {2, 3, 4, 5} # | performs set union
                    # bar is now {1, 2, 3, 4, 5}
bar -= {2, 4}       # - performs set difference
print(bar)          # prints {1, 3, 5}
```

Note: because it is indeed a [[Statement]], the following will produce an error:
```python
def foo(bar):
    print(bar)

a = 3
foo(a *= 2)
#     ^^
# SyntaxError: invalid syntax

def foo():
    a = 3
    return a *= 2
#            ^^
# SyntaxError: invalid syntax
```
---
Be aware that if the [[Variable]] of an "augmented assignment" is mutable, then often it's not really an [[Variable reassignment]] going on. For instance:
```python
bar = [1, 2, 3]     # bar is [1, 2, 3]
bar += [4, 5]       # + with lists appends
```
In the example above `bar` value was mutated, i.e. it was not really a [[Variable reassignment]].
