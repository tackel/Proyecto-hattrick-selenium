import pandas as pd
from pathlib import Path
import os
from datetime import datetime
from time import sleep
import logging


logging.basicConfig(filename='logging.log', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d',level=logging.INFO)

'''
# Path usados en el archivo
path = Path(__file__).parent
path_descargas = path.joinpath('dowload_files')
path_link = path.joinpath('links_transitorios')
path_datos_finales = path.joinpath('datos_finales')
'''


def create_links_mas_ides(path_link):
    """ Funcion que crea los links completos de cada jugador descargado con su id """
    try:
        numero = 1
        # lee los link descargados de la pagina
        df_links = pd.read_csv(f"{path_link}\link.csv")
        for i in df_links['links']:
            # divido la lista y queda en 3 partes
            lista_links = []
            cadena = i.split('=')
            for a in cadena:
                # divido la lista en elementos por , y obtengo los 25 id
                ides = a.split(',')
            for e in ides:
                # uno la primer parte de la url con el id de cada jugador y lo guardo en una lista
                link = cadena[0]+'='+e
                lista_links.append(link)  

            df_link_finales = pd.DataFrame({'link': lista_links})
            df_link_finales.to_csv(f"{path_link}/link{str(numero)}.csv", encoding='utf-8-sig' )
            numero +=1
        logging.info(f'Archivos csv con los link de jugadores creado')
    except Exception as e:
        logging.error(f'Error al crear los csv con los link de jugadores: {e}  ')
        



def data_mas_links(path_descargas, path_link, path_datos_finales ):
    """ 
    Funcion que une los datos de cada jugador con su link de acceso,
    guardando los datos completos en un archivo .csv
    """
    try:
        contador = 1
        for folder, subfolders, files in os.walk(path_descargas):
            for file in files:
                if file.endswith('.csv'):
                    sleep(2)
                    today = datetime.now()
                    today = today.strftime("%Y-%m-%d-%H-%M-%S")
                    try:
                        datos_totales = pd.read_csv(f'{folder}/{file}', sep=',', encoding='utf-8-sig')
                        link = pd.read_csv(f'{path_link}/link{contador}.csv', sep=',', encoding='utf-8-sig')

                        datos_totales['link'] = link['link']
                        datos_totales.to_csv(f'{path_datos_finales}/lista_final-{today}.csv',sep=',', encoding='utf-8-sig')
                    except Exception as e:
                        logging.error(f'Error al leer el csv descargado, algun dato erroneo {e}')
                        pass
                    contador += 1
        logging.info('Archivos lista_final creados')
    except Exception as e:
        logging.error(f'Error en la creacin del csv con los datos mas los links de cada jugador: {e}')

