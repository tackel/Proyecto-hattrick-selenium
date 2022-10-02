from dowload_data_selenium import Hattrick_proyect
from proceso_datos import create_links_mas_ides, data_mas_links
from load_data import create_table, load_data

import logging
from datetime import datetime
#from pathlib import Path
from os import path

ruta_base = path.abspath(path.join(path.dirname(__file__)))
path_descargas = path.abspath(path.join(ruta_base, 'dowload_files'))
path_guardar_link = path.abspath(path.join(ruta_base, 'links_transitorios'))
path_datos_finales = path.abspath(path.join(ruta_base, 'datos_finales' ))
path_sql = path.abspath(path.join(ruta_base, 'sql' ))

# configuracion del logging
# Formato del log: %Y-%m-%d - nombre_logger - mensaje
logging.basicConfig(filename=f'{ruta_base}/logging.log', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

# variables para el buscador
#edad_minima = '27'
#edad_maxima = '41'

habilidades_list = ['Jugadas', 'Defensa', 'Lateral', 'Portería', 'Anotación']
#habilidad_1 = 'Anotación'
hab_1_min = '12'
hab_1_max = '16'
puja_maxima = '0'

'''
path = Path(__file__).parent
path_descargas = path.joinpath('dowload_files')
path_guardar_link = path.joinpath('links_transitorios')
path_datos_finales = path.joinpath('datos_finales')
path_sql = path.joinpath('sql')
'''

if __name__ == '__main__':
    hora_inicio = datetime.now()
    logging.info(f'\n Comienza la ejecucion del programa en: {hora_inicio} ')
    for i in range(2):
        if i == 1:
            edad_minima = '27'
            edad_maxima = '41'
        if i == 0:
            edad_minima = '21'
            edad_maxima = '26'
        for habilidad_1 in habilidades_list:

            logging.info(f'\n - - - - Descargando: {habilidad_1} de {edad_minima} a {edad_maxima} años: {datetime.now()} ')
            hattrick = Hattrick_proyect()
            hattrick.setup(path_descargas)
            hattrick.login()
            hattrick.borrar_archivos_antiguos(path_descargas)
            hattrick.borrar_archivos_antiguos(path_guardar_link)
            hattrick.borrar_archivos_antiguos(path_datos_finales)
        
            hattrick.tranfer(edad_minima, edad_maxima, habilidad_1, hab_1_min, hab_1_max, puja_maxima)
            hattrick.dowload_file()
            hattrick.paginar()
            hattrick.create_df(path_guardar_link)
            create_links_mas_ides(path_guardar_link)
            data_mas_links(path_descargas, path_guardar_link, path_datos_finales)
            create_table(path_sql)
            load_data(path_datos_finales)
    
    hora_fin = datetime.now()
    logging.info(f'Fin de la ejecucion del programa: {hora_fin} ')
    logging.info(f'Tiempo total de ejecucion: {hora_fin - hora_inicio}\n')
