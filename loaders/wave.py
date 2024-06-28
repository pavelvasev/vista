# загрузка из каталога wave

import os
import pyvista as pv

#print("Wwww")

def load(dir,name,suffix,plotter):
	#name = os.path.basename(dir).split(".")[0]
	#datatypy = os.path.basename(dir).split(".")[1]
	if suffix != "wave":
		return []

	print("Wave load ",dir,"name=",name,"suffix=",suffix)
	
	norm = True

	coordinates = [] # координаты точек
	line_segs = [] # номера индексов координат, в семантике PolyData lines
	#dir = os.path.dirname(__file__) + "/"

	text_files = [f for f in os.listdir(dir) if f.endswith('.txt') and f.split(".")[0].isnumeric()]
	K = len(text_files)
	# не наше
	if K == 0:
		return []

	for i in range(0,K):
	    # Загрузка данных из файла
	    fname = dir+"/" + str(i)+".txt"
	    print("loading i=",i,"fname=",fname)
	    with open(fname, "r") as file:
	        lines = file.readlines()
	        if norm:
	            z_value = i / float(K-1)  # Значение для координаты z
	            
	        print("z=",z_value)

	        final = len(coordinates)+len(lines) # номер последней вершине в текущей набранной коллекции
	        if i == 0: # первый файл не замыкаем ломаную
	            l = [len(lines)] + list(range( len(coordinates), final ))
	        else:  # остальные файлы замкнутая ломанаю
	            l = [1+len(lines)] + list(range( len(coordinates), final )) + [len(coordinates)]    
	        line_segs.extend(l)

	        for line in lines:
	            x, y = map(float, line.split())
	            coordinates.append([x, y, z_value])	

	#print("line_segs=",line_segs)
	points = pv.PolyData(coordinates,lines=line_segs)
	actor = plotter.add_mesh(points,line_width=5, color='red')

	return [name,actor]