import os
import pyvista as pv

K = 16

def load(plotter):
	coordinates = [] # координаты точек
	line_segs = [] # номера индексов координат, в семантике PolyData lines	
	dir = os.path.dirname(__file__) + "/"

	for i in range(0,K+1):	    
	    # Загрузка данных из файла
	    fname = dir+str(i)+".txt"
	    print("loading i=",i,"fname=",fname)
	    with open(fname, "r") as file:
	        lines = file.readlines()
	        z_value = i # / float(K-1)  # Значение для координаты z
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

	return actor
