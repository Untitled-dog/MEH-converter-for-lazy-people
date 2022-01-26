global inp, out, holdd
import os, json, sys
import configparser
import time
modes=['jsontoini','initojson']

def ckw(append,dat,size=1000):#chunk writeing
    going=True
    while going==True:
        le=len(dat)
        print(le)
        if le >= size:
            append.write(dat[:size])
            dat=dat[size:]
        if le <  size:
            append.write(dat)
            going=False
def ckwi(append,dat,zone=0.7):#chunk writeing
    import timeit
    going=True
    size=100000
    while going==True:
        starttime = timeit.default_timer()
        le=len(dat)
        #print(le)
        if le >= size:
            append.write(dat[:size])
            dat=dat[size:]
        elif le <  size:
            append.write(dat)
            going=False
        tem=(timeit.default_timer() - starttime)
        size+=round(zone-tem)
        print(size)
        #if tem>zone: size-=1
        #if tem<zone: size+=1

def phm(fn):#makes a placeholder file
    open(fn,'w').write('foo')
class converror(Exception):
    pass#print("FOO")
argn=len(sys.argv)
if argn==1:
    print("no mode")
    print("usage: python converter.py <mode> <file> ")
    print("=====list of modes")
    for i in modes:
        print(i)
    sys.exit(1)
if argn==2:
    print('no file')
    print('usage: python converter.py <mode> <file> ')
    sys.exit(1)
mode=sys.argv[1]
fn=sys.argv[2]
end=''
hold=''
file=open(fn,'r').read()
print(fn)
print('working...')
if mode == 'jsontoini':
    global level, deff, dn
    level=[]
    out=configparser.ConfigParser()
    inp=json.loads(file)
    deff=False
    dn=0
    def setarea():
        try:
            out.add_section(iniroot)
        except:
            out.add_section(iniroot)
    def layer(level,area,dn):
        deff=False
        out.add_section(''.join(level))
        print('layer:'+''.join(level))
        for b in area:
            dn+=1
            if type(area[b])==dict:
                level.append('/'+str(b))
                dn=layer(level,area[b],dn)
            else:
                out.set(str(''.join(level)),str(b),str(area[b]))
        level.pop(-1)
        return dn
    
    for b in inp:
        dn+=1
        if type(inp[b])==dict:
            level.append(str(b))
            dn=layer(level,inp[b],dn)
        else:
            if deff==False:
                print('layer:DEFAULT')
                deff=True
            out.set('DEFAULT',str(b),str(inp[b]))
    print(f'{dn} stuff did')
    print('writeing')
    out.write(open(fn[:-4]+'ini','w'))
if mode == 'initojson':
    b=file.split('\n')
    fn=fn[:-3]+'json'
    out={}
    md=''
    hold=''
    def mklayer(dira):
        import sys
        print(dira.split('/'))
        sys.exit()
    for i in b:
        if i == '':continue
        elif i.startswith('[') and i.endswith(']'): 
            md=i[1:-1]
            print(f'key switch:{md}')
            if md=='DEFAULT':pass
            else:mklayer(md)#out[md]={}
            continue
        else:
            c=i.split(' = ',1)
            try:c[1]=int(c[1])
            except:pass
            if c[0] not in out:
                print(c[0])
                if md=="DEFAULT":out[c[0]]=c[1]
                else:out[md][c[0]]=c[1]
                
            #print(md)
    print('writeing')
    json.dump(out,open(fn,'w'),indent=2)




































