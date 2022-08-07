"""calca.screening
---
Calculate screen resolution
---

rs() use
---
    >>> import calca.screening
    >>> calca.screening.length=1000
    >>> calca.screening.width=500
    >>> calca.screening.EXP_LEN=500
    >>> calca.screening.EXP_WID=250
    >>> calca.screening.rs(400,calca.screening.LEN)
    ... #400/500*1000
    800"""
LEN=1;WID=2;BOTH=3
EXP_LEN=1356;EXP_WID=864
LENDE=(LEN,BOTH);WIDDE=(WID,BOTH)
length:int=0
width:int=0
def rs(_num:int,AffectTo:int=BOTH)->int:
    "Standard: 1356*864"
    if AffectTo in LENDE:_num=_num*length/EXP_LEN
    if AffectTo in WIDDE:_num=_num*width/EXP_WID
    return int(_num)