Python provides the `super` function to call methods in the superclass. The return value from `super()` is a proxy that let's you access the entire [[Inheritance]] hierarchy above the current [[Class]] and call any of its [[Instance method]]s that'll be found by [[MRO]]. Commonly, though, you do it for calling the [[Instance method]] of the same name above. Most commonly of all, you do it in the [[Initializer]].

When using `super()` to call an [[Instance method]] above in the [[Inheritance]] hierarchy, there's no need to pass [[Self]] as the argument. It is done automatically.
