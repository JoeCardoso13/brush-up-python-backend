Using a function means **calling**, **invoking**, **executing**, or **running** it. All of those terms mean the same thing. When Python encounters a function call, it transfers program flow to the code that comprises the [[Function definition]] and executes that code. When the code finishes its work, the function **returns** a value to the code that invoked it. To illustrate:
```python
def hello():
    print('Hello')
    return True

hello()         # invoking function; ignore return value
print(hello())  # using return value in a `print` call
```
