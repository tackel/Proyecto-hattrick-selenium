import sqlite3
import pandas as pd
import os
from pathlib import Path
import logging

'''
path = Path(__file__).parent
path_datos_finales = path.joinpath('datos_finales')
path_sql = path.joinpath('sql')
'''
logging.basicConfig(filename='logging.log', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d',level=logging.INFO)

con = sqlite3.connect('hattrick_db')
miCursor = con.cursor()

#df = pd.read_csv(f'{path_datos_finales}/lista_final-2022-08-29-20-21-13.csv')
#df.to_sql('players', con)
def create_table(path_sql):
    """ Crea la tabla players mediante el archivo .sql """
    try:
        with open(f'{path_sql}/crear_tabla.sql', 'r', encoding='utf-8') as table:
            data = table.read()
            miCursor.execute(data)
            con.commit()
            logging.info('Tabla en base de datos creada')
    except (EOFError, IOError) as e:
        logging.error(f'Error en la creacion de la tabla para la base de datos: {e}')

        
def load_data(path_datos_finales):
    ''' Guarda los datos de los csv ya completos en la base de datos '''
    try:
        for folder, subfolder, files in os.walk(path_datos_finales):
            for file in files:
                df = pd.read_csv(f'{path_datos_finales}/{file}') 
                df.to_sql('players', con, if_exists='append', index=False )
                logging.info(f'Datos del archivo {file} guardados en la base de datos')
        con.close()
    except (EOFError, IOError) as e:
        logging.error(f'Error al guardar los datos la base de datos: {e}')