import sqlite3
import pandas as pd
from pathlib import Path
import logging
from time import sleep


from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By



logging.basicConfig(filename='logging_data_final.log', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d', level=logging.INFO)

path = Path(__file__).parent
path_sql = path.joinpath('sql')


con = sqlite3.connect('hattrick_db')
miCursor = con.cursor()

chromeDriver = f'{path}\chromedriver.exe'

options = Options()
options.binary_location = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
s = Service(chromeDriver)
driver = webdriver.Chrome(service=s, options=options)

#df = pd.read_csv(f'{path_datos_finales}/lista_final-2022-08-29-20-21-13.csv')
#df.to_sql('players', con)
'''
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
'''
def read_data():
    """ Lee los datos de la tabla players y retorna los link  """
    try:
        # Ajustar en archivo read_data.sql el limit de link a buscar
        with open(f'{path_sql}/read_data.sql', 'r', encoding='utf-8') as base:
            data = base.read()
            miCursor.execute(data)
            data_resp = miCursor.fetchall()
            logging.info('Datos de la BD obtenidos correctamente.')
            
            return data_resp

    except Exception as e:
        logging.error(f'Error al leer la base de datos: {e}')


def obtener_precio_semana():
    try:
        links = read_data()
        for link in links:
            try:
                driver.get(link[1])
                #driver.maximize_window()
                sleep(4)
                transfer_folder = driver.find_element(By.ID, 'ctl00_ctl00_CPContent_CPMain_btnViewTransferHistory').click()
                sleep(3)
           
                precio = driver.find_element(By.XPATH, '//*[@id="ctl00_ctl00_CPContent_CPMain_updPlayerTabs"]/div/table/tbody/tr[1]/td[7]').text                                   
                semana_hattrick = driver.find_element(By.XPATH, '//*[@id="ctl00_ctl00_CPContent_CPMain_updPlayerTabs"]/div/table/tbody/tr[1]/td[4]/span').text
                precio = precio.split('P')
                precio = int(precio[0].replace(' ', ''))
                semana_hattrick = semana_hattrick[1:-1]
               
            # Actualizar datso.
                miCursor.execute(f"UPDATE players SET Precio_venta = '{precio}', Fecha_hat_venta = '{semana_hattrick}' WHERE link = '{str(link[1])}'")
                con.commit()
                print(f'El precio del jugador {link[0]} es {precio} y se actualizo ')
                logging.info(f'El precio del jugador {link[0]} fue actualizado')
            except Exception as e:
                logging.error(f'El jugador {link[0]} nunca fue vendido o hay otro error: {e} ')
                pass
    except Exception as e:
        logging.error(f'Error al obtener el precio de venta y la semana {e} ')



if __name__ == '__main__':
    #create_table()
    obtener_precio_semana()