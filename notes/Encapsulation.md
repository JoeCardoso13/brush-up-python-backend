Python doesn't have built-in encapsulation. This means that, in the following code:
```python
class GoodDog:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def speak(self):
        return f'{self.name} says arf!'

sparky = GoodDog('Sparky', 5)
print(sparky.speak())  # Sparky says arf!

rover = GoodDog('Rover', 3)
print(rover.speak())   # Rover says arf!
```
We could do this:
```python
print(sparky.name)            # Sparky
```
Or even this:
```python
sparky.name = 'Fido'
print(sparky.name)            # Fido
```
And there's nothing that can be done to impede the access and [[Variable reassignment]] of this [[Instance variable]].

There are 2 conventions used to simulate encapsulation in Python through "private" [[Attribute]]s:
* Single underscore:
You simply prepend the [[Instance variable]] or [[Instance method]] name with an `_` as a signal to developers to only use them internally, within the [[Class definition]]. 
* [[Name mangling]]

[[Property]] [[Decorator]]s also help with encapsulation.
