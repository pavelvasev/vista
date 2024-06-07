import importlib

#import wave_16.load
#import wave_8.loader

# вернуть список слоев
# слой это пара name, actor

import os 
import sys

def load(plotter):
  dir = os.path.dirname(__file__)
  sys.path.append(dir)
  wave_8 = importlib.import_module('wave_8.loader')
  a = wave_8.load(plotter)

  wave_16 = importlib.import_module('wave_16.loader')
  b = wave_16.load(plotter)
  
  wave_16b = importlib.import_module('cos_16.loader')
  c = wave_16b.load(plotter)  

  #wave_8s = importlib.import_module('wave_8_surface.loader')
  #c = wave_8s.load(plotter)
  
  # ["wave_8_surface",c]
  return [ ["wave_8",a],["wave_16",b],["cos_16",c] ]