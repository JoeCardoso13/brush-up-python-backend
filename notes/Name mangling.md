The use of double underscore, `__`, provides a little syntactical benefit over the signal convention of "privacy"  given by use of single underscore, `_`, for [[Encapsulation]]:
```python
class GoodDog:

    def __init__(self, name, age):
        self.__name = name
        self._age = age

    def speak(self):
        return f'{self.__name} says arf!'

sparky = GoodDog('Sparky', 5)

sparky.__name = 'Fido'
print(sparky.__name)         # Fido
print(sparky.speak())        # Sparky says arf!

sparky._GoodDog__name = 'Fido'
print(sparky._GoodDog__name) # Fido
print(sparky.speak())        # Fido says arf!
```
The attempt to change the name using the unmangled name, `__name`, initially seemed to work. However, `sparky.speak()` didn't reflect the name change. Instead, Python created a new `__name` [[Instance variable]] that `speak` doesn't know about. However the following lines of code show how easy it is to defeat name mangling.
