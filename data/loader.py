import importlib

# вернуть список слоев
# слой это пара name, actor

import os 
import sys

# проходимся по подкаталогам и если в подкаталоге есть файл loader.py то это слой и мы его загружаем
def load(plotter):
  dir = os.path.dirname(__file__)
  sys.path.append(dir)

  items = os.listdir(dir)
  dirs = []
  for x in items:
    p = os.path.join( dir, x )
    loader_path = os.path.join( dir, x, "loader.py" )
    if os.path.isfile( loader_path ):
      dirs.append( x )

  layers = []
  for p in dirs:
    print("loading",p)
    w = importlib.import_module(p+'.loader')
    a = w.load(plotter)
    layers.append( [p,a] )

  return layers
