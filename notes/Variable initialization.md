When you initialize a [[Variable]], Python gives it an initial value and sticks that value somewhere in the computer's memory. It also allocates a small amount of memory for the [[Variable]] itself, then places the value's memory address into the variable's spot in memory.

For instance, consider this code:
```python
foo = 'abcdefghi'
```

When Python encounters this code, it will create the string `'abcdefghi'` somewhere in memory. Let's assume Python stores the string at memory address 73420. Next, it creates a variable somewhere else in memory. Let's suppose the [[Variable]] is at address 10230. It then associates address 10230 with the name `foo`. Python stores the address of the string (73420) at address 10230. Thus, we get a situation that looks like this:
If we later do:
```python
foo = 'Hello'
```
That's a [[Variable reassignment]].
