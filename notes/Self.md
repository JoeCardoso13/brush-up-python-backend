The most important thing to understand about `self` is that it always represents an [[Object]]. What [[Object]], though? It's the calling [[Object]] for a [[Method]].

Things become slightly more confusing when dealing with [[Inheritance]]:
```python
class Pet:

    def __init__(self, name):
        self.name = name

    def speak(self, sound):
        print(f'{self.name} says {sound}!')

class Cat(Pet):

    def speak(self):
        super().speak('meow')

cheddar = Cat('Cheddar')
cheddar.speak()
```
The actual calling [[Object]] is a `Cat` object. It's that [[Object]] that `self` refers to. The invocation of `super()` on line 12 returns an [[Object]] that lets you call [[Method]]s from the superclass of an [[Object]]. Thus `super().speak('meow')` calls the `speak` method from the `Pet` class.

The name `self` is a convention. The first parameter defined for any [[Instance method]] always represents the calling [[Object]], no matter what name used.

Note: in writing [[Instance method]]s of a [[Class definition]] always, 100% of the times, it is necessary to include the [[Self]] as first parameter.
