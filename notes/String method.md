### Letter Case

- `str.capitalize` returns a copy of `str` with the first character capitalized and the remaining characters converted to lowercase.
- `str.title` returns a copy of `str` with every word in the string capitalized. The remaining characters are converted to lowercase.
- `str.swapcase` returns a copy of `str` with every uppercase letter converted to lowercase, and vice versa.
### Character Classification

- `str.isalpha()` returns `True` if all characters of `str` are alphabetic, `False` otherwise. It returns `False` if the string is empty.
- `str.isdigit()` returns `True` if all characters of `str` are digits, `False` otherwise. It returns `False` if the string is empty.
- `str.isalnum()` returns `True` if `str` is composed entirely of letters and/or digits, `False` otherwise. It returns `False` if the string is empty.
- `str.islower()` returns `True` if all cased characters in `str` are lowercase letters, `False` otherwise. It returns `False` if the string contains no case characters.
- `str.isupper()` returns `True` if all cased characters in `str` are uppercase, `False` otherwise. It returns `False` if the string contains no case characters.
- `str.isspace()` returns `True` if all characters in `str` are **whitespace characters**, `False` otherwise. It returns `False` if the string is empty. The whitespace characters include ordinary spaces (), tabs (`\t`), newlines (`\n`), and carriage returns (`\r`). It also includes two rarely used characters: vertical tabs (`\v`) and form feeds (`\f`), as well as some foreign characters that count as whitespace.
### Stripping Characters

* The `str.strip` method returns a copy of `str` with all leading and trailing whitespace characters (see `str.isspace` above) removed. You can also tell `strip` to remove other characters by providing a [[String]] argument. The characters inside this [[String]] are the ones you want removed.
* The `str.lstrip` method is identical to `str.strip` except it only removes leading characters (the leftmost).
* `str.rstrip` removes trailing characters (the rightmost).
### startswith and endswith
* `str.startswith` returns `True` if the [[String]] given by `str` begins with a certain substring, `False` if it does not.
* `str.endswith` returns `True` if the [[String]] given by `str` ends with a certain substring, `False` if it does not.
### Splitting and Joining Strings

* The `str.split` method returns a list of the words in the [[String]] `str`. By default, `split` splits the [[String]] at sequences of one or more whitespace characters.
* `str.splitlines` returns a list of lines from the [[String]] `str`. `splitlines` looks for line-ending characters like `\n` (line feed), `\r` (carriage return), `\n\r` (new lines), and a variety of other line boundaries.
* `str.join`, concatenates all [[String]]s in an [[Iterable]] [[Collection]] into a single lone [[String]]. Each [[String]] from the [[Collection]] gets concatenated to the previous [[String]] with the value of `str` between them.
### Finding Substrings
* `str.find` searches through `str` looking for the first occurrence of the argument. It returns the index of the first matching substring. Otherwise, returns `-1`.
* `str.rfind` searches from right to left (that is, in reverse). It returns the index of the first matching substring. Otherwise, they return `-1`.
