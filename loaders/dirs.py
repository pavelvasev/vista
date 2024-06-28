# загрузка из подкаталогов

import os
import sys

import loader

def load(dir,name,suffix,plotter):
  result = []

  items = os.listdir(dir)
  dirs = []
  for x in items:
    p = os.path.join( dir, x )    
    if os.path.isdir( p ):
      parts = x.split(".")
      cname = parts[0]
      print("PARTS=",parts)
      suffix = parts[1] if len(parts) > 1 else ""

      result = result + loader.load( p,name + "/" + cname,suffix,plotter )

  return result