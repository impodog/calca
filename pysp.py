from calca.overall import*

_G=globals()

def browse(___var___:object)->'str|NoReturn':
    """Gets the name of a specific variant.\n
    Only browses surfaces in globals."""
    for k,v in _G.items():
        if v is ___var___:return k
    raise NameError("Value %s not existing in global surface."%(___var___))

def Get(_name:str)->'object|NoReturn':
    """Gets the object of a name.\n
    Only browses surfaces in globals."""
    try:return _G[_name]
    except KeyError:raise NameError("Name %s not existing in global surface."%(_name))
def Set(_name:str,_object:object,inside:dict=_G)->None:
    """Sets the name to an object.\n"""
    inside[_name]=_object
    
def objects(num:int)->"list[object,]":
    """Return new objects to the given number."""
    result=[]
    for i in range(num):result.append(object())
    return result
class DefaultsTo():
    "See analyze()"
    def __init__(self,o:object):self.o=o
    @property
    def value(self):return self.o
    def __repr__(self):return self.__str__()
    def __str__(self):return "%s(%s)"%(self.__class__.__name__,str(self.o))
class DefaultsTo_WithType(DefaultsTo):
    "See analyze()"
    def __init__(self,o:object,t:type):
        self.o=o;self.t=t
    def __repr__(self):return self.__str__()
    def __str__(self):return "%s(%s,%s)"%((self.__class__.__name__,)+tuple(map(str,(self.o,self.t))))
class SubType():
    "See analyze()"
    def __init__(self,itertype:type,subtype:"tuple[type]|type",dict_valuetype:"tuple[type]|type"=None,lower_limit:int=None,upper_limit:int=None):
        self.itertype=itertype;self.subtype=subtype;self.dict_valuetype=dict_valuetype;self.isdict=self.itertype is dict;self.tupled=istuple(self.subtype);self.length=len(self.subtype) if self.tupled else None;self.lower_limit=lower_limit;self.upper_limit=upper_limit
        if self.isdict:
            if iswidetype(self.subtype) and iswidetype(self.dict_valuetype):self.isdict=True
            else:raise TypeError("dict subtype must contain two proper types")
            if self.tupled:
                if not isinstance(self.dict_valuetype,tuple) or self.length != len(self.dict_valuetype):raise TypeError("tupled typecheck should have the same length of tuples")
    def issubtype(self,o:object):return self.subtype.check(o) if isinstance(self.subtype,SubType) else isinstance(o,self.subtype)
    def isvaluetype(self,o:object):return self.dict_valuetype.check(o) if isinstance(self.dict_valuetype,SubType) else isinstance(o,self.dict_valuetype)
    def check(self,o:Iterable):
        if isinstance(o,self.itertype):
            if not self.tupled:return all(map(self.issubtype,o)) and (all(map(self.isvaluetype,o.values())) if self.isdict else True) and (0 if self.lower_limit is None else self.lower_limit) <= len(o) <= (math.inf if self.upper_limit is None else self.upper_limit)
            else:
                if not self.isdict:
                    if self.length == len(o):
                        result=True
                        for i in range(self.length):
                            if not ana_isinstance(self.subtype[i],o[i]):result=False;break
                        return result
                else:
                    if self.length == len(o):
                        result=True
                        values=tuple(o.values())
                        keys=tuple(o.keys())
                        for i in range(self.length):
                            if not (ana_isinstance(self.subtype[i],keys[i]) and ana_isinstance(self.dict_valuetype[i],values[i])):result=False;break
                        return result
        return False
    def __call__(self,*args,**kwargs):return self.itertype(*args,**kwargs)
    def __repr__(self):return "%s(%s,%s,%s)"%((self.__class__.__name__,)+tuple(map(repr,(self.itertype,self.subtype,self.dict_valuetype))))
    def __str__(self):return self.__repr__()
ARGS,KWARGS,NOTDEFINED=objects(3)
ANY=object
class analyze_args():
    def __init__(self,argtype:type=ANY):self.argtype=argtype
    def check(self,o:object):return annocheck(self.argtype,o)
class analyze_kwargs():
    def __init__(self,valuetype:type=ANY):self.valuetype=valuetype
    def check(self,o:object):return annocheck(self.valuetype,o)
def typecheck(Each:'tuple[object]',Types:'tuple[type,]')->bool:
    for i in range(len(Each)):
        if type(Types)==tuple:CurType=Types[i]
        else:CurType=Types
        if not isinstance(Each[i],CurType):return False
    return True
