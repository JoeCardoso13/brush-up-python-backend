It's where the state and behavior of [[Object]]s from the [[Class]] are defined. The former is given by the [[Instance variable]]s whereas the latter is given by the [[Instance method]]s. Example:
```python
class GoodDog:

    def __init__(self, name):
        # self.name is an instance variable (state)
        self.name = name
        print(f'Constructor for {self.name}')

    # speak is an instance method (behavior)
    def speak(self):
        # We're using the self.name instance variable
        print(f'{self.name} says Woof!')

    # roll_over is an instance method (behavior)
    def roll_over(self):
        # We're using the self.name instance variable
        print(f'{self.name} is rolling over.')

sparky = GoodDog('Sparky') # Constructor for Sparky
sparky.speak()             # Sparky says Woof!
sparky.roll_over()         # Sparky is rolling over.

rover = GoodDog('Rover')   # Constructor for Rover
rover.speak()              # Rover says Woof!
rover.roll_over()          # Rover is rolling
```
* The [[Magic method]] `__init__` is the [[Initializer]] [[Method]] or **instance constructor**.
* `speak` and `roll_over` are [[Instance method]]s.
* `name` is an [[Instance variable]].
