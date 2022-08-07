"""Import and define wide-used functions and module
---
See more at calca
---"""
import math,fractions,sys,os,copy,warnings
from fractions import Fraction
from typing import NoReturn,Iterable,Any,Union,overload
fr=fractions.Fraction
class CalcaQuit(Exception):...
INFINITY=float('inf')
Number=Union[int,float,fr]
def rbystr_(_f:float,digits:int=0):
    """This is the old rbystr"""
    if digits <= 0:
        try:
            if digits!=0:
                if int(_f[0][digits]) >= 5:add=10**abs(digits)
                else:add=0
                if digits<-1:return int(_f[0][:digits])*10**abs(digits)+add
                else:return int(_f[0][:digits])*10+add
            else:
                try:
                    if int(_f[1][0]) >= 5:add=1
                    else:add=0
                except:add=0
                return int(_f[0])+add
        except IndexError:return 0
    else:
        _f=str(_f).split('.')
        try:
            if int(_f[1][digits]) >= 5:add=add=0.1**abs(digits)
            else:add=0
        except IndexError:add=0
        try:return round(float('.'.join((_f[0],_f[1][:digits])))+add,digits)
        except IndexError:return float('.'.join((_f[0],_f[1])))
def rbystr(_f:float,digits:int=0):
    """The new rbystr, if it has bugs, switch back to rbystr_()"""
    if digits >= 0:return float(('%%.%df'%digits)%_f)
    else:
        try:
            if int(_f[1][digits]) >= 5:add=add=0.1**abs(digits)
            else:add=0
        except IndexError:add=0
        try:return round(float('.'.join((_f[0],_f[1][:digits])))+add,digits)
        except IndexError:return float('.'.join((_f[0],_f[1])))
def symbol(_num:'float|int')->int:
    """Gets the symbol a of number."""
    try:return int(_num // abs(_num))
    except ZeroDivisionError:return 0
def viewhelp(name:str="calca"):
    """View the helps to calca.
    >>> calca.viewhelp("drt")
    ... # Is equivalent to:
    >>> help(calca.drt)"""
    if isinstance(name,str):
        try:help(sys.modules["calca."+name])
        except KeyError:
            if name.startswith("calca"):
                try:help(sys.modules[name])
                except KeyError:print("No helps available")
            else:print("No helps available")
    else:help("calca")
def divisible(N:int,Div:int=2):return N%Div==0
def almost(a:Number,b:Number=0,frac:float=0.02)->bool:return abs(a-b)<=frac
def tupalmost(a:tuple,b:tuple,frac:float=0.02)->bool:
    for i in range(len(a)):
        if not almost(a[i],b[i],frac):return False
    return True
class rangeac():
    """Make a range across two numbers. Can only use () in ()."""
    def __init__(self,x:Number,y:Number,ledge:bool=True):self.x=min((x,y));self.y=max((x,y));self.ledge=ledge
    def __str__(self):return "rangeac("+str(self.x)+', '+str(self.y)+')'
    def __repr__(self):return str(self)
    def __contains__(self,item:'Number|rangeac'):
        if self.ledge:
            if isinstance(item,(int,float,Fraction)):return self.x<=item<=self.y
            elif isinstance(item,rangeac):return item.x>=self.x and item.y<=self.y
        else:
            if isinstance(item,(int,float,Fraction)):return self.x<item<self.y
            elif isinstance(item,rangeac):return item.x>self.x and item.y<self.y