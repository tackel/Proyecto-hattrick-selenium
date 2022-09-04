import sqlite3
import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(filename='logging_data_final.log', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d', level=logging.INFO)

path = Path(__file__).parent
path_sql = path.joinpath('sql')


con = sqlite3.connect('hattrick_db')
miCursor = con.cursor()

#df = pd.read_csv(f'{path_datos_finales}/lista_final-2022-08-29-20-21-13.csv')
#df.to_sql('players', con)
def create_table():
    """ Crea la tabla players_data_end mediante el archivo .sql """
    try:
        with open(f'{path_sql}/players_data_end.sql', 'r', encoding='utf-8') as table:
            data = table.read()
            miCursor.execute(data)
            con.commit()
            logging.info('Tabla en base de datos creada')
    except (EOFError, IOError) as e:
        logging.error(f'Error en la creacion de la tabla para la base de datos: {e}')

def read_data():
    """ Lee los datos de la bd para crear un dataFrame """
    try:
        with open(f'{path_sql}/read_data.sql', 'r', encoding='utf-8') as base:
            data = base.read()
            miCursor.execute(data)
            data_resp = miCursor.fetchall()
            print(data_resp)

    except (EOFError, IOError) as e:
        logging.error(f'Error al leer la base de datos: {e}')




if __name__ == '__main__':
    create_table()
    read_data()