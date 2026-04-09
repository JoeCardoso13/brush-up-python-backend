Consider a variable `foo` that's been initialized as follows:
```python
foo = 'abcdefghi'
```
Furthermore, assume the memory address where this [[String]] is stored is 73420 and the address of the [[Variable]] itself is 10230. If we then do:
```python
foo = 'Hello'
```
That's a variable reassignment and Python creates the new [[String]] `'Hello'` somewhere in memory. We can assume that `'Hello'` is stored at memory address 87160. Since we already have a `foo` variable, Python simply replaces the value at address 10230 with 87160. This breaks the connection with the original [[String]] and establishes a new one with the new [[String]]. Things now look like this:
