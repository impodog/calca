"""calca.run
---
Threading through(this requires _thread)
---

    >>> import calca.run
    >>> A=1
    >>> def cal(plus):
    ...     global A
    ...     A+=plus
    ...
    >>> def printout():
    ...     global A
    ...     print(A)
    ...
    >>> THcal=calca.run.through(cal,0,10)
    ... #'0' is sleep time and '10' is for the argument for 'cal'
    >>> THout=calca.run.through(printout,0)
    >>> THcal.startup();\
    ... THout.startup()
    11
    21
    31
    41
    51
    61
    71
    81
    91"""
import _thread as th
import time,traceback

class through:
    def __init__(self,func,sleeptime:int=0,ontime:bool=False,*args,**kwargs):
        """Gives a instance keeping a function to run on thread.

        Args:
            func (function): The function needed to run on thread(no looping)
            sleeptime (int, optional): What time needed to sleep after each loop. Defaults to 0.
            ontime (bool, optional): If the function can loop itself. Defaults to False.
            
            The following args are what needed to give to the function.
        """
        self._switch=True
        self._args=args
        self._kwargs=kwargs
        if not ontime:
            def LOOP(sleeptime:int=sleeptime):
                while self.switch:func(*self._args,**self._kwargs);time.sleep(sleeptime)
            self.loop=LOOP
        else:self.loop=func
    @property
    def switch(self)->bool:
        """Gives the switch bool."""
        return self._switch
    def start(self)->None:
        """Start the thread (not including to startup).
Already started on default."""
        self._switch=True
    def end(self)->None:
        """End the thread."""
        self._switch=False
    def startup(self)->None:
        """Startup the thread, end on self.end()"""
        try:th.start_new_thread(self.loop,tuple())
        except TypeError:raise TypeError("'%s' object is not callable."%(str(type(self.loop),)))