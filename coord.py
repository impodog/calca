from calca.overall import*
def Azimuth(Angle:Number)->Number:
    """Azimuth angle started with the x positive direction. -180 < A <= 180"""
    T=abs(Angle)%360
    if T>180:T=T-360
    return symbol(Angle)*T
def turns(Angle:Number)->Number:
    """Convert a azimuth angle to 360 turn angle. 0 <= A < 360"""
    A=Angle+180
    if A==360:A=0
    return A
def clockwise(Azi1:Number,Azi2:Number):
    """Give the clockwise azimuth subtraction"""
    t1,t2=turns(Azi1),turns(Azi2)
    return t2-t1+(360 if t1>t2 else 0)
def ccs(Azi1:Number,Azi2:Number):
    """Give the counter-clockwise azimuth subtraction"""
    t1,t2=turns(Azi1),turns(Azi2)
    return t1-t2+(360 if t2>t1 else 0)
def Acute(Angle:Number)->Number:return (180-abs(Angle))*symbol(Angle) if abs(Angle) > 90 else Angle
def Quadrant(Angle:Number)->'tuple':
    """Find the angle's quadrant: (1,1) -> First, (-1,1) -> Second, etc."""
    Angle=Azimuth(Angle)if Angle > 0 else Angle;return (-symbol(Azimuth(turns(Angle)-90)),-symbol(Angle))
def AinsideB(A:'Point|Linal',B:'Linal'):
    if type(A)==Point:return AinsideB(Segment.connect(B.start,A),B)
    elif almost(abs(A.Angle),abs(B.Angle)) or almost(abs(A.Angle + B.Angle), 90):
        xrange=rangeac(A.start.x,A.end.x)
        yrange=rangeac(A.start.y,A.end.y)
        ixrange=rangeac(B.start.x,B.end.x)
        iyrange=rangeac(B.start.y,B.end.y)
        return xrange in ixrange and yrange in iyrange
    return False
class Point():
    """A single point."""
    def __init__(self,Pos:'tuple|int|float',y:Number=None,Name="P"):
        if y is None:self.Pos=Pos
        else:self.Pos=(Pos,y)
        self.Name=Name
    def cover(self,P:'Point')->bool:return self.Pos==P.Pos
    def addx(self,L:Number):return Point((self.x+L,self.y))
    def addy(self,L:Number):return Point((self.x,self.y-L))
    def differ(self,P:'Point'):return self.x-P.x,self.y-P.y
    def dis(self,P:'Point'):return abs(self.x-P.x),abs(self.y-P.y)
    def distance(self,P:'Point'):return math.hypot(*(self.dis(P)))
    def move(self,x:Number=0,y:Number=0)->'Point':return Point((self.x+x,self.y+y))
    def symmetry(self,item:'Point|Line')->'Point':
        if type(item)==Point:return Point(item.x*2-self.x,item.y*2-self.y)
        elif type(item)==Line:
            ExSeg=self.shortest(item)
            return self.symmetry(ExSeg.end)
        else:raise TypeError("Can only make symmetry by Point or Line.")
    def shortest(self,Li:'Line')->'Segment':
        RPoint=Point(0,Li.add)
        CLine=Line(Segment.connect(self,RPoint))
        LineAngle=Acute(Li.intersectAngle(CLine))
        PolarAngle=Azimuth(Li.Angle-90-(180 if self.isunder(Li) else 0))
        Length=math.sin(math.radians(LineAngle))*CLine.Extend.Length
        return Segment.polar(self,PolarAngle,Length)
    def turn(self,around:'Point',Angle:Number)->'Point':
        Seg=Segment.connect(around,self)
        return Segment.polar(around,Azimuth(Seg.Angle+Angle),Seg.Length).end
    def isunder(self,Li:'Line')->bool:return Li.mul*self.x+Li.add>self.y
    def __add__(self,xy:'tuple[int,int]')->'Point':return Point((self.x+xy[0],self.y+xy[1]))
    def __lt__(self,P:'Point')->bool:return self.x < P.x and self.y < P.y
    def __gt__(self,P:'Point')->bool:return self.x > P.x and self.y > P.y
    def __repr__(self)->str:return "Point(%f, %f)"%(self.x,self.y)
    def __str__(self)->str:return "%s(%f, %f)"%(self.Name,self.x,self.y)
    def copy(self)->'Point':return Point(self.x,self.y)
    @property
    def x(self):return self.Pos[0]
    @property
    def y(self):return self.Pos[1]
