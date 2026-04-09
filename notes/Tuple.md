Are just like [[List]], but immutable. Being immutable allows some low-level performance optimizations. Here's an example:
```python
>>> tup = ('xyz', [2, 3, 4], 1, True) 
>>> tup 
('xyz', [2, 3, 4], 1, True)
```
If you try to do [[Index reassignment]] you get a [[TypeError]].
