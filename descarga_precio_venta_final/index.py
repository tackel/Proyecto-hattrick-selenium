import sqlite3
import pandas as pd
#from pathlib import Path
import logging
from time import sleep
from datetime import datetime
from os import path

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By

ruta_base = path.abspath(path.join(path.dirname(__file__), ".."))
path_descargas = path.abspath(path.join(ruta_base, 'descarga_precio_venta_final'))
path_sql = path.abspath(path.join(path_descargas, 'sql'))

logging.basicConfig(filename=f'{ruta_base}/logging_data_final.log', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

#path = Path(__file__).parent
#path_sql = path.joinpath('sql')

con = sqlite3.connect(f'{ruta_base}/hattrick_db')
miCursor = con.cursor()

chromeDriver = f'{path_descargas}/chromedriver.exe'

options = Options()
#options.headless = True
options.add_argument('--headless')

# en windows:
options.binary_location = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
# en Linux
#options.binary_location = r'/snap/brave/179/opt/brave.com/brave/brave-browser'

s = Service(chromeDriver)
driver = webdriver.Chrome(service=s, options=options)

#df = pd.read_csv(f'{path_datos_finales}/lista_final-2022-08-29-20-21-13.csv')
#df.to_sql('players', con)

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
        cont = 0
        for link in links:
            cont += 1
            try:
                #driver.get('https://www86.hattrick.org/es/Club/Players/Player.aspx?playerId=434653155')
                driver.get(link[1])
                #driver.maximize_window()
                sleep(4)
                transfer_folder = driver.find_element(By.ID, 'ctl00_ctl00_CPContent_CPMain_btnViewTransferHistory').click()
                sleep(1)
           
                precio = driver.find_element(By.XPATH, '//*[@id="ctl00_ctl00_CPContent_CPMain_updPlayerTabs"]/div/table/tbody/tr[1]/td[7]').text                                   
                                                        
                semana_hattrick = driver.find_element(By.XPATH, '//*[@id="ctl00_ctl00_CPContent_CPMain_updPlayerTabs"]/div/table/tbody/tr[1]/td[4]/span').text
                edad_dias = driver.find_element(By.XPATH, '//*[@id="ctl00_ctl00_CPContent_CPMain_updPlayerTabs"]/div/table/tbody/tr[1]/td[6]').text
                # try para obtener si esta lesionado por que varia el xpath
                try:
                    lesion = driver.find_element(By.XPATH, '//*[@id="mainBody"]/div[4]/table/tbody/tr[2]/td[2]/div').text  
                                                                                                                                                            
                    lesion = lesion.split(' ')
                    lesion = int(lesion[1])
                except:
                    lesion = 0
                    pass
                try:
                    lesion = driver.find_element(By.XPATH, '//*[@id="mainBody"]/div[4]/table/tbody/tr[3]/td[2]/div').text                                                                                                  
                    lesion = lesion.split(' ')
                    lesion = int(lesion[1])
                except:
                    lesion = 0
                    pass

                precio = precio.split('P')
                precio = int(precio[0].replace(' ', ''))
                semana_hattrick = semana_hattrick[1:-1]
                edad = int(edad_dias[0:2])
                dias = edad_dias.split('(')
                dias = int(dias[1].replace(')', ''))
                

                if (int(link[2]) == edad and (int(link[3]) == dias or int(link[3])+3 >= dias) or (int(link[2]) == edad+1 and edad <=3)):
                # significa que el jugador se vendio en esta oportunidad
                # Actualizar datso.
                    miCursor.execute(f"UPDATE players SET Precio_venta = '{precio}', Fecha_hat_venta = '{semana_hattrick}', Edad = '{edad}', Días = '{dias}', Lesiones = '{lesion}' WHERE link = '{str(link[1])}'")
                    con.commit()
                    print(f'{cont}-Jugador {link[0]} Precio: {precio}, edad: {edad} años, {dias} dias. ACTUALIZADO')
                    logging.info(f'{cont}- El precio de {link[0]} es {precio}, edad: {edad} años, {dias} dias. ACTUALIZADO')
                else:
                    precio = 0
                    miCursor.execute(f"UPDATE players SET Precio_venta = '{precio}' WHERE link = '{str(link[1])}'")
                    con.commit()
                    print(f'{cont}- Jugador {link[0]} no fue vendido. Precio: 0')
                    logging.info(f'{cont}- Jugador {link[0]} no fue vendido. Precio: 0')

                    
            except Exception as e:
                
                precio = 0
                miCursor.execute(f"UPDATE players SET Precio_venta = '{precio}' WHERE link = '{str(link[1])}'")
                con.commit()
                print(f'{cont}- El jugador {link[0]} nunca fue vendido o lo DESPIDIERON')
                logging.info(f'{cont}- El jugador {link[0]} nunca fue vendido o lo DESPIDIERON')
                pass
    except Exception as e:
        logging.error(f'Error al obtener el precio de venta y la semana {e} ')



if __name__ == '__main__':
    #create_table()
    hora_inicio = datetime.now()
    logging.info(f'Comienza la ejecucion del programa: {hora_inicio} \n')
    print(f'Comienza la ejecucion del programa: {hora_inicio} \n')
    obtener_precio_semana()
    driver.close()
    hora_fin = datetime.now()
    print(f'Fin de la ejecucion del programa: {hora_fin} \n')
    print(f'Tiempo total de ejecucion: {hora_fin - hora_inicio}')
    logging.info(f'Fin de la ejecucion del programa: {hora_fin} \n')
    logging.info(f'Tiempo total de ejecucion: {hora_fin - hora_inicio}')