Since Python doesn't have a syntactical difference between [[Variable reassignment]] and [[Variable initialization]], the following happens:
```python
greeting = 'Salutations'

def well_howdy(who):
    greeting = 'Howdy'
    print(f'{greeting}, {who}') # Howdy, Angie

well_howdy('Angie')
print(greeting) # Salutations
```
Even though the `greeting` [[Variable]] was shadowed within the [[Function definition]], there was no [[Variable reassignment]] taking place.