class Segment():
    """Two ways to create a new segment: Segment.polar(); Segment.connect()"""
    def __init__(self,start:Point,end:Point,Angle:Number,Length:Number):
        self.start=start;self.end=end;self.Angle=Angle;self.Length=abs(Length)
        if self.start.x == self.end.x:self.end=Point(self.end.x+0.0000,self.end.y,self.end.Name)
    @classmethod
    def polar(cls,start:Point,Angle:Number,Length:Number)->'Segment':
        dx,dy=Quadrant(Angle)
        OriAngle=Angle
        Angle=Acute(Angle)
        try:XExtend=Length*math.cos(math.radians(abs(Angle)))*dx
        except:XExtend=Length*dx
        try:YExtend=Length*math.sin(math.radians(abs(Angle)))*dy
        except:YExtend=Length*dy
        return Segment(start,start.addx(XExtend).addy(YExtend),OriAngle,Length)
    @classmethod
    def connect(cls,start:Point,end:Point)->'Segment':
        dx,dy=start.differ(end)
        try:Angle=math.degrees(math.atan(dy/dx))
        except ZeroDivisionError:Angle=Azimuth(180*symbol(dy))
        Length=math.hypot(abs(dx),abs(dy))
        if dx<0 and dy<0:Angle+=180
        return Segment(start,end,Azimuth(Angle),Length)
    def goup(self)->'Segment':
        if self.start.y < self.end.y:return self.invert()
        return self
    def invert(self)->'Segment':return Segment(self.end,self.start,Azimuth(self.Angle-180),self.Length)
    def isinside(self,item:'Linal')->bool:return AinsideB(self,item)
    def isparallelto(self,item:'Linal')->bool:return self.Angle==item.Angle
    def iscollinear(self,item:'Linal')->bool:return self in Line(item)
    def extend(self,Length)->'Segment':return Segment.polar(self.end,self.Angle,Length)
    def move(self,x:Number=0,y:Number=0)->'Segment':return Segment.connect(self.start.move(x,y),self.end.move(x,y))
    def symmetry(self,item:'Point|Line')->'Segment':return Segment.connect(self.start.symmetry(item),self.end.symmetry(item))
    def turn(self,around:'Point',Angle:Number)->'Segment':return Segment.connect(self.start.turn(around,Angle),self.end.turn(around,Angle))
    def intersect(self,L:"Linal")->'Point|None':
        spoint=Line(self).intersect(Line(L.Extend))
        if spoint in self and spoint in L:return spoint
        else:return None
    def intersectAngle(self,L:"Linal")->'Point|None':
        sangle=Line(self).intersectAngle(Line(L.Extend))
        if self.intersect(L)!=None:return sangle
        else:return None
    @property
    def direction(self):return Quadrant(self.Angle)
    @property
    def Extend(self):return self
    def copy(self)->'Segment':return Segment(self.start,self.end,self.Angle,self.Length)
    def deepcopy(self)->'Segment':return Segment(self.start.copy(),self.end.copy(),self.Angle,self.Length)
    def movepoint(self,which:Point,x:Number=0,y:Number=0)->'Segment':
        if which is self.start:return Segment.connect(self.start.move(x,y),self.end)
        elif which is self.start:return Segment.connect(self.start,self.end.move(x,y))
    def __floordiv__(self,item:'Linal')->bool:return self.isparallelto(item)
    def __contains__(self,item:'Point|Segment')->bool:return AinsideB(item,self)
    def __float__(self):return self.Length
    def __int__(self):return int(self.Length)
    def __repr__(self)->str:return "Segment(start=%s, end=%s, Angle=%f, Length=%f)"%(self.start.__repr__(),self.end.__repr__(),self.Angle,self.Length)
    def __str__(self)->str:return "Segment %s <-> %s, Tilt %f, Length %f"%(str(self.start),str(self.end),self.Angle,self.Length)
