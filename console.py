"""
calca.console
---
Provides the terminal shortcuts and operations.
---
"""
import os,sys,time,re
from calca.overall import*
if(sys.platform == "win32"):
    import ctypes
    from ctypes import wintypes
else:
    import termios
stdout=sys.stdout;stdin=sys.stdin
cslength,cswidth=os.get_terminal_size()
PutLen=0
Mem=""
Solid=""
ForMem=""


class util:
    """Standard Utilities

Use print(util.) to call this."""
    reset = "\u001b[0m"
    bold = "\u001b[1m"
    underline = "\u001b[4m"
    reverse = "\u001b[7m"

    clear = "\u001b[2J"
    clearline = "\u001b[2K"

    up = "\u001b[1A"
    down = "\u001b[1B"
    right = "\u001b[1C"
    left = "\u001b[1D"

    nextline = "\u001b[1E"
    prevline = "\u001b[1F"

    top = "\u001b[0;0H"
    
    RESET='\033[0m'
    Return='\r'
    Next='\n'
    Back='\b'
    
    _ALL=(reset,bold,underline,reverse,clear,clearline,up,down,right,left,nextline,prevline,top,reset,Back)
    
ELIMINPUT=util.prevline+util.clearline
"""This default input eliminates the inputed line."""
RETURNS='\r\n'
"""The return inputs '\\r' and '\\n'"""


def jumpto(x, y):
    """Jump to a terminal position"""
    write("\033[%d;%dH" % (y, x))
def rgb(r:int, g:int, b:int, text:str=None):
    """Get a console R G B color."""
    return f"\u001b[38;2;{r};{g};{b}m" + ((text+util.RESET) if text is not None else "")
def write(*values,sep:str='',end:str=''):
    """Put a string into stdout. Same as 'print()'"""
    stdout.write(sep.join(values)+end)
    stdout.flush()
def writeslow(*values,wait:int=0.01,sep:str='',end:str=''):
    """Put a string slowly into stdout."""
    text=sep.join(values)
    for char in text:
        stdout.write(char)
        stdout.flush()
        time.sleep(wait)
    write(end)
def readipt(begin="",end:str=''):
    """Wait and read the input. Same as 'input()'"""
    text = ""
    write(begin)
    while True:
        char = stdin.read(1)
        if char == '\x03': raise KeyboardInterrupt
        elif char in ('\n','\r'): break
        else:text += char
    write(end)
    return text
def tercenter(string:str,fill:str):return string.center(cslength,fill)

class _Getch:
    """The getchar class. Use by instance 'getchar()'"""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self)->str: 
        INPUT=self.impl()
        INPUT=INPUT.decode() if isinstance(INPUT,bytes) else INPUT
        if INPUT == "\x03":raise KeyboardInterrupt
        return INPUT


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getchar = _Getch()
"""Gets the single char pressed. Does not require pressing RETURN."""
def backspace():write(util.left,' ',util.left)
def clearall():write(util.clear,util.top)
"""Clear the whole screen and go back to start point."""
def clearline():write(util.clearline);jumpto(0,getCursorPos()[1])
"""Clear the line and go back to the start of the line."""
def fdipt(endwith:'str|tuple'=RETURNS,limit:int=INFINITY,ctrl:'str|tuple'=None,each:str="",fill:str=None,show:bool=True,cgReturn:bool=True):
    """Find input. The ender input char will NOT be counted into result.
    WARNING: To get better result, ctrl is considered to help with wrong chars.

    endwith: End input when which letters are inputed. A long str or tuple of single strs.
    limit: Maximum input length(int). Defaults to infinity
    ctrl: Define what characters can be inputed, throw others. If None, there's no control. Defaults to None.
    each: What needed to be printed after every input
    fill: Not to show the string but an single text. Defaults to None.
    show: If it is False, each input will be hidden.
    cgReturn: To change \\r to \\n. Defaults to True"""
    text = ""
    while True:
        write(each)
        char = getchar()
        if cgReturn and char == '\r':char='\n'
        if char in endwith: break
        if (ctrl is None or char in ctrl) and len(text)<limit:
            text += char
            if show:write(char if fill is None else fill[0])
        if char == '\b' and len(text)>0:text=text[:-1];backspace()
    return text
def getcharwithin(s:str="yn",lower:bool=True):
    """Get a single char in c.
Lower: make the input in lower case."""
    while True:
        gc=getchar()
        if lower:gc=gc.lower()
        if gc in s:return gc
def getCursorPos()->'tuple[int,int]':
    if(sys.platform == "win32"):
        OldStdinMode = ctypes.wintypes.DWORD()
        OldStdoutMode = ctypes.wintypes.DWORD()
        kernel32 = ctypes.windll.kernel32
        kernel32.GetConsoleMode(kernel32.GetStdHandle(-10), ctypes.byref(OldStdinMode))
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 0)
        kernel32.GetConsoleMode(kernel32.GetStdHandle(-11), ctypes.byref(OldStdoutMode))
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    else:
        OldStdinMode = termios.tcgetattr(sys.stdin)
        _ = termios.tcgetattr(sys.stdin)
        _[3] = _[3] & ~(termios.ECHO | termios.ICANON)
        termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, _)
    try:
        _ = ""
        sys.stdout.write("\x1b[6n")
        sys.stdout.flush()
        while not (_ := _ + sys.stdin.read(1)).endswith('R'):
            True
        res = re.match(r".*\[(?P<y>\d*);(?P<x>\d*)R", _)
    finally:
        if(sys.platform == "win32"):
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), OldStdinMode)
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), OldStdoutMode)
        else:
            termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, OldStdinMode)
    if(res):
        return (int(res.group("x")), int(res.group("y")))
    return (-1, -1)