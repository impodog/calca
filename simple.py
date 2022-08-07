from .overall import*
def root(base:Number,rootindex:Number)->Number:return base ** (1/rootindex)
def aripro1(start:Number,end:Number,shift:Number=1)->Number:end-=end%shift;num=(end-start)//shift+1;return (start+end)*num/2
def aripro2(start:Number,num:Number,shift:Number=1)->Number:end=shift*(num-1)+start;return (start+end)*num/2
def geopro1(start:Number,end:Number,shift:Number=2)->Number:num=int(math.log(end/start,shift));return (shift**num-1)/(shift-1)*start
def geopro2(start:Number,num:Number,shift:Number=2)->Number:return (shift**num-1)/(shift-1)*start
class georange():
    """A geometry(multiplying) sequence similar to range()

Either the end or the width is defined while initialising to limit the size. Otherwise, the size would be infinity.
An infinity-sized georange object returns -1 on len()"""
    @overload
    def __init__(self,start:Number=1,step:Number=2):...
    @overload
    def __init__(self,start:Number=1,step:Number=2,*,end:Number):...
    @overload
    def __init__(self,start:Number=1,step:Number=2,*,width:Number):...
    def __init__(self,start:Number=1,step:Number=2,**kwargs):
        self.start,self.step=start,step;self.cur=0
        if kwargs.get("end") is not None:self.end=kwargs["end"];self.width=math.ceil(math.log(self.end/self.start,self.step))
        elif kwargs.get("width") is not None:self.width=kwargs["width"];self.end=step**self.width*start
        else:self.end=self.width=math.inf
    def __iter__(self):return georange(self.start,self.step,width=self.width)
    def __next__(self):
        if self.cur < self.width:self.cur+=1;return self.start * self.step ** (self.cur-1)
        else:raise StopIteration
    def __getitem__(self,i:int):return self.step**i*self.start
    def __len__(self):return self.width if self.width != math.inf else -1
    def __str__(self):return f"georange(start={self.start}, step={self.step}, end={self.end}, width={self.width})"
    def __repr__(self):return str(self)