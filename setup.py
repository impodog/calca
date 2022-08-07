import os,sys,warnings
FILENAME="calca"
everything=['console.py', 'coord.py', 'factoring.py', 'notinitial.py', 'numeries.py', 'overall.py', 'point.py', 'pysp.py', 'run.py', 'screening.py', 'sets.py', 'simple.py', 'sort.py', 'support.py', 'text.py', 'unicode.py', '__init__.py']
FILENUMBER=len(everything)
python_path=sys.exec_prefix
install_path=python_path+"\\Lib\\%s\\"%FILENAME
if not os.path.isdir(install_path):os.mkdir(install_path)
pathlist=list()
now=1
for path in os.listdir("./"):
    if path.endswith(".py") and path.find("setup") == -1:
        try:
            everything.remove(path)
            pathlist.append(path)
            print("File found: %s    %d/%d"%(path,now,FILENUMBER))
            now+=1
        except:
            warnings.warn("Found extra python file '%s' under directory."%path,Warning)
now=1;end=len(pathlist)
if len(everything)!=0:
    raise FileNotFoundError(
        "%d file(s): \n    %s\nare missing"%(len(everything),"\n    ".join(everything))
    )
for path in pathlist:
    print("Installing file %s... %d/%d"%(path,now,end))
    with open(path,"r",encoding="UTF-8") as file:
        content=file.read()
    with open(install_path+path.split("\\")[-1],'w',encoding="UTF-8") as target:
        target.write(content)
    now+=1
print("Successfully installed %s main part."%FILENAME)
#print("Using pip to check requirements...")
#subprocess.call((sys.executable,'-m','pip','install','-r','requirements.txt'))
print("No requirements needed.")
print("%s installation complete!"%FILENAME)