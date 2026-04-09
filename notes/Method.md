Method invocations occur when you prepend an [[Object]] followed by a period (`.`) to a [[Function invocation]], e.g., `'xyzzy'.upper()`. We call such [[Function invocation]]s **method calls**. You can think of the previous code as the function `upper` returning a modified version of the [[String]] `'xyzzy'`.

All methods are [[Function]]s, but **not** vice-versa. Every method belongs to a [[Class]] and requires an [[Object]] of that [[Class]] to invoke it.

---
In Python, the distinction between [[Function]]s and methods may sometimes seem fuzzy. Some [[Function invocation]]s look like method invocations. For instance, consider the `math` [[Module]] from Python's standard libraries. The [[Module]] provides some mathematical [[Function]]s that any program can use. Once you import the [[Module]], you just call the [[Function]]s you need:
```python
import math

print(math.sqrt(5))           # 2.23606797749979
```
While `math` is technically a reference to a [[Module]] [[Object]], we're not using it to perform operations on that [[Object]]. The sole purpose of the `math` [[Object]] here is to tell Python where to look for those [[Function]]s.

---
From built-in [[Type]]s we got some [[Common method]]s.