class Ray():
    """Define a new ray extended by original segment."""
    def __init__(self,Extend:Segment):self.Extend=Extend.deepcopy().goup()
    def invert(self)->'Ray':return Ray(self.Extend.invert())
    def isinside(self,item:'Linal')->bool:return AinsideB(self,item)
    @property
    def Angle(self):return self.Extend.Angle
    @property
    def start(self):return self.Extend.start
    @property
    def end(self):return Point(INFINITY*self.direction[0],INFINITY*self.direction[1])
    @property
    def direction(self):return Quadrant(self.Angle)
    def isparallelto(self,item:'Linal')->bool:return self.Angle==item.Angle
    def move(self,x:Number=0,y:Number=0)->'Ray':return Ray(self.Extend.move(x,y))
    def symmetry(self,item:'Point|Line')->'Ray':return Ray(self.Extend.symmetry(item))
    def turn(self,around:'Point',Angle:Number)->'Ray':return Ray(self.Extend.turn(around,Angle))
    def copy(self)->'Ray':return Ray(self.Extend)
    def deepcopy(self)->'Ray':return Ray(self.Extend.deepcopy())
    def __contains__(self,item:'Point|Linal'):return AinsideB(item,self)
    def __floordiv__(self,item:'Linal')->bool:return self.isparallelto(item)
    def __repr__(self)->str:return "Ray(Extend="+self.Extend.__repr__()+")"
    def __str__(self)->str:return "Ray %s -> %s -> ..., Tilt %f While going %s"%(str(self.start),str(self.Extend.end),self.Angle,str(self.direction))
    
class Line():
    """Define a new line extended by original segment."""
    def __init__(self,Extend:Segment,mul:Number=None,add:Number=None):
        self.Extend=Extend.deepcopy().goup()
        if mul is not None:self.mul=mul,self.add=add
        else:
            s,e=self.Extend.start,self.Extend.end
            try:self.mul=(s.y-e.y)/(s.x-e.x)
            except:self.mul=0
            self.add=e.y-self.mul*e.x
    @classmethod
    def analytical(self,mul:Number,add:Number):return Line(Segment.connect(Point(0,add),Point(1,mul+add)),mul,add)
    def isinside(self,item:'Linal')->bool:return AinsideB(self,item)
    @property
    def Angle(self):return self.Extend.Angle
    @property
    def start(self):return Point(-INFINITY*self.direction[0],-INFINITY*self.direction[1])
    @property
    def end(self):return Point(INFINITY*self.direction[0],INFINITY*self.direction[1])
    @property
    def direction(self):return Quadrant(self.Angle)
    def isparallelto(self,item:'Linal')->bool:return self.Angle==item.Angle
    def move(self,x:Number=0,y:Number=0)->'Line':return Line(self.Extend.move(x,y))
    def symmetry(self,item:'Point|Line')->'Line':return Line(self.Extend.symmetry(item))
    def turn(self,around:'Point',Angle:Number)->'Line':return Line(self.Extend.turn(around,Angle))
    def intersect(self,Li:'Line')->"Point|INFINITY":
        try:x=(Li.add-self.add)/(self.mul-Li.mul)
        except:raise ValueError("Two lines covered each other.")
        y=self.mul*x+self.add
        return Point(x,y)
    def intersectAngle(self,Li:'Line')->Number:
        if self.Angle > Li.Angle:return 180-abs(self.Angle-Li.Angle)
        else:return abs(self.Extend.Angle-Li.Angle)
    def copy(self)->'Line':return Line(self.Extend)
    def deepcopy(self)->'Line':return Line(self.Extend.deepcopy())
    def mkx(self,x:Number)->'Point':return Point(x,x*self.mul*self.add)
    def __contains__(self,item:'Point|Linal'):return AinsideB(item,self)
    def __floordiv__(self,item:'Linal')->bool:return self.isparallelto(item)
    def __repr__(self)->str:return "Line(Extend="+self.Extend.__repr__()+" )"
    def __str__(self)->str:return "Line ... <-> %s <-> %s <-> ..., Tilt %f"%(str(self.start),str(self.Extend.end),self.Angle)
    
