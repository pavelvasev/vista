import os
import sys


import wave
import surf
import dirs

tablica = {}
tablica["wave"] = wave.load
tablica["triangles"] = surf.load
tablica["subdirs"] = dirs.load

def get_tablica():
	return tablica

# https://stackoverflow.com/questions/17142090/how-to-get-reference-to-module-by-string-name-and-call-its-method-by-string-name
# getattr(globals()[module_name], function_name)