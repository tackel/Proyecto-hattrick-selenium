from os import path

ruta_base = path.abspath(path.join(path.dirname(__file__)))
path_guardar_link = path.abspath(path.join(ruta_base, 'links_transitorios'))
print(path_guardar_link)
print(ruta_base)
