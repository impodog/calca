"""
calca.point
---
Simulate pointers
---
 
This is easy to use so there'd be only some examples

Examples
---
    >>> import calca.point
    >>> A = 9
    >>> ptrA = calca.point.mk(9).new
    ... #Makes the pointer of number '9'
    >>> print(calca.point.mk(ptrA).get
    ... #Gets the value from pointer 'ptrA'
    9
    >>> otherptrA = ptrA = calca.point.mk(A).ptr
    ... #Find a known pointer of 'A'
    >>> otherptrA == ptrA
    ... #They're the same pointer
    True"""
from calca.overall import*
points=list()
class mk(object):
    """Trying to make a pointer or gets a pointer.

    .new --- Make a new pointer
    .get --- Get from a pointer
    .ptr --- Find an item's pointer.
    """
    def __init__(self,_o:object):self.o=_o
    @property
    def new(self):points.append(self.o);return len(points)-1
    @property
    def get(self):return points[self.o]
    @property
    def ptr(self):
        try:return points.index(self.o)
        except:raise ValueError("Value Not Existing.")
