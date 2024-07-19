"""
Поперечные поверхности
"""

import os

dir = "."
text_files = [f for f in os.listdir(dir) if f.endswith('.txt') and f.split(".")[0].isnumeric()]
N = len(text_files)
print("N=",N)
#N=16

norm = True

import numpy as np
np.bool = np.bool_
import pyvista as pv

surf = [] # координаты точек треугольников

for i in range(0,N):
    
    # Загрузка данных из файла
    fname = dir + "/" + str(i)+".txt"
    print("loading i=",i,"fname=",fname)
    with open(fname, "r") as file:
        lines = file.readlines()
        # Значение для координаты z
        z_value = i
        if norm:
           z_value = z_value / float(N-1)
        print("z=",z_value)

        coordinates = []
        for line in lines:
            x, y = map(float, line.split())
            coordinates.append([x, y, z_value])

        pt0 = coordinates[0]        
        for i in range( 1, len(coordinates)-1 ):
            surf.append( pt0 )
            surf.append( coordinates[i] )
            surf.append( coordinates[i+1] )

f = open("surf2.txt", "w")
for i in range(0,len(surf),3):
    a = surf[i]
    b = surf[i+1]
    c = surf[i+2]
    print(a,b,c)
    f.write( f"{a[0]} {a[1]} {a[2]} {b[0]} {b[1]} {b[2]} {c[0]} {c[1]} {c[2]}\n" )
  #f.write( f"{face[0]} {face[1]} {face[2]}\n" )
f.close()
