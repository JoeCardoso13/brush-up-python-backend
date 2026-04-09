The `is` operator is kind of like the triple equal operator in JavaScript. Take, for instance:
```
>>> l = [1, 2, 3]
>>> id(l)
139980036942720
>>> l2 = list(l)
>>> id(l2)
139980036225728
>>> l == l2
True
>>> l is l2
False
```
