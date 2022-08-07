"""
calca.factoring
---
Find prime numbers and give factors
---

This is easy to understand so there'd be only some explanations

    >>> import calca.factoring
    >>> calca.factoring.get_prime(100)
    True
    ... #It saves into 'primes'. True means it did generated some extra numbers.
    >>> calca.factoring.primes
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    >>> calca.factoring.get_prime(10)
    False
    ... #The generate is re-used so no numbers is generated.
  
     
Two ways of get if the number is prime:

    >>> calca.factoring.isprime_div(6701)
    True
    >>> calca.factoring.isprime_browse(6701)
    True

Of course, we expect that 'div' method works much quicker than the other.


Get factors:

    >>> calca.factoring.pfactors(90)
    [2, 45, 3, 30, 5, 18]

The two factors are always in pairs.

"""
from calca.overall import*
primes=[2]
highest=3
def step()->None:
    """Step through a prime generate."""
    global highest,primes
    add=True
    n=highest+2
    curlim=math.sqrt(n)
    for p in primes:
        if n%p == 0:add=False;break
        if p > curlim:break
    if add:primes.append(n)
    highest=n
def get_prime(limit:int)->bool:
    """Gets prime numbers to the limit.
    Return if the limit is not re-used."""
    global highest,primes
    if limit <=highest:return False
    for n in range(highest,limit+1,2):
        add=True
        curlim=math.sqrt(n)
        for p in primes:
            if n%p == 0:add=False;break
            if p > curlim:break
        if add:primes.append(n)
    highest=limit
    return True
def isprime_browse(_n:int)->bool:
    """Browse all the prime numbers to see if the number is in it."""
    get_prime(_n/2);return _n in primes
def isprime_div(_n:int)->bool:
    """Generate the prime to the sqrt and return if it is prime number."""
    lim=int(math.sqrt(_n))+1;get_prime(lim)
    for p in primes:
        if _n%p == 0:return False
        elif p > lim:break
    return True
def pfactors(_n:int)->'list[int]':
    """Gets all the prime factors by getting all prime numbers."""
    get_prime(_n//2)
    result=[]
    for p in primes:
        if _n%p == 0:result.append(p);result.append(_n//p)
    return result