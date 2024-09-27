from playlist import *

comp = Composition('1', '1')
pl = PlayList('2')
pl.append(comp)
comp2 = Composition('2', '2')
pl.append(comp2)
pl.remove(comp)
for i in pl:
    print(i.data)