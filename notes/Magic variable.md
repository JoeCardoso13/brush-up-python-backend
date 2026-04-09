Python has a handful of **magic variables**, aka **dunder variables**, that are primarily useful for debugging and testing. Noticeable ones:
* `__name__`: returns the current [[Module]]'s name as a [[String]]. Example:
In mod1.py we have:
```python
print(__name__)
```
In mod2.py we have:
```python
print(__name__)
```
In test.py we have:
```python
import mod1
import mod2

print(__name__)
```
When we run test.py we get:
```
mod1
mod2
__main__
```
This is why sometimes we see code like this:
```python
if __name__ == '__main__':
    # call the program's main processing function
```
This code runs the entire program when the module is the main program. It does nothing otherwise. This lets you test your code in a more piecemeal style without running the full program version.
* `__file__`: returns the full path name of the current running program.
* `__dict__`: returns a [[Dictionary]] of all the [[Instance variable]]s defined by an [[Object]]. Example:
```python
class MyClass:

    def __init__(self, x):
        self.x = x
        self.y = []
        self.z = 'xxx'

obj = MyClass(5)
print(obj.__dict__)
# {'x': 5, 'y': [], 'z': 'xxx'}
```
