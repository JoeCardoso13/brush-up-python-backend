Suppose you have 3 [[Class]]es, `Car`, `House` and `Smartlight` and they all need a [[Getter]] and [[Setter]] for their color [[Attribute]]. Instead of repeating code, you can make a [[Module]] and import it as follows:
```python
class ColorMixin:

    def set_color(self, color):
        self._color = color

    def get_color(self):
        return self._color
```
```python
from color_mixin import ColorMixin

class Car(ColorMixin):

    def __init__(self, color):
        self.set_color(color)
```
```python
from color_mixin import ColorMixin

class SmartLight(ColorMixin):

    def __init__(self, color):
        self.set_color(color)
```
```python
from color_mixin import ColorMixin

class House(ColorMixin):

    def __init__(self, color):
        self.set_color(color)
```
It's worth noting that we've named our mix-in [[Class]] with a `Mixin` suffix. This is a common Python convention.
