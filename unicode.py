"""calca.unicode
---
Unicode and shift on keyboard
---

main function: shift

    >>> import calca.unicode
    >>> calca.unicode.shift('a',True)
    'A'
    >>> calca.unicode.shift('$',False)
    '4'
    >>> calca.unicode.shift(70,False)
    102

unicode can be used by built-in functions
    ord : get unicode of a single str
    chr : get a single str's unicode"""
from calca.overall import*

def unistr(string:str):return ''.join('{:04X}'.format(ord(chr)) for chr in string)

unicode=ord

LOWUP_CHR={'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D', 'e': 'E', 'f': 'F', 'g': 'G', 'h': 'H', 'i': 'I', 'j': 'J', 'k': 'K', 'l': 'L', 'm': 'M', 'n': 'N', 'o': 'O', 'p': 'P', 'q': 'Q', 'r': 'R', 's': 'S', 't': 'T', 'u': 'U', 'v': 'V', 'w': 'W', 'x': 'X', 'y': 'Y', 'z': 'Z','1':'!','2':'@','3':'#','4':'$','5':'%','6':'^','7':'&','8':'*','9':'(','0':')','-':'_','=':'+','[':'{',']':'}','\\':'|',';':':','\'':'"',',':'<','.':'>','/':'?','`':'~'}
LOWUP_UNICODE={97: 65, 98: 66, 99: 67, 100: 68, 101: 69, 102: 70, 103: 71, 104: 72, 105: 73, 106: 74, 107: 75, 108: 76, 109: 77, 110: 78, 111: 79, 112: 80, 113: 81, 114: 82, 115: 83, 116: 84, 117: 85, 118: 86, 119: 87, 120: 88, 121: 89, 122: 90, 49: 33, 50: 64, 51: 35, 52: 36, 53: 37, 54: 94, 55: 38, 56: 42, 57: 40, 48: 41, 45: 95, 61: 43, 91: 123, 93: 125, 92: 124, 59: 58, 39: 34, 44: 60, 46: 62, 47: 63, 96: 126}
UPLOW_CHR={'A': 'a', 'B': 'b', 'C': 'c', 'D': 'd', 'E': 'e', 'F': 'f', 'G': 'g', 'H': 'h', 'I': 'i', 'J': 'j', 'K': 'k', 'L': 'l', 'M': 'm', 'N': 'n', 'O': 'o', 'P': 'p', 'Q': 'q', 'R': 'r', 'S': 's', 'T': 't', 'U': 'u', 'V': 'v', 'W': 'w', 'X': 'x', 'Y': 'y', 'Z': 'z', '!': '1', '@': '2', '#': '3', '$': '4', '%': '5', '^': '6', '&': '7', '*': '8', '(': '9', ')': '0', '_': '-', '+': '=', '{': '[', '}': ']', '|': '\\', ':': ';', '"': "'", '<': ',', '>': '.', '?': '/', '~': '`'}
UPLOW_UNICODE={65: 97, 66: 98, 67: 99, 68: 100, 69: 101, 70: 102, 71: 103, 72: 104, 73: 105, 74: 106, 75: 107, 76: 108, 77: 109, 78: 110, 79: 111, 80: 112, 81: 113, 82: 114, 83: 115, 84: 116, 85: 117, 86: 118, 87: 119, 88: 120, 89: 121, 90: 122, 33: 49, 64: 50, 35: 51, 36: 52, 37: 53, 94: 54, 38: 55, 42: 56, 40: 57, 41: 48, 95: 45, 43: 61, 123: 91, 125: 93, 124: 92, 58: 59, 34: 39, 60: 44, 62: 46, 63: 47, 126: 96}  

def shift(ucode:'int|str',shiftup:bool)->'int|str':
    """Shift a unicode or str to upper case according to the keyboard."""
    ErrorMade=TypeError("Can only shift unicode(int) to int or str to str.")
    if shiftup:
        if isinstance(ucode,int):PASS=LOWUP_UNICODE
        elif isinstance(ucode,str):PASS=LOWUP_CHR
        else:raise ErrorMade
    else:
        if isinstance(ucode,int):PASS=UPLOW_UNICODE
        elif isinstance(ucode,str):PASS=UPLOW_CHR
        else:raise ErrorMade
    try:return PASS[ucode]
    except KeyError:return ucode

