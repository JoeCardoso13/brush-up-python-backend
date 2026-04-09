[[Instance variable]]s capture information related to specific [[Class]] instances. Similarly, **class variables** capture information about the [[Class]]. We initialize class variables in the main [[Class definition]] body, usually at the top. We can access and manipulate them with both [[Instance method]]s and [[Class method]]s.
```python
class GoodCat:

    counter = 0                  # class variable

    def __init__(self):
        GoodCat.counter += 1

    @classmethod
    def number_of_cats(cls):
        return GoodCat.counter

class ReallyGoodCat(GoodCat):
    pass

cat1 = GoodCat()
cat2 = GoodCat()
cat3 = ReallyGoodCat()

print(GoodCat.number_of_cats())        # 3
print(GoodCat.counter)                 # 3
print(ReallyGoodCat.number_of_cats())  # 3
print(ReallyGoodCat.counter)           # 3
```
If we use `self.__class` or `cls`, we end up with some unusual results:
```python
class GoodCat:

    counter = 0                  # class variable

    def __init__(self):
        self.__class__.counter += 1

    @classmethod
    def number_of_cats(cls):
        return cls.counter

class ReallyGoodCat(GoodCat):
    pass

cat1 = GoodCat()
cat2 = GoodCat()
cat3 = ReallyGoodCat()

print(GoodCat.number_of_cats())        # 2
print(GoodCat.counter)                 # 2
print(ReallyGoodCat.number_of_cats())  # 3
print(ReallyGoodCat.counter)           # 3
```
Here, the `counter` tells us that we only have 2 `GoodCat` objects but 3 `ReallyGoodCat` objects. We only see 2 `GoodCat` objects since `cat3` ended up creating a `counter` in `ReallyGoodCat` instead of incrementing the `counter` in `GoodCat`. We also see 3 `ReallyGoodCat` objects because of inheritance.

If we want to count all `GoodCat` objects, including any instances of `ReallyGoodCat` or other subclasses, we need to increment `GoodCat.counter` explicitly instead of `self.__class__.counter`. Otherwise, we'll end up incrementing a `counter` variable in the subclass. For the same reason, we also refer to `GoodCat.counter` in the `number_of_cats` method.
