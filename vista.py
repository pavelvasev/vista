#!/usr/bin/env python3
"""
Скрипт читает файлы wave_8/N.txt где N=0..7 с координатами точек (x y в каждой строке).
И рисует каждый файл как ломаную.
При этом соединяет последнюю и первую точку файла, кроме первого файла.
"""

# выставить movie = True и тогда будет запись мультика
movie = False

import numpy as np
np.bool = np.bool_
import pyvista as pv

#import os
#import sys
#dir = os.path.dirname(__file__)
#sys.path.append(dir)
#importlib.import_module("data")

# todo загружать из папки указанной в аргументе
#import data.loader
import loaders.loader

coordinates = [] # координаты точек
line_segs = [] # номера индексов координат, в семантике PolyData lines
# см https://docs.pyvista.org/version/stable/api/core/_autosummary/pyvista.PolyData.html
# то есть описание ломаной это есть
# кол-во вершин
# номера вершин
# и вот такие описания ломаных соединяются в один общий массив

# Создание окна для визуализации
plotter = pv.Plotter()

#layers = data.loader.load( plotter )
layers = loaders.loader.load( "data2","data","", plotter )

# Настройка видового окна
plotter.set_background('white')
#grid_actor = plotter.show_grid(ztitle="Z (iteration)" ) #, n_xlabels=9)

class MkGrid:
  def __init__(self,plotter):
    self.actor = None
    self.plotter=plotter

  def make(self,mesh=None):
    plotter.remove_actor(self.actor)
    # todo https://github.com/pyvista/pyvista/blob/6698923f73a1032bb3a42131d265b98b891e4836/pyvista/plotting/renderer.py#L1417
    self.actor = self.plotter.show_grid(mesh=mesh,ztitle="Z (iteration)" ) #, n_xlabels=9)  

gg = MkGrid(plotter)
gg.make()
  
# plotter.show(auto_close=False)

#    pass
#cb1 = plotter.add_checkbox_button_widget(toggle_vis, value=True, color_off='blue' )

class MAKEGUI:

  def __init__(self, plotter,sx=5,sy=20,dx=0,dy=55,color_off='grey'):
    self.plotter = plotter
    self.xx=sx
    self.yy=sy
    self.dx=dx
    self.dy=dy    
    self.color_off = color_off

  def addcb(self,text,cb,value):
    y = self.yy
    x = self.xx
    self.yy = self.yy + self.dy
    self.xx = self.xx + self.dx
    
    # color_off='blue',
    cb2    = plotter.add_checkbox_button_widget(cb, value, color_off=self.color_off,position=(x, y) ) #, color_on='red')
    actor2 = plotter.add_text(text,position=(x+57, y+7))
    return actor2

class SetVisibilityCallback:
    """Helper callback to keep a reference to the actor being modified."""

    def __init__(self, actor):
        self.actor = actor

    def __call__(self, state):
        self.actor.SetVisibility(state)
        gg.make( self.actor )

class SetVisibilityCallback2:
    """Helper callback to keep a reference to the actor being modified."""

    def __init__(self, actors, name):
        self.actors = actors
        self.name = name

    def __call__(self, state):
        for i in range(0,len(self.actors),2):
            if self.actors[i] == self.name:
                self.actors[i+1].SetVisibility(state)
                gg.make( self.actors[i+1] )

gui = MAKEGUI(plotter)

added = dict()
for i in range( 0,len(layers),2 ):
    name = layers[i]
    actor = layers[i+1]
    print(name)
    if not name in added:
        fn = SetVisibilityCallback2(layers,name)
        added[name] = True
        gui.addcb(name,fn,True)

"""
for layer in layers:
    name = layer[0]
    actor = layer[1]  
    #def toggle_vis(flag):
    #   actor.SetVisibility(flag)

    gui.addcb(name,SetVisibilityCallback(actor),True)
"""

######################33
class SetCameraCallback:
    """Helper callback to keep a reference to the actor being modified."""

    def __init__(self, pos):
        self.pos = pos

    def __call__(self, state):
        #self.actor.SetVisibility(state)
        plotter.camera_position = self.pos
        pass


gui2 = MAKEGUI(plotter,300,20,110,0,'blue')
#gui2.addcb("XY",SetCameraCallback(([1, 0, 0], [0, 0, 0], [0, 0, 1])),True)
#gui2.addcb("XZ",SetCameraCallback(([-1, 0, 0], [0, 0, 0], [0, 0, -1])),True)

def pos_xy(arg):
    plotter.camera_position = "xy"

gui2.addcb("xy",pos_xy,True)


# идея хочется нажать еще раз
def pos_xy1(arg):
    plotter.camera_position = "xy"
    plotter.camera.elevation = 15

gui2.addcb("xy'",pos_xy1,True)

def pos_xz(arg):
    plotter.camera_position = "xz"

gui2.addcb("xz",pos_xz,True)

def pos_xz1(arg):
    plotter.camera_position = "xz"
    plotter.camera.elevation = 15

gui2.addcb("xz'",pos_xz1,True)

def pos_zy(arg):
    plotter.camera_position = "zy"

gui2.addcb("zy",pos_zy,True)

def pos_zy11(arg):
    plotter.camera_position = "zy"
    plotter.camera.azimuth = 30

gui2.addcb("zy''",pos_zy11,True)

"""
def pos0(arg):
    plotter.camera_position = "xz"
    plotter.camera.azimuth = 45
    plotter.camera.elevation = 30
    plotter.camera.zoom(1.5)

gui2.addcb("p0",pos0,True)
"""

if not movie:
    plotter.show()
    #plotter.export_html('pv5.html')
    #plotter.export_obj('scene.obj')
else:
    print("writing movie!")
    p = plotter
    viewup = [0, 1, 0]
    #viewup = [0.5, 0.5, 1]
    #p.show(auto_close=False)
    path = p.generate_orbital_path(n_points=360, shift=1, viewup=viewup)
    p.open_movie("orbit.mp4")
    p.orbit_on_path(path, write_frames=True, viewup=viewup, step=0.02)
    #p.orbit_on_path(path, write_frames=True, viewup=viewup)
    p.close()
