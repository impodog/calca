"""calca.sets
---
Set operation
---

usage
---
    >>> import calca.sets
    >>> calca.sets.reverse({1:2,7:5})
    {2:1,5:7}
    >>> A=calca.sets.unordered((3,1,2,3,4,2,3,3,3))
    >>> A[3]
    ... #This is the count of '3'
    5
    >>> A[2]=100
    ... #Change number of '2' to '100'
    >>> A.remove(2,95)
    ... #Remove 95 of '2'
    >>> A
    unordered([1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4,])
    """
from calca.overall import*
def reverse(D:dict)->dict:
    """Reverse the dict."""
    result={}
    for k,v in D.items():result[v]=k
    return result

class unordered():
    """Get an unordered list.
__getitem__ and __setitem__: item is the number of sth."""
    def __init__(self,iterable:Iterable):
        if isinstance(iterable,dict):self._count=iterable
        else:
            self._count=dict()
            for obj in set(iterable):self._count[obj]=iterable.count(obj)
    @property
    def count(self)->dict:return self._count
    def __getitem__(self,_o:object)->int:return self._count[_o]
    def append(self,_o:object,_n:int=1)->None:
        """Append sth into the object."""
        try:self._count[_o]+=_n
        except:self._count[_o]=_n
    def __setitem__(self,_o:object,_n:int)->None:self._count[_o]=_n
    def __delitem__(self,_o:object):del self._count[_o]
    def remove(self,_o:object,_n:int=1)->'None|NoReturn':
        """Remove sth from the object.
_n is the number to remove."""
        if self._count.get(_o) is not None:
            if self._count.get(_o) <= _n:del self[_o]
            else:self[_o]-=_n
        else:raise ValueError("Non-existing object to remove.")
    def __str__(self)->str:
        result='unordered(['
        for k,v in self._count.items():result+=(str(k)+', ')*v
        result=result[:-1]+'])'
        return result
    def __repr__(self)->str:return self.__str__()
def allobject(D:dict):
    """gets all the p=objects inside a dict"""
    result=[]
    for k,v in D.items():
        result+=[k,v]
    return result
def maxdimension(L:Iterable,Pure:bool=False,Current:int=0)->int:
    """Find the maximum dimension depth of a list."""
    _all=[]
    for i in L:
        if isinstance(i,Iterable):
            if type(i)==dict:_all.append(maxdimension(allobject(i),Pure,Current=Current+1))
            else:_all.append(maxdimension(i,Pure,Current=Current+1))
        elif not Pure:_all.append(Current)
        else:return Current
    if len(_all)>0:return max(_all)
    else:return Current
def opendimension(L:Iterable)->list:
    """Open all the dimensions of a list."""
    result=[]
    for i in L:
        if isinstance(i,Iterable):result+=opendimension(i)
        else:result.append(i)
    return result
def indexdimension(L:Iterable,obj:object,dim:int=0)->"tuple[int,int]|None":
    """Return (dimension, index) pairs. Return None on failure"""
    Current=0
    for i in L:
        if isinstance(i,Iterable):
            Result=indexdimension(i,obj,dim+1)
            if Result is not None:return Result
        else:
            if i is obj:return (dim,Current)
        Current += 1
    return None
def insdimension(L:Iterable,obj:object,*dim)->"tuple[int,...]|None":
    """Return the tuple of where in a list, as if L[0][1][2] -> (0,1,2)
Return None on failure"""
    for i in range(len(L)):
        if isinstance(L[i],Iterable):
            Result=insdimension(L[i],obj,*dim,i)
            if Result is not None:return Result
        else:
            if L[i] is obj:return dim+(i,)
    return None
def finddimension(L:Iterable,dims:"tuple[int,...]"):
    """Return object by the index, as if L[0][1][2]..."""
    try:
        if len(dims)>1:return finddimension(L[dims[0]],dims[1:])
        else:return L[dims[0]]
    except:raise IndexError("Cannot open the dimension on dims %d in %s"%(dims[0],str(L)))