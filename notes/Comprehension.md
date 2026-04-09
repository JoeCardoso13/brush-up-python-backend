They are a shorthand syntax that allows you to perform both **selection** and **transformation**, simultaneously, on certain [[Type]]s of [[Iterable]]s. They can return a [[List]], a [[Dictionary]] or a [[Set]].
* [[List]]
It's the most common form of comprehension. The basic syntax is:
```python
[ expression for element in iterable if condition ]
```
Here the [[Iterable]] is selected and transformed into a [[List]]. 

It's common to use multiple lines when the comprehension [[Expression]] gets too long:
```python
cats_colors = {
    'Tess':   'brown',
    'Leo':    'orange',
    'Fluffy': 'gray',
    'Ben':    'black',
    'Kat':    'orange',
}

names = [ name.upper()
          for name in cats_colors
          if cats_colors[name] == 'orange'
          if name[0] == 'L' ]
print(names) # ['LEO']
```
You may also concatenate [[For loop]] components like so:
```python
suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
ranks = [
    '2', '3', '4', '5', '6', '7', '8', '9', '10',
    'Jack', 'Queen', 'King', 'Ace',
]

deck = [ f'{rank} of {suit}'
         for suit in suits
         for rank in ranks ]
print(deck)
```
* [[Dictionary]]
The basic syntax is:
```python
{ key: value for element in iterable if condition }
```
Example:
```python
squares = { f'{number}-squared': number * number
            for number in range(1, 6) }
print(squares)
# pretty-printed for clarity.
# {
#     '1-squared': 1,
#     '2-squared': 4,
#     '3-squared': 9,
#     '4-squared': 16,
#     '5-squared': 25
# }
```
* [[Set]]
The basic syntax is:
```python
{ expression for element in iterable if condition }
```
Example:
```python
squares = { number * number for number in range(1, 6) }
print(squares)      # {1, 4, 9, 16, 25}
```
