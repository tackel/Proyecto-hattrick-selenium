from os import path
from time import sleep
import datetime
import os


from decouple import config

ruta_base = path.abspath(path.join(path.dirname(__file__)))
path_descargas = path.abspath(path.join(ruta_base, 'dowload_files'))
path_datos_finales = path.abspath(path.join(ruta_base, 'datos_finales' ))
path_guardar_link = path.abspath(path.join(ruta_base, 'links_transitorios'))

def data_mas_links(path_descargas, path_link ):
    """ 
    Funcion que une los datos de cada jugador con su link de acceso,
    guardando los datos completos en un archivo .csv
    """
    try:
        contador = 1
        for folder, subfolders, files in os.walk(path_descargas):
            for file in files:
                #print(f'{folder}/{file}')
                if file.endswith('.csv'):
                    try:
                        print(f'{folder}/{file}')
                        print(f'{path_link}/link{contador}')

                      
                    except Exception as e:
                   
                        pass
                    contador += 1
    
    except Exception as e:
        pass

data_mas_links(path_descargas, path_guardar_link)