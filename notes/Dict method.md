Python provides 3 [[Method]]s to get lists of the keys, values, and key/value pairs from a [[Dictionary]]. Those [[Method]]s are `dict.keys`, `dict.values`, and `dict.items`. Let's see them in action:
```python
people_phones = {
    'Chris': '111-2222',
    'Pete':  '333-4444',
    'Clare': '555-6666',
}

print(people_phones.keys())
# dict_keys(['Chris', 'Pete', 'Clare'])

print(people_phones.values())
# Pretty printed for clarity
# dict_values([
#     '111-2222',
#     '333-4444',
#     '555-6666'
# ])

print(people_phones.items())
# Pretty printed for clarity
# dict_items([
#     ('Chris', '111-2222'),
#     ('Pete',  '333-4444'),
#     ('Clare', '555-6666')
# ])
```
The return value of the [[Method]]s aren't ordinary [[List]]s but **dictionary view objects** that are tied to the [[Dictionary]]. If you add a new key/value pair to the [[Dictionary]], remove an element, or update a value, the corresponding [[List]]s are updated immediately:
```python
people_phones = {
    'Chris': '111-2222',
    'Pete':  '333-4444',
    'Clare': '555-6666',
}

keys = people_phones.keys()
values = people_phones.values()

print(keys)    # dict_keys(['Chris', 'Pete', 'Clare'])
print(values)
# dict_values(['111-2222', '333-4444', '555-6666'])

people_phones['Max'] = '123-4567'
people_phones['Pete'] = '345-6789'
del people_phones['Chris']

print(keys)    # dict_keys(['Pete', 'Clare', 'Max'])
print(values)
# dict_values(['345-6789', '555-6666', '123-4567'])
```
