String literals with an `r` prefix are **raw string literals**. Raw string literals don't recognize escapes, so you can use literal `\` characters freely.

```python
# Both of these print C:\Users\Xyzzy
print("C:\\Users\\Xyzzy")  # Each \\ produces a literal \
print(r"C:\Users\Xyzzy")  # raw string literal
```