class Triangle():
    """Triangle shape. Can be drawed by SSS, SAS, ASA, AAS, HL, PPP, SP if possible.
    
    C should be the right angle in right triangles."""
    def __init__(self,SA:Segment,SB:Segment,SC:Segment,AA:Number,AB:Number,AC:Number,points:"tuple[Point]"):
        self.SA,self.SB,self.SC,self.AA,self.AB,self.AC,self.points=SA,SB,SC,AA,AB,AC,points
    @classmethod
    def PPP(cls,A:Point,B:Point,C:Point)->'Triangle':
        Xt=Triangle.SSS(Segment.connect(B,C),Segment.connect(A,C).Length,Segment.connect(A,B).Length)
        return Triangle(Segment.connect(B,C),Segment.connect(A,C),Segment.connect(A,B),Xt.AA,Xt.AB,Xt.AC,(A,B,C))
    @classmethod
    def SP(cls,S:Segment,P:Point)->'Triangle':return Triangle.PPP(S.start,S.end,P)
    @classmethod
    def SSS(cls,SA:Segment,LSB:Number,LSC:Number,clockwise:bool=True)->'Triangle':
        LSA=SA.Length;COUNT=1 if clockwise else -1
        try:
            AA=math.degrees(math.acos((LSB**2+LSC**2-LSA**2)/(2*LSB*LSC)))
            AB=math.degrees(math.acos((LSA**2+LSC**2-LSB**2)/(2*LSA*LSC)))
            AC=math.degrees(math.acos((LSA**2+LSB**2-LSC**2)/(2*LSA*LSB)))
        except ValueError:raise ValueError("Cannot make a triangle by the given side lengths.")
        SB=Segment.polar(SA.end,Azimuth(turns(SA.Angle)+COUNT*AC),LSB)
        SC=Segment.connect(SB.end,SA.start)
        return Triangle(SA,SB,SC,AA,AB,AC,(SA.start,SA.end,SB.end))
    @classmethod
    def SAS(cls,SA:Segment,AB:Number,LSC:Number,clockwise:bool=True)->'Triangle':
        h=LSC*math.sin(math.radians(AB))
        LSB=math.sqrt((LSC-math.sqrt(SA.Length**2-h**2))**2+h**2)
        return Triangle.SSS(SA,LSB,LSC,clockwise)
    @classmethod
    def AAS(cls,AB:Number,AA:Number,SA:Segment,clockwise:bool=True)->'Triangle':
        h=SA.Length*math.sin(math.radians(AB))
        P1=math.sqrt(SA.Length**2-h**2)
        P2=h/math.tan(math.radians(AA))
        return Triangle.SAS(SA,AB,P1+P2,clockwise)
    @classmethod
    def ASA(cls,AB:Number,SA:Segment,AC:Number,clockwise:bool=True)->'Triangle':return Triangle.AAS(AB,180-AB-AC,SA)
    @classmethod
    def HL(cls,LSC:Number,SA:Segment,clockwise=True)->'Triangle':
        try:return Triangle.SAS(SA,math.degrees(math.acos(SA.Length/LSC)),LSC)
        except ValueError:raise ValueError("Hypotenuse MUST be longer than legs.")
    def move(self,x:Number=0,y:Number=0)->'Triangle':return Triangle(self.SA.move(x,y),self.SB.move(x,y),self.SC.move(x,y),self.AA,self.AB,self.AC)
    def onanyside(self,item:'Point|Segment'):
        for i in (self.SA,self.SB,self.SC):
            if item in i:return True
        return False
    def inside(self,item:'Point'):
        Total=0
        Total+=Triangle.SP(self.SA,item).size+Triangle.SP(self.SB,item).size+Triangle.SP(self.SC,item).size
        return Total<=self.size
    def symmetry(self,item:'Point|Line')->"Triangle":
        return Triangle.PPP(self.points[0].symmetry(item),self.points[1].symmetry(item),self.points[2].symmetry(item))
    def insidal(self,item:'Segment'):return self.inside(item.start) and self.inside(item.end)
    def copy(self)->'Triangle':return Triangle(self.SA,self.SB,self.SC,self.AA,self.AB,self.AC)
    def deepcopy(self)->'Triangle':return Triangle(self.SA.deepcopy(),self.SB.deepcopy(),self.SC.deepcopy(),self.AA,self.AB,self.AC)
    def __contains__(self,item:'Point|Segment'):
        if type(item)==Point:return self.inside(item)
        elif type(item)==Segment:return self.insidal(item)
    @property
    def C(self):return self.SA.Length+self.SB.Length+self.SC.Length
    @property
    def size(self):p=self.C/2;return math.sqrt(p*(p-self.SA.Length)*(p-self.SB.Length)*(p-self.SC.Length))      
    def __repr__(self) -> str:return "Triangle(SA=%s,\nSB=%s,\nSC=%s,\nAA=%f,\nAB=%f,\nAC=%f)"%(self.SA.__repr__(),self.SB.__repr__()
,self.SC.__repr__(),self.AA,self.AB,self.AC)
    def __str__(self)->str:return "∆\nBC %s\nAC %s\nAB %s\n∠A=%f\n∠B=%f\n∠C=%f"%(str(self.SA),str(self.SB),str(self.SC),self.AA,self.AB,self.AC)
Linal=Union[Segment,Ray,Line]