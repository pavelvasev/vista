#!/usr/bin/env python3.9
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

import os
import sys
#dir = os.path.dirname(__file__)
#sys.path.append(dir)
#importlib.import_module("data")

# todo загружать из папки указанной в аргументе
#import data.loader
mdir = os.path.dirname(__file__)
sys.path.insert(0,os.path.join(mdir,"loaders"))

import loader
import active
loader.set_tablica( active.get_tablica() )
# этот трюк нужен изза циклической зависимости loader -> dirs -> loader

# Создание окна для визуализации
plotter = pv.Plotter()

#layers = data.loader.load( plotter )
layers = loader.load( "data3",plotter,[] )

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

class SetVisibilityCallback3:
    """Helper callback to keep a reference to the actor being modified."""

    def __init__(self, actors, all_labels, label):
        self.actors = actors
        self.label = label
        self.all_labels = all_labels

    def __call__(self, state):
        # состояние метки
        self.all_labels[self.label] = state

        for i in range(0,len(self.actors),2):
            this_actor_labels = self.actors[i]
            visible = True
            for name in this_actor_labels:
                if not self.all_labels[name]:
                    visible = False
                    break
            self.actors[i+1].SetVisibility(visible)
        gg.make()

gui = MAKEGUI(plotter)

# список всех меток
# а заодно и видимостью будет
all_labels = dict()

for i in range( 0,len(layers),2 ):
    labels = layers[i]
    for name in labels:
        all_labels[name] = True

sorted_keys = list(all_labels.keys())
sorted_keys.sort(reverse = True)

for name in sorted_keys:
    fn = SetVisibilityCallback3(layers,all_labels,name)
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
