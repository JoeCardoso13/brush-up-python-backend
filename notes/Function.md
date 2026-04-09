Most languages support the concept of **procedures**, blocks of code that run as separate units. In Python, we call these **functions** or [[Method]]s.

As of Python 3.11.4, there are approximately 70 [[Built-in function]]s.

Functions that always return a [[Boolean]] value are (conventionally) called [[Predicate]]s.

You can have *default parameters* with the following syntax:
```python
def say(text='hello'):
    print(text + '!')

say('Howdy') # Howdy!
say()        # hello!
```
But you can never have a mandatory parameter after a default one:
```python
def say(msg1, msg2, msg3='dummy message', msg4):
    pass
# SyntaxError: non-default argument follows default argument
```
---
Always have the [[Function definition]] on top of the [[Function invocation]] so you don't get a [[NameError]].
