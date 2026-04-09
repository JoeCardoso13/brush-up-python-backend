Python provides several hundred modules with the main Python distribution. You can read about these modules [here](https://docs.python.org/3/py-modindex.html). The `import` [[Statement]] is used in Python to load code from Python modules into your code. The most basic way to load a module is to write `import module_name`, where `module_name` is the module's name. The `import` [[Statement]](s) are conventionally coded at the very top of the program file. You can also import just the names you want by using the `from` statement:
```python
from math import pi, sqrt

print(sqrt(pi))             # 1.7724538509055159
```
If you want, you can use an alias:
```python
import math as m

print(m.sqrt(m.pi))         # 1.7724538509055159
```
