# загрузка из подкаталогов

import os
import sys

import loader

def load(dir,plotter, parent_labels, **kwargs):
  result = []

  items = os.listdir(dir)
  items.sort()
  dirs = []
  for x in items:
    # F-MODEL-FIRST
    dir_label = " "+x
    dir_labels = parent_labels + [dir_label]
    p = os.path.join( dir, x )
    if os.path.isdir( p ):
       result = result + loader.load( p,plotter,dir_labels )

  return result