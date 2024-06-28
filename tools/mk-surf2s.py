"""
Скрипт читает файлы N.txt где N=0..7 с координатами точек (x y в каждой строке).
и строит поверхность.
которую записывает в файл faces.txt
"""

import os

dir = "."
text_files = [f for f in os.listdir(dir) if f.endswith('.txt') and f.split(".")[0].isnumeric()]
N = len(text_files)
#N=16

norm = True

import numpy as np
np.bool = np.bool_
import pyvista as pv

coordinates = [] # координаты точек
line_segs = [] # номера индексов координат, в семантике PolyData lines
# см https://docs.pyvista.org/version/stable/api/core/_autosummary/pyvista.PolyData.html

# собираем поверхность
faces = []

prev_start = None
prev_final = None
start = None
final = None

for i in range(0,N):
    
    # Загрузка данных из файла
    fname = dir + "/" + str(i)+".txt"
    print("loading i=",i,"fname=",fname)
    with open(fname, "r") as file:
        lines = file.readlines()
        # Значение для координаты z
        z_value = i
        if norm:
           z_value = z_value / float(N)
        print("z=",z_value)

        # собираем поверхность
        prev_start = start
        prev_final = final

        start = len(coordinates)
        final = len(coordinates)+len(lines)
        if i == 0:
            l = [len(lines)] + list(range( len(coordinates), final ))
        else:
            l = [1+len(lines)] + list(range( len(coordinates), final )) + [len(coordinates)]    
        line_segs.extend(l)

        for line in lines:
            x, y = map(float, line.split())
            coordinates.append([x, y, z_value])

        # собираем поверхность
        if prev_start is not None:
            print("O(n^2) search",range(start,final-1),range(prev_start, prev_final))
            for k in range(prev_start, prev_final-1): # -1
                x1 = coordinates[k][0]
                y1 = coordinates[k][1]
                z1 = coordinates[k][2]
                x2 = coordinates[k+1][0]
                y2 = coordinates[k+1][1]
                z2 = coordinates[k+1][2]
                best_dist = 1000*1000
                best_j = -1
                for j in range(start,final-1):    
                    x3 = coordinates[j][0]
                    y3 = coordinates[j][1]
                    z3 = coordinates[j][2]
                    dist = (x3-x1)*(x3-x1) + (y3-y1)*(y3-y1)
                    if dist < best_dist:
                        best_j = j
                        best_dist = dist
                if best_j >= 0:
                    faces.append([k,k+1,best_j])
                    faces.append([k+1,best_j,best_j+1])

f = open("triangles.txt", "w")
for face in faces:
    a = coordinates[ face[0] ]
    b = coordinates[ face[1] ]
    c = coordinates[ face[2] ]
    f.write( f"{a[0]} {a[1]} {a[2]} {b[0]} {b[1]} {b[2]} {c[0]} {c[1]} {c[2]}\n" )
  #f.write( f"{face[0]} {face[1]} {face[2]}\n" )
f.close()
