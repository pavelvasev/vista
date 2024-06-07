import importlib

# вернуть список слоев
# слой это пара name, actor

import os
import sys
import util

# проходимся по подкаталогам и если в подкаталоге есть файл loader.py то это слой и мы его загружаем
def load(plotter):
  dir = os.path.dirname(__file__)
  return util.recursive_load( dir, plotter )
