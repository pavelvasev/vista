# загрузка из каталога wave

import os
import pyvista as pv

#print("Wwww")

def load(iid,itype,dir,N,plotter,parent_labels):
	print("Wave load ",dir,N)
	
	norm = True # todo параметр?

	coordinates = [] # координаты точек
	line_segs = [] # номера индексов координат, в семантике PolyData lines
	#dir = os.path.dirname(__file__) + "/"

    # нафиг всякие эвристики
	#text_files = [f for f in os.listdir(dir) if f.endswith('.txt') and f.split(".")[0].isnumeric()]
	#K = len(text_files)
	# не наше
	#if K == 0:
    #return []

	for i in range(0,N+1):
	    # Загрузка данных из файла
	    fname = dir+"/" + str(i)+".txt"
	    print("loading i=",i,"fname=",fname)
	    with open(fname, "r") as file:
	        lines = file.readlines()
	        if norm and (N > 1):
	            z_value = i / float(N)  # Значение для координаты z
	            
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

	return [ [iid] + parent_labels,actor]