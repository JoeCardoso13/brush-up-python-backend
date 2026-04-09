They all follow the same pattern, so first let's illustrate it by using [[Magic method]]s `__add__` and `__iadd__` to create the analogous of addition [[Instance method]]s to a Vector [[Class]] (and the [[Magic method]] `__repr__` to display):
```python
class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented

        new_x = self.x + other.x
        new_y = self.y + other.y
        return Vector(new_x, new_y)

    def __iadd__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented

        self.x += other.x
        self.y += other.y
        return self

    def __repr__(self):
        x = repr(self.x)
        y = repr(self.y)
        return f'Vector({x}, {y})'

v1 = Vector(5, 12)
v2 = Vector(13, -4)
print(v1 + v2)   # Vector(18, 8)
```
Other [[Arithmetic operation]] [[Method]]s include `__sub__` (subtraction with `-`), `__mul__` (multiplication with `*`), `__truediv__` (floating division with `/`), and `__floordiv__` (integer division with `//`). There are several more you can use. As with `__add__` and `__iadd__`, you should normally define the `__isub__`, `__imul__`, `__itruediv__`, and `__ifloordiv__` methods when you define the primary method.

The [[Arithmetic operation]]s should obey the commutative and associative laws of arithmetic, as appropriate.
