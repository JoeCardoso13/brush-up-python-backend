The **scope** of an [[Identifier]] determines where you can use it. Python determines scope by looking at where you initialize the [[Identifier]]. In Python, [[Identifier]]s have **function scope**. That means that anything initialized inside a [[Function]] is only available within the body of that [[Function]] and any nested [[Function]]s. No code outside of the [[Function]] body can access that [[Identifier]].

Be ware of [[Variable shadowing]].

Python can have nuances that overlay its scoping rules:
```python
def scope_test():
    if True:
        foo = 'Hello'
    else:
        bar = 'Goodbye'

    print(foo)
    print(bar)

scope_test()

# Outputs
# Hello
# UnboundLocalError: cannot access local variable
# 'bar' where it is not associated with a value
```
Technically `bar` is within scope, but Python has this extra rule for cases like this.

---
Scope in Python can also be referred do as [[Namespace]]s.

---
Python allows us to override normal [[Function]] scoping rules with `global` and `nonlocal` [[Statement]]s.
* With `global`, Python is told to look to the outermost scope (the global scope) for the variable to be used. It works in any function. Example:
```python
greeting = 'Salutations'

def well_howdy(who):
    global greeting
    greeting = 'Howdy'
    print(f'{greeting}, {who}')

well_howdy('Angie')
print(greeting)
# Howdy, Angie
# Howdy
```
* The `nonlocal` [[Statement]] only works in nested [[Function]]s: [[Function]]s that are defined inside an outer [[Function]]. When Python processes a `nonlocal` [[Statement]], it looks for the associated [[Variable]] in one of the outer [[Function]]s. Example:
```python
def outer():
    def inner1():
        def inner2():
            nonlocal foo
            foo = 3
            print(f"inner2 -> {foo} with id {id(foo)}")

        nonlocal foo
        foo = 2
        inner2()
        print(f"inner1 -> {foo} with id {id(foo)}")

    foo = 1
    inner1()
    print(f"outer -> {foo} with id {id(foo)}")

outer()
# inner2 -> 3 with id 4339312328
# inner1 -> 3 with id 4339312328
# outer -> 3 with id 4339312328     # All 3 are the same
```
