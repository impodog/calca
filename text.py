"""calca.text
---
Text functions
---

The functions are pretty easy so you can read the docs."""
Alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
Uppercase=Alphabet[:26]
Lowercase=Alphabet[26:]
Symbol="`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/?"
Keyboard=Alphabet+Symbol
from calca.overall import*
def separate(string:str,each:int=1,throw:bool=False)->'list[str]':
    """Separates a string by a length. Leave the last characters a single value if not enough.
throw:bool --- to throw the last characters if not enough. Default: False"""
    result=list();string=str(string)
    if not isinstance(each,int) or each <= 0:raise ValueError("Cannot separate text by each "+str(each))
    try:
        while True:
            if len(string)==0:raise CalcaQuit
            if not throw or len(string)>=each:result.append(string[:each]);string=string[each:]
            else:raise CalcaQuit
    except CalcaQuit:...
    return result
def mltsplit(string:'str|list',*splitby:'str')->"list[str]":
    """Input a str or list of strs. Split the string by multiple strings.

    Example:
        >>> mltsplit("I like dogs because they are cute",' ','e','a')
        ['I', 'lik', '', 'dogs', 'b', 'c', 'us', '', 'th', 'y', '', 'r', '', 'cut', '']
        ... #The characters are removed after spliting.
        """
    if len(splitby)>0:
        if isinstance(string,str):
            return mltsplit(string.split(splitby[0]),*splitby[1:])
        else:
            result=list()
            for s in string:
                splitresult=mltsplit(s,*splitby)
                if isinstance(splitresult,str):result.append(splitresult)
                else:result+=splitresult
            return result
    else:return string
def mltsplit_stair(string:'str|list',*splitby:'str')->list:
    """Input a str or list of strs. Split the string by multiple strings. Creates dimensions to the splitbys.

    Example:
        >>> mltsplit_stair("I like dogs because they are cute",' ','e','a')
        ['I', 'lik', '', 'dogs', 'b', 'c', 'us', '', 'th', 'y', '', 'r', '', 'cut', '']
        ... #The characters are removed after spliting.
        """
    if len(splitby)>0:
        if isinstance(string,str):
            return mltsplit_stair(string.split(splitby[0]),*splitby[1:])
        else:
            result=list()
            for s in string:
                splitresult=mltsplit_stair(s,*splitby)
                result.append(splitresult)
            return result
    else:return string