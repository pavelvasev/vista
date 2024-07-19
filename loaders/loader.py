# вернуть список слоев в формате [name, actor, name, actor ... ]

import os
import sys
import yaml

print('------------ init tablica')
tablica = {}

def set_tablica(t):
  print("sss",t)
  global tablica
  tablica = t

# не очень удобное щас
# мб https://stackoverflow.com/a/17142143
# или что-то такое

# еще был вариант что loader.load получает ссылку на таблицу
# но тогда как сделать dirs? явный.. он же лоадера вызывает
# да легко кстати - передавать явному dirs такую ссылку в этом случае
# ну ок есть варианты, щас какой-то 
# а еще можно было просто import loader изнутри dirs сказать метода..

def process_item( key, value, dir, plotter, parent_labels ):
  print("process_item key=",key)
  itype = value["type"]
  r = dict(value)
  del value["type"] # type ключевое слово
  global tablica
  #print("Tabliuca=",tablica)
  loader_fn = tablica[itype]
  result = loader_fn(dir=dir,itype=itype,iid=key,**value,plotter=plotter,parent_labels=parent_labels)
  #result["labels"] = parent_labels + result["labels"]
  return result

def load(dir,plotter,parent_labels):
  result = []
  descr = {}

  yf = os.path.join(dir,"vista.yaml")
  if os.path.isfile(yf):
    with open(yf) as stream:
        try:
            descr = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

  # неявное
  descr["subdirs"] = { "type":"subdirs" }

  for key, value in descr.items():
      result = result + process_item( key, value, dir, plotter, parent_labels )

  return result