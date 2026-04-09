Everything with a value in Python is said to be an [[Object]]. Furthermore, each object has an associated **data type** or, more concisely, **type**, which has an associated [[Class]]. For instance, the objects `42` and `123` are instances of the [[Integer]] type, i.e., the `int` [[Class]]]. Similarly, the values `True` and `False` are instances of the [[Boolean]] type, i.e., the `bool` [[Class]].

In Python, the terms _object_ and _value_ can be used interchangeably, as can the terms _class_, _data type_, and _type_. We will use them that way, too.

There are 3 main kinds of types:
- The **built-in** types are part of Python. They are available in every program if you want them; just start using them.
- The **standard** types aren't automatically loaded when running Python. Instead, they are available from [[Module]]s you can import into your programs. You don't have to download the standard types, but you do need to import them.
- The **non-standard** types come from either you and your colleagues or as downloadable [[Module]]s available on the Internet.

Python has a large number of built-in data types compared to many other languages, some of them are:

| Data Type         | Class       | Category       | Kind          | Mutable |
| ----------------- | ----------- | -------------- | ------------- | ------- |
| [[Integer]]       | `int`       | numerics       | Primitive     | No      |
| [[Float]]         | `float`     | numerics       | Primitive     | No      |
| [[Boolean]]       | `bool`      | booleans       | Primitive     | No      |
| [[String]]        | `str`       | text sequences | Primitive     | No      |
|                   |             |                |               |         |
| [[Range]]         | `range`     | sequences      | Non-primitive | No      |
| [[Tuple]]         | `tuple`     | sequences      | Non-primitive | No      |
| [[List]]          | `list`      | sequences      | Non-primitive | **Yes** |
| [[Dictionary]]    | `dict`      | mappings       | Non-primitive | **Yes** |
| [[Set]]           | `set`       | sets           | Non-primitive | **Yes** |
| [[Frozen set]]    | `frozenset` | sets           | Non-primitive | No      |
|                   |             |                |               |         |
| [[Function]]      | `function`  | functions      | Non-primitive | **Yes** |
| [[None type]]<br> | `NoneType`  | nulls          | _--?--_       | No      |

These **types** can be further categorized into [[Primitive type]] and [[Non-primitive type]] ([[None type]] being debatable but mostly [[Primitive type]]).

---
Sometimes you can transform one type into another through [[Type coercion]].

---
You can use the [[Type function]] to determine the type of a value.
