In terms of [[Inheritance]] is helps identify [[Composition]] kinds of relationships.

Examples (comparing with [[Type function]]):
```python
print(isinstance('abc', str))    # True
print(isinstance([], set))       # False

class A:
    pass

class B(A):
    pass

b = B()

print(type(b).__name__) # B
print(type(b) is B)     # True
print(type(b) is A)     # False (b's type is # not A)
print(isinstance(b, B)) # True
print(isinstance(b, A)) # True (b is instance of A and B)
```
