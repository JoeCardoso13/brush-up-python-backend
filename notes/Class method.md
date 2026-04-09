They are [[Method]]s that pertain to a [[Class]] instance. [[Class]] [[Method]]s provide general services for the [[Class]] as a whole rather than the individual [[Object]]s. We usually use the [[Class]] to invoke the [[Method]]. However, Python also lets you invoke class methods with instance [[Object]]s (but avoid it).

We use the `@classmethod` [[Decorator]] to create a class method. Class methods require at least one parameter: the [[Class]] itself. By convention, the first parameter is named `cls`:
```python
class GoodCat():

    @classmethod
    def what_am_i(cls):
        print("I'm a GoodCat class!")

GoodCat.what_am_i()    # I'm a GoodCat class!
```

Ways to call a class method:
* If you need to call a class method from within another class method of the same [[Class]], you can use the [[Cls]] argument as the caller for the second method:
```python
class Foo:

    @classmethod
    def bar(cls):
        print('this is bar')

    @classmethod
    def qux(cls):
        print('this is qux')
        cls.bar()

Foo.qux()
# this is qux
# this is bar
```
* When you want to call a specific class method from outside the [[Class]] that contains the class method, use the [[Class]]'s name to call it (e.g. `Foo.qux()`). If you call a class method without using the explicit [[Class]] name, Python will use the inferred [[Class]] and the [[Method resolution order]] ([[MRO]]) to determine which class method it should use.
* If you have an instance [[Object]], `obj`, of a [[Class]] that has a class method, you can invoke that [[Method]] by using `type(obj)`, `obj.__class__`, or even `obj` as the caller. You can also use `self` inside a method, as we show below:
```python
class Foo1:

    @classmethod
    def bar(cls):
        print('this is bar in Foo1')

    def qux(self):
        type(self).bar()
        self.__class__.bar()
        self.bar()
        Foo1.bar()

class Foo2(Foo1):

    @classmethod
    def bar(cls):
        print('this is bar in Foo2')

foo1 = Foo1()
foo1.qux()
# this is bar in Foo1
# this is bar in Foo1
# this is bar in Foo1
# this is bar in Foo1

foo2 = Foo2()
foo2.qux()
# this is bar in Foo2
# this is bar in Foo2
# this is bar in Foo2
# this is bar in Foo1
```
The main difference between using `type(self).bar()` vs. `self.__class__.bar()` is readability (`obj.bar()` syntax for class methods should **not** be used).
