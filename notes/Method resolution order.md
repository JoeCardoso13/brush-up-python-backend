Defines where Python looks for a [[Method]]. The search is a modified "depth first" search that considers all items listed in the [[Inheritance]] list, even those that are being used as [[Mix-in]]s.

If we assume that [[Mix-in]]s are listed first in the [[Inheritance]] list, and no more than one superclass is listed, you can describe the process with pseudocode:
- set the current class to the class of the calling object
- while the current class is not `None`:
    - if the current class has the method, stop searching
    - for each mix-in in the current class's inheritance list:
        - if the mix-in has the method, stop searching
    - set the current class to the superclass of the current class
- raise an `AttributeError`
 
 `mro` is a [[Class method]] defined by the `type` metaclass.
