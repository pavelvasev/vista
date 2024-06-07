import os
import pyvista as pv

def load(name,plotter,coordinates):

	dir = os.path.dirname(__file__) + "/"
	faces = []

	# Загрузка faces.txt
	fname = os.path.join(dir,"faces.txt")	    
	with open(fname, "r") as file:
		lines = file.readlines()
		for line in lines:	           
			f1,f2,f3 = map(int, line.split())
			faces.append([f1,f2,f3])

	#print("faces=",faces)

	tetra = pv.PolyData.from_regular_faces(coordinates, faces)
	actor = plotter.add_mesh(tetra,color='blue',opacity=0.85)

	return [name,actor]
