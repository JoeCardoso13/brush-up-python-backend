`cls` is nearly identical to [[Self]] in almost all respects. However, it conventionally references a [[Class]] rather than an ordinary [[Object]]. In Python, though, [[Class]]es are instance [[Object]]s, too! They are instantiated from the `type` [[Class]]. Theoretically, there is no difference between `cls` and [[Self]].

The fact that [[Class]]es are [[Object]]s suggests something: you can use `super()` to reference a [[Class method]] in a superclass.
```python
class Animal:

    @classmethod
    def make_sound(cls):
        print(f'{cls.__name__}: A generic sound')

class Dog(Animal):

    @classmethod
    def make_sound(cls):
        super().make_sound()
        print(f'{cls.__name__}: Bark')

Dog.make_sound()
# Dog: A generic sound
# Dog: Bark
```
