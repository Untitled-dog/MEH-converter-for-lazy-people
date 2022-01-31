global inp, out, holdd, modes
import os, json, sys
import configparser
import time
modes=['jsontoini','initojson']
class converror(Exception):
  pass
argn=len(sys.argv)
if argn==1:
  print('''no mode input
usage: python converter.py <mode> <file>
=====list of modes''')
  for i in modes:print(i)
  sys.exit(1)
if argn==2:
  print('''no file input
usage: python converter.py <mode> <file>''')
  sys.exit(1)
mode=sys.argv[1]
fn=sys.argv[2]
end=''
hold=''
file=open(fn,'r').read()
def note(text):
  print(text)

note('working...')
if mode == 'jsontoini':
  global level, deff, dn
  level=[]
  out=configparser.ConfigParser()
  inp=json.loads(file)
  dn=0
  def layer(level,area,dn):
    out.add_section(''.join(level))
    note('layer:'+''.join(level))
    for b in area:
      dn+=1
      if type(area[b])==dict:
        level.append('/'+str(b))
        dn=layer(level,area[b],dn)
      else:out.set(str(''.join(level)),b,str(area[b]))
    level.pop(-1)
    return dn
  note('layer:DEFAULT')
  for b in inp:
    dn+=1
    if type(inp[b])==dict:
      level.append(str(b))
      dn=layer(level,inp[b],dn)
    else:out.set('DEFAULT',str(b),str(inp[b]))
  
  note(f'''{dn} stuff did
writeing...''')
  out.write(open(fn[:-4]+'ini','w'))
if mode == 'initojson':
  global md
  inp=configparser.ConfigParser()
  inp.read(fn)
  out={};md=''
  def addto(md,val,run="out"):
    for i in md.split('/'):run+=f"['{i}']"
    if type(val)==str:run+=f" = '{val}'"
    elif type(val)==dict:run+=" = {}"
    else:run+=f" = {val}"
    exec(run,globals(),locals())
  for i in file.split('\n'):
    if i=='' or i.startswith("#"):continue
    elif i.startswith('[') and i.endswith(']'): 
      md=i[1:-1]
      if md=='DEFAULT':pass
      else:addto(md,{})
      note(f'key switch:{md}')
      continue
    else:
      c=i.split('=',1)
      try:c[1]=int(c[1])
      except:pass
      addto(md+'/'+c[0],c[1])
      continue
  note('writeing...')
  json.dump(out,open(fn[:-3]+'json','w'),indent=2)



































