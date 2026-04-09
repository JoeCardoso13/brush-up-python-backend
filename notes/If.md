Consist in the use of the keywords `if`, `elif` and `else` along with corresponding blocks of code. The shole thing is a [[Statement]]. The blocks can't be empty so if you don't want a certain block to do anything you write `pass`:
```python
if value == 3:
    print('value is 3')
elif value == 4:
    print('value is 4')
elif value == 9:
    pass # We don't care about 9
else:
    print('value is something else')
```

The conditional evaluates its condition in terms of [[Truthiness]]. [[Logical operator]]s are also sometimes employed.

Sometimes they can be converted (back-and-forth) to a [[case statement]]. 

When the return value is needed, we can use a [[Ternary operator]] [[Expression]].
