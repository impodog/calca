"""
calca.numeries
---
Sqrt and number arrays
---

Calculating
---
    >>> import calca.numeries
    >>> calca.numeries.sqrt(8,4) # means '4(√8)'
    ... #All the sqrts will be simplified.
    8(√2)
    >>> calca.numeries.sqrt(8,2,True)
    ... #You can force it not to simplify by changing the last argument 'indicated'
    2(√8)
    
    
    >>> calca.numeries.sqrt(8,2) + 8
    ... #If it cannot be a single number, it will return a numery.
    8 + 4(√2)
    >>> calca.numeries.sqrt(8,2) + 8 + calca.numeries.sqrt(72,5)
    ... #Combine sames.
    8 + 60(√2)
    
    
    >>> A = (calca.numeries.sqrt(8,2) + 8 + calca.numeries.sqrt(72,5)).reciprocal()
    ... #Give reciprocal.
    >>> A
    -4/31 + 17/31(√2)
    >>> float(A)
    0.6465042116239553
    """
from calca.overall import*
class sqrt():
    """Square root of a number. But returns numery eventually.
    Indicated is for not to simplify the _squared number."""
    def __init__(self,_squared:int,_multi=1,indicated:bool=False):
        if _squared>=0:self._squared=_squared
        else:raise ValueError("Cannot give square root of number %d."%(_squared,))
        self._multi=Fraction(_multi)
        limit=int(math.sqrt(self._squared))+1
        if not indicated:
            for i in range(1,limit):
                if self._squared%(i**2) == 0:self._squared=self._squared//i**2;self._multi=self._multi*i
    def __str__(self):return "sqrt("+str(self.squared)+', '+str(self.multiply)+')'
    def __repr__(self):
        if self.multiply==1:return "(√"+str(self._squared)+')'
        else:return str(self.multiply)+"(√"+str(self.squared)+')'
    def __float__(self):return math.sqrt(self.squared)*self.multiply
    def __int__(self):return int(math.sqrt(self.squared)*self.multiply)
    def __add__(self,_n):
        if isinstance(_n,sqrt) and _n.squared==self.squared:return sqrt(self.squared,_n.multiply+self.multiply,indicated=True)
        else:return numery(self,_n)
    def __sub__(self,_n):
        if isinstance(_n,sqrt) and _n.squared==self.squared:return sqrt(self.squared,self.multiply-_n.multiply,indicated=True)
        else:return numery(self,-_n)
    def __mul__(self,_n):
        if isinstance(_n,sqrt):return sqrt(self.squared*_n.squared,self.multiply*_n.multiply)
        return sqrt(self._squared,self.multiply*_n)
    def __truediv__(self,_n):
        if isinstance(_n,sqrt):return sqrt(self.squared/_n.squared,self.multiply/_n.multiply)
        return sqrt(self.squared,self.multiply/_n)
    def __neg__(self):return sqrt(self.squared,-self.multiply,indicated=True)
    def reciprocal(self):return sqrt(self.squared,1/(self.squared*self.multiply))
    def __hash__(self):return hash(float(self))
    def __abs__(self):return sqrt(self.squared,abs(self.multiply))
    def __eq__(self,_n):return float(self)==_n
    def __gt__(self,_n):return float(self)>_n
    def __lt__(self,_n):return float(self)<_n
    def __le__(self,_n):return float(self)<=_n
    def __ge__(self,_n):return float(self)>=_n
    def __ne__(self,_n):return float(self)!=_n
    @property
    def rec(self):return self.reciprocal()
    @property
    def squared(self):return self._squared
    @property
    def multiply(self):return self._multi
class numery():
    """Creates an array of numbers which can save multiple types."""
    def __init__(self,*numbering):
        self.Rational:Fraction=Fraction(0,1);self.Sqrt:'list[sqrt]'=list();Existingsq=dict()
        for number in numbering:
            if isinstance(number,(Fraction,int,float)):self.Rational+=Fraction(number)
            elif isinstance(number,sqrt):self.Sqrt.append(number)
        for root in self.Sqrt:
            if root.squared not in Existingsq.keys():Existingsq[root.squared]=root.multiply
            else:Existingsq[root.squared]+=root.multiply
        del self.Sqrt;self.Sqrt=list()
        for s,m in Existingsq.items():self.Sqrt.append(sqrt(s,m))
    def __str__(self):
        result=""
        if self.Rational!=0:result+=self.Rational.__repr__()+", "
        for root in self.Sqrt:result+=str(root)+", "
        return "numery("+result[:-2]+")"
    def __repr__(self):
        result=""
        if self.Rational!=0:result+=self.Rational.__str__()+" + "
        for root in self.Sqrt:result+=root.__repr__()+" + "
        return result[:-3]
    def __float__(self):
        result=float(self.Rational)
        for root in self.Sqrt:result+=float(root)
        return result
    def __int__(self):
        return int(float(self))
    def __add__(self,number):
        """Returns a new numery made with an extra number."""
        if isinstance(number,numery):return numery(self.Rational,*self.Sqrt,*(number._pack))
        return numery(self.Rational,*self.Sqrt,number)
    def __sub__(self,number):
        """Returns a new numery made with an extra negative number."""
        if isinstance(number,numery):return numery(self.Rational,*self.Sqrt,*((-number)._pack))
        return numery(self.Rational,*self.Sqrt,-number)
    def __mul__(self,number):
        """Returns a new numery with multiplied arguments."""
        __allsqrts=[]
        for root in self.Sqrt:__allsqrts.append(root*number)
        return numery(self.Rational*number,*__allsqrts)
    def __truediv__(self,number):
        """Returns a new numery with divided arguments."""
        __allsqrts=[]
        for root in self.Sqrt:__allsqrts.append(root/number)
        return numery(self.Rational/number,*__allsqrts)
    def __neg__(self):
        """Returns a new numery with negative arguments."""
        __allsqrts=[]
        for root in self.Sqrt:__allsqrts.append(-root)
        return numery(-self.Rational,*__allsqrts)
    def __len__(self):
        """Gives then length that cannot be simplified."""
        return int(self.Rational!=0)+len(self.Sqrt)
    def __iter__(self):return [self.Rational]+self.Sqrt
    def __hash__(self):return hash(float(self))
    def __abs__(self):
        if float(self)<0:return -self
        else:return self
    def __eq__(self,_n):return float(self)==_n
    def __gt__(self,_n):return float(self)>_n
    def __lt__(self,_n):return float(self)<_n
    def __le__(self,_n):return float(self)<=_n
    def __ge__(self,_n):return float(self)>=_n
    def __ne__(self,_n):return float(self)!=_n
    def reciprocal(self):
        """Gives reciprocal of the numery(if possible).\n
        Cannot give reciprocal if you have items more than 1.
        If you did, raise ValueError."""
        if len(self.Sqrt)>1 and self.Rational != 0 or len(self.Sqrt)>2:raise ValueError("Cannot give reciprocal if you have items more than 1. %d Existing."%(len(self.Sqrt)+1,))
        if self.Rational != 0:
            rootnum=self.Sqrt[0]
            DEMOL=Fraction(self.Rational**2)-Fraction(rootnum.squared)
            UP=abs(-rootnum+self.Rational)
            return UP/DEMOL
        else:
            rootnum1,rootnum2=self.Sqrt[0],self.Sqrt[1]
            DEMOL=rootnum1.squared-rootnum2.squared
            return numery(rootnum1/DEMOL,-rootnum2/DEMOL)
    @property
    def _pack(self):return tuple(self.Sqrt+[self.Rational,])
    @property
    def rec(self):return self.reciprocal()