class AnalyzingError(Exception):...
def annocheck(anno,arg:object):return (isinstance(anno,SubType) and anno.check(arg)) or (istype(anno) and isinstance(arg,anno)) or type(anno) == DefaultsTo or (isinstance(anno,DefaultsTo_WithType) and (ana_isinstance(anno.t,arg) or anno.o is arg))
def istype(o:object):return isinstance(o,type) or AnyType.check(o)
def iswidetype(o:object):return isinstance(o,(type,SubType)) or AnyType.check(o)
def istuple(o:object):return type(o) is tuple
def ana_isinstance(t,o:object):return t.check(o) if isinstance(t,SubType) else isinstance(o,t)
def is_akw(o:object):return isinstance(o,analyze_kwargs)
AnyType=SubType(tuple,type,lower_limit=1)
@overload
def analyze(input_args:tuple,input_kwargs:dict,rich_names:"dict")->dict:...
@overload
def analyze(input_args:tuple,input_kwargs:dict,names:"tuple")->dict:...
def analyze(input_args:tuple,input_kwargs:dict,given)->dict:
    """Analyze with * and ** operand and default settings. Put these object on items for special meanings:
    
ANY - Supports any type

analyze_args(argtype) - Starting an *args argument clause, with a variable type(defaults to ANY).

analyze_kwargs(valuetype) - Starting an **kwargs keyword clause, with a value type(defaults to ANY).

DefaultsTo(object) - If not given, defaults to the specific object.

AnyType(types) - Use as a normal type, matches if the argument is any type's instance.

SubType(itertype,subtype,dict_valuetype,lower_limit,upper_limit) - Matches an iterable with specified element type. Give dict_valuetype ONLY if itertype is dict. If given a tuple of types(with the same length), match as ordered has corresponding types.

If names is given, return only the name matching arguments.
If rich_names is given, analyze the advance arguments with type annotation,"""
    if not typecheck((input_args,input_kwargs),(tuple,dict)):raise TypeError("Wrong input on input_args and input_kwargs.")
    result=dict()
    if isinstance(given,tuple):
        Argable=True;ArgUsed=0
        for name in given:
            if input_kwargs.get(name)!=None:result[name]=input_kwargs.get(name);Argable=False
            elif Argable:result[name]=input_args[ArgUsed];ArgUsed+=1
            else:raise AnalyzingError("analyzed positional argument '%s' follows keyword argument"%name)
    elif isinstance(given,dict):
        rich_names:dict=given
        Names=tuple(rich_names.keys())
        Anno=tuple(rich_names.values())
        Now=0
        Mode=ANY
        Have=None
        #Initiallise result
        for ind in range(len(rich_names)):
            name=Names[ind];anno=Anno[ind]
            if isinstance(anno,DefaultsTo):result[name]=anno.value
            elif isinstance(anno,analyze_args):result[name]=list()
            elif isinstance(anno,analyze_kwargs):result[name]=dict()
            else:result[name]=anno
        #Analyze *args first
        for arg in input_args:
            try:
                anno=Anno[Now];name=Names[Now]
                if isinstance(anno,DefaultsTo_WithType):anno=anno.t
            except IndexError:
                raise AnalyzingError("Too many input arguments.")
            if isinstance(anno,analyze_args):
                if not isinstance(Mode,analyze_args):Mode=anno;Have=name
                elif name != Have:raise SyntaxError("Too many * arguments to have.")
            if Mode is ANY:
                if annocheck(anno,arg):
                    result[name]=arg
                    Now+=1
                else:
                    raise AnalyzingError("Wrong type annotation %s for argument '%s', %s given."%tuple(map(repr,(anno,name,arg))))
            else:
                if Mode.check(arg):result[name].append(arg)
                else:raise AnalyzingError("Wrong type annotation %s for * argument '%s', %s given."%tuple(map(repr,(Mode.argtype,name,arg))))
        #Then **kwargs
        any_kwargs=False;kwargs_option:analyze_kwargs=None;kwargs_index=None
        for i in range(len(Anno)):
            kw=Anno[i]
            if is_akw(kw):any_kwargs=True;kwargs_option=kw;kwargs_index=i;break
        for k,v in input_kwargs.items():
            try:anno=Anno[Names.index(k)]
            except ValueError:
                if not any_kwargs:raise AnalyzingError("Value not found with keyword '%s'."%k)
                else:Mode=kwargs_option;Target=Names[kwargs_index];Have=Target
            if is_akw(anno):
                if not is_akw(Mode):Mode=kwargs_option;Target=k;Have=k
                elif k != Have:raise SyntaxError("Too many ** keyword arguments to have.")
            if not is_akw(Mode):
                if annocheck(anno,v):
                    result[k]=v
                else:
                    raise AnalyzingError("Wrong type annotation %s for keyword argument '%s', %s given."%tuple(map(repr,(anno,k,v))))
            elif Target != k:
                if Mode.check(v):result[Target][k]=v
                else:raise AnalyzingError("Wrong type annotation %s for ** keyword argument '%s', %s given."%tuple(map(repr,(anno,k,v))))
        #Final check
        for k,v in result.items():
            if iswidetype(v) or v is NOTDEFINED:
                print(result)
                raise AnalyzingError("Required argument '%s' not filled."%k)
    else:
        raise ValueError("Non-existing way to analyze")
    return result
def overloaded(input_args:tuple,input_kwargs:dict,*overloading_rich_names:"dict")->dict:
    exceptions:"list[str]"=list()
    for rich_names in overloading_rich_names:
        try:
            return analyze(input_args,input_kwargs,rich_names)
        except AnalyzingError as e:exceptions.append(e)
    raise AnalyzingError("No matched overloading analysis.",exceptions)