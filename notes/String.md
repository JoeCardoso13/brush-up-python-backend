A **string** is a text sequence of Unicode characters.

Text sequences can often be treated as ordinary [[Sequence]]. For instance:
```python
greeting = 'hello'
for letter in greeting:
    print(letter)
# h
# e
# l
# l
# o
```
There is one significant difference between a text sequence and an ordinary [[Sequence]]. Ordinary [[Sequence]]s contain zero or more [[Object]]s, but a text sequence does **not** contain any [[Object]]s: it simply contains the characters (or bytes) that make up the text sequence. Those characters or bytes are **not** [[Object]]s; they are simply part of the value.

---
String [[Literal]]s can have single, double or triple quotes:
```python
'Hi there'                      # Single quotes
"Monty Python's Flying Circus"  # Double quotes

# Triple single quotes
'''King Arthur: "What is your name?"
Black Knight: "None shall pass!"
King Arthur: "What is your quest?"
Black Knight: "I have no quarrel with you,
               but I must cross this bridge."
'''

# Triple double quotes
"""Man: "Is this the right room for an argument?"
Other Man: "I've told you once."
Man: "No you haven't!"
"""
```
---
Supports [[Indexed key access]] along with all [[Collection]] [[Type]]s. Also supports [[Indexed slicing]]

---
They can be prefixed with an `r` or `f` corresponding to [[Raw string]]s and [[String interpolation]] respectively.
