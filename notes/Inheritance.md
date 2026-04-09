Defines a superclass <=> subclass hierarchy, which can also be understood as an "is-a" relationship. 

Example:
```python
class Pet:

    def __init__(self, name):
        self.name = name
        type_name = type(self).__name__
        print(f'I am {name}, a {type_name}.')

class Dog(Pet):

    # __init__ method removed

    def roll_over(self):
        print(f'{self.name} is rolling over.')

class Cat(Pet):

    # __init__ method removed
    pass

class Parrot(Pet):

    # __init__ method removed
    pass

sparky = Dog('Sparky') # I am Sparky, a Dog.
fluffy = Cat('Fluffy') # I am Fluffy, a Cat.
polly = Parrot('Polly') # I am Polly, a Parrot.

sparky.roll_over() # Sparky is rolling over.
```
By the way; we can rewrite `type(self).__name__` as `self.__class__.__name__`. `type(self)` and `self.__class__` return the same values.

As shown in the example above, the [[Initializer]] can be omitted from the subclasses when all it does is call [[Super]]'s own [[Initializer]].

It is possible to have **multiple inheritance**:
```python
class Pet:

    def play(self):
        print('I am playing')

class Predator:

    def hunt(self):
        print('I am hunting')

class Cat(Pet, Predator):

    def purr(self):
        print('I am purring')

cat = Cat()
cat.purr()          # I am purring
cat.play()          # I am playing
cat.hunt()          # I am hunting
```
