import os
import pyvista as pv

def load(dir,file,itype,iid,plotter,parent_labels,color='blue',opacity=0.85,show_edges=False,edge_color='grey'):

	#dir = os.path.dirname(__file__) + "/"
	faces = []
	coords = []

	# Загрузка faces.txt
	fname = os.path.join(dir,file)
	with open(fname, "r") as file:
		lines = file.readlines()
		f = 0
		for line in lines:	           
			a1,a2,a3,b1,b2,b3,c1,c2,c3 = map(float, line.split())
			coords.append([a1,a2,a3])
			coords.append([b1,b2,b3])
			coords.append([c1,c2,c3])
			faces.append([f,f+1,f+2])
			f = f + 3

	#print("faces=",faces)

	tetra = pv.PolyData.from_regular_faces(coords, faces)
	actor = plotter.add_mesh(tetra,color=color,opacity=opacity,show_edges=show_edges,edge_color=edge_color)
	#,show_edges=True,edge_color='grey')
	# show_edges=True
	# ,style='wireframe'

	return [ [iid]+parent_labels,actor]
