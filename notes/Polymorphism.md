Is when [[Method]]s of the same name can be called by different [[Object]]s in a meaningful way. Example:
```python
class Pet:

    def __init__(self, name):
        self.name = name
        type_name = type(self).__name__
        print(f'I am {name}, a {type_name}.')

    def eat(self):
        print(f"{self.name}: Yum-yum-yum!")

class Dog(Pet):

    def speak(self):
        print(f'{self.name} says Woof!')

class Cat(Pet):

    def speak(self):
        print(f'{self.name} says Meow!')

class Parrot(Pet):

    def speak(self):
        print(f'{self.name} wants a cracker!')

sparky = Dog('Sparky')
fluffy = Cat('Fluffy')
polly = Parrot('Polly')

for pet in [sparky, fluffy, polly]:
    pet.speak()
    pet.eat()
```
Some build-in examples are [[Arithmetic method]]s, [[Comparison method]]s etc.
