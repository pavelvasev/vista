"""
!!!!! good
Оболочка
- версия "зубчики" (пропускаем полигоны)
кстати она хороша..для 3д восприятия..  еще можно прпоускать большие треугольники

но
а) дыры
б) перепрыги

тут версия ленточной протяжки и интерполяции (индексов?). слава чатжпт + ручного тюнинга)

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

def loadN( N ):
    trajs = []
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

            if i == 0 or i == (N-1): # вырожденный случай - добавим вторую половинку идущую обратно
                kk = len(coordinates)
                for j in range(kk):
                    coordinates.append( coordinates[kk-j-1] )

            trajs.append( coordinates )
            print("points=",len(coordinates))

    return trajs


# возвращает набор координат треугольников
def connect2( line1, line2 ):
    tris = []
    print("O(n^2) search")
    for k in range(len(line1)-1):
        x1 = line1[k][0]
        y1 = line1[k][1]
        z1 = line1[k][2]
        x2 = line1[k+1][0]
        y2 = line1[k+1][1]
        z2 = line1[k+1][2]
        best_dist = 1000*1000
        best_j = -1
        for j in range(len(line2)):    
            x3 = line2[j][0]
            y3 = line2[j][1]
            z3 = line2[j][2]
            dist = (x3-x1)*(x3-x1) + (y3-y1)*(y3-y1)
            if dist < best_dist:
                best_j = j
                best_dist = dist
        if best_j >= 0:
            tris.extend( [ [x1,y1,z1], [x2,y2,z2], [x3,y3,z3]] )
            #tris.append( [ [x1,y1,z1], [x2,y2,z2], [x3,y3,z3]] )
            #faces.append([k,k+1,best_j])
            #faces.append([k+1,best_j,best_j+1])
    return tris

################################
def interpolate_points(points, num_points):
    """
    Интерполирует точки для получения заданного количества точек.
    """
    original_indices = np.linspace(0, len(points) - 1, num=len(points))
    interpolated_indices = np.linspace(0, len(points) - 1, num=num_points)
    
    interpolated_points = np.zeros((num_points, points.shape[1]))
    for dim in range(points.shape[1]):
        interpolated_points[:, dim] = np.interp(interpolated_indices, original_indices, points[:, dim])
    
    return interpolated_points    

def find_closest_point_index(point, points):
    """
    Находит индекс ближайшей точки в заданном наборе точек.
    """
    distances = np.linalg.norm(points - point, axis=1)
    return np.argmin(distances)

def reorder_points(points, start_index):
    """
    Переупорядочивает точки, начиная с заданного индекса, чтобы они оставались замкнутыми.
    """
    return np.concatenate((points[start_index:], points[:start_index]))    

def connect2gpt(line1, line2 ): 
    L1 = np.array( line1 )
    L2 = np.array( line2 )

    # Находим ближайшие точки
    start_idx_L1 = 0  # Начинаем с первой точки на L1
    start_idx_L2 = find_closest_point_index(L1[start_idx_L1], L2)

    # Переупорядочиваем точки L2, начиная с ближайшей точки
    L2_reordered = reorder_points(L2, start_idx_L2)

    # Выравниваем количество точек
    num_points = max(len(L1), len(L2))
    L1_interpolated = interpolate_points(L1, num_points)
    L2_interpolated = interpolate_points(L2_reordered, num_points)


    # Построение треугольников
    triangles = []
    for i in range(num_points):
        next_i = (i + 1) % num_points
        triangles.extend([L1_interpolated[i], L1_interpolated[next_i], L2_interpolated[i]])
        triangles.extend([L2_interpolated[i], L1_interpolated[next_i], L2_interpolated[next_i]])

    return triangles

################################    

lines = loadN( N )
print("loaded lines:",len(lines),N)
surf = []
for i in range(len(lines)-1):
    print("i=",i)
    tris = connect2gpt( lines[i], lines[i+1])
    #print("tris=",tris)
    surf = surf + tris

print("saving")

f = open("surf1.txt", "w")
for i in range(0,len(surf),3):
    a = surf[i]
    b = surf[i+1]
    c = surf[i+2]
    #print(a,b,c)
    f.write( f"{a[0]:.5} {a[1]:.5} {a[2]:.5} {b[0]:.5} {b[1]:.5} {b[2]:.5} {c[0]:.5} {c[1]:.5} {c[2]:.5}\n" )
  #f.write( f"{face[0]} {face[1]} {face[2]}\n" )
f.close()
