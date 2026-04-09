**Classes** form the basis of Python's [[Type]] system. You can think of classes as blueprints, templates, or molds from which we create [[Object]]s of a given [[Type]]. A class, by default, can create many different [[Object]]s of the same [[Type]]. The basic syntax of a [[Class definition]] is:
```python
class GoodDog:
    pass

sparky = GoodDog()
```
Each class defines a [[Constructor]] of the same name.

Every class defines a [[Type]], and every [[Type]] has a class. These two terms are so fundamentally similar that we often use them interchangeably.

---
All Python [[Class]]es are instances of the `type` **metaclass**. A metaclass is a [[Class]] that creates other [[Class]]es. As a result, [[Class]]es can call [[Method]]s defined on `type`.
