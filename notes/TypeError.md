Raised when an operation or [[Function]] is applied to an [[Object]] of inappropriate [[Type]]. The associated value is a [[String]] giving details about the type mismatch.

This exception may be raised by user code to indicate that an attempted operation on an [[Object]] is not supported, and is not meant to be. If an [[Object]] is meant to support a given operation but has not yet provided an implementation, [`NotImplementedError`](https://docs.python.org/3/library/exceptions.html#NotImplementedError "NotImplementedError") is the proper exception to raise.

Passing arguments of the wrong type (e.g. passing a [[List]] when an [[Integer]] is expected) should result in a [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError "TypeError"), but passing arguments with the wrong value (e.g. a number outside expected boundaries) should result in a [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError "ValueError").
