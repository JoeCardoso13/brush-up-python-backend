In the following example:
```python
class GoodDog:
    pass

sparky = GoodDog()
```
Line 4 has a constructor [[Function call]]. The [[Class definition]] itself automatically generates a [[Function]] that's the constructor of the [[Class]]. 

---
Most built-in Python data [[Type]]s let the programmer create new [[Object]]s using [[Literal]] values. [[Literal]]s are great. However, you can also use special [[Function]]s called **constructors** to create new [[Object]]s. In fact, sometimes you can't use [[Literal]]s; you must use constructors to create [[Range]]s, [[Frozen set]]s, and empty [[Set]]s.

The constructor of the following [[Collection]]s: [[List]], [[Tuple]], [[Set]] and [[Frozen set]] take an [[Iterable]] as argument (or no argument, in which case they return an empty [[Collection]]). They create a [[Shallow copy]] when the argument is of the [[Type]] described by the constructor's name itself.
