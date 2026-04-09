The `@property` [[Decorator]] is used to create [[Getter]] [[Method]]s for an [[Instance variable]]. When you apply `@property` to a [[Method]] named `foo`, `@property` creates a secondary [[Decorator]] named `@foo.setter`; this secondary [[Decorator]] is used to create [[Setter]] [[Method]]s. (Thus, you can have a [[Getter]] without a [[Setter]], but you can't have a [[Setter]] without a [[Getter]].)

Example:
```python
class GoodDog:

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def speak(self):
        return f'{self.name} says arf!'

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError('Name must be a string')

        self._name = name

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        if not isinstance(age, int):
            raise TypeError('Age must be an integer')

        if age < 0:
            raise ValueError("Age can't be negative")

        self._age = age

sparky = GoodDog('Sparky', 5)
print(sparky.name)          # Sparky
print(sparky.age)           # 5
sparky.name = 'Fireplug'

print(sparky.name)          # Fireplug
sparky.age = 6

print(sparky.age)           # 6

sparky.name = 42  # TypeError: Name must be a string

sparky.age = -1   # ValueError: Age can't be negative
```
With this code, we seem to have two different methods called `name` and two more named `age`. The [[Decorator]]s, `@property`, `@name.setter`, and `@age.setter`, make them distinct. The `@property` prior to the first `name` [[Method]] creates the `@name.setter` [[Decorator]], while the one prior to the first `age` [[Method]] creates the `@age.setter` [[Decorator]].

Using these [[Decorator]]s means we no longer need `()` when accessing the [[Getter]] and [[Setter]]. We can also use standard assignment syntax to give an [[Instance variable]] a new value.

[[Getter]]s created with the `@property` decorator are known as **properties**.

Note:
- Only the `@property`, `@name.setter`, and `@age.setter` [[Method]]s use the underscored name. All other references that look like [[Instance variable]] accesses are, in fact, calling the property [[Method]]s.
- The name of the [[Setter]] argument is, conventionally, the same name as used by the [[Method]]. There is no need to use `new_name` or `new_age`.

As a rule, you should use properties when:
- you want to strongly discourage misuse of the [[Instance variable]]s.
- you want to validate data when your [[Instance variable]]s receive new values.
- you have dynamically computed [[Attribute]]s.
- you need to refactor your code in a manner incompatible with the existing interface.
- you want to improve your code readability, and properties can help.
