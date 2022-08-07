"""Calculate common ADVANCED!
------
See help() to get avalible imports.(Or 'import calca' to import all initial modules)

Initial Modules
------
    - calca.factoring : Prime numbers and prime factors
    - calca.numeries : Sqrt and an array of numbers
    - calca.screening : Calculate screen resolution
    - calca.sets : Sets and giving more classes
    - calca.text : Text operate, spliting calculate
    - calca.unicode : Unicode and shift on keyboard
    - calca.simple : Simple calculation


Not in initial because they're either too slow or not necessary
------
    - calca.point : Simulate pointers
    - calca.sort : Provide common sort methods
    - calca.pysp : Python function extending
    - calca.run : Running threads
    - calca.console : Easy terminal prints
    - calca.coord : Coordinate calculation

Useful
------
    >>> from calca.notinitial import*
    ... #This imports all the not initial modules
    >>> import calca.support
    >>> calca.support.see()
    ... #This shows the support message
    ... #Run python help() to see the module in calca


New/Fixed things in the 0.2.1.6 compared to the last one.
------
    - rbystr change
"""
__version__="0.2.1.6"
from calca.overall import*
from calca.factoring import*
from calca.screening import*
from calca.numeries import*
from calca.unicode import*
from calca.text import*
from calca.sets import*
from calca.simple import*