# вернуть список слоев в формате [name, actor, name, actor ... ]

import os
import sys

mdir = os.path.dirname(__file__)
sys.path.insert(0,mdir)

def load(dir,name,suffix,plotter):
  result = []

  import wave  
  result = result + wave.load(dir,name,suffix,plotter)

  import surf
  result = result + surf.load(dir,name,suffix,plotter)

  import dirs
  result = result + dirs.load(dir,name,suffix,plotter)

  return result