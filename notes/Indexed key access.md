It's indexed access to individual elements in the [[Sequence]]. Indices begin at 0 and run through 1 less than the length of the [[String]] or [[Sequence]] (Indices may also be negative in the range `-1` to `-len(seq)`). Any index used must be in this range, or you will get an `IndexError`:
```python
my_str = "abc"                # string
print(my_str[0])              # 'a'
print(my_str[1])              # 'b'
print(my_str[2])              # 'c'
print(my_str[3])
# IndexError: string index out of range

my_range = range(5, 8)         # range
print(my_range[0])             # 5
print(my_range[1])             # 6
print(my_range[2])             # 7
print(my_range[3])
# IndexError: range object index out of range

my_list = [4, 5, 6]           # list
print(my_list[0])             # 4
print(my_list[1])             # 5
print(my_list[2])             # 6
print(my_list[3])
# IndexError: list index out of range

tup = (8, 9, 10)              # tuple
print(tup[0])                 # 8
print(tup[1])                 # 9
print(tup[2])                 # 10
print(tup[3])
# IndexError: tuple index out of range
```
