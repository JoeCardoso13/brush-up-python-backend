**Sets** represent an **unordered** [[Collection]] of unique [[Object]]s; the [[Object]]s are sometimes called the **members** of the set. Sets are similar to [[Mapping]], except instead of using keys and values, a set is simply a [[Collection]] of immutable (and _hashable_) [[Object]]s.

The [[Literal]] syntax for sets is a comma-separated list of object values between curly braces (`{}`). As a special case, empty sets must be created with the `set` [[Constructor]] since `{}` by itself is an empty [[Dictionary]]. Let's see how it's done:
```
# Create a set from a literal 
>>> s2 = {2, 3, 5, 7, 11, 13} 
>>> print(s2) 
{2, 3, 5, 7, 11, 13}

# Create a set from a string 
>>> s3 = set("hello there!") 
{'t', 'o', 'e', 'l', ' ', 'h', '!', 'r'}
```
In the last example, notice that the set only contains one occurrence of each character, even though the [[String]] has repeated instances of some characters. Set members are always **unique**, even if you try to add duplicates. This example also shows that the order of the characters in the set has nothing to do with the order of the characters in the [[String]].
