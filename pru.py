import sqlite3
import pandas as pd
from pathlib import Path
import logging
from time import sleep


from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By

path = Path(__file__).parent
path_sql = path.joinpath('sql')
chromeDriver = f'{path}\chromedriver.exe'

options = Options()
options.binary_location = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
s = Service(chromeDriver)
driver = webdriver.Chrome(service=s, options=options)

def obtener_precio_semana():
    try:
        links = ['https://www86.hattrick.org/es/Club/Players/Player.aspx?playerId=444839553',]
        for link in links:
            try:
                driver.get(link)
                #driver.maximize_window()
                sleep(4)
                transfer_folder = driver.find_element(By.ID, 'ctl00_ctl00_CPContent_CPMain_btnViewTransferHistory').click()
                sleep(3)

                lesion = driver.find_element(By.XPATH, '//*[@id="mainBody"]/div[4]/table/tbody/tr[2]/td[2]/div').text
                #lesion = lesion.split(' ')
                
                #lesion = int(lesion[1])
                print(lesion)
           
               
            # Actualizar datso.
                #miCursor.execute(f"UPDATE players SET Precio_venta = '{precio}', Fecha_hat_venta = '{semana_hattrick}' WHERE link = '{str(link[1])}'")
                #con.commit()
                #print(f'El precio del jugador {link[0]} es {precio} y se actualizo ')
                #logging.info(f'El precio del jugador {link[0]} fue actualizado')
            except Exception as e:
                print(e)
                #precio = 0
                #miCursor.execute(f"UPDATE players SET Precio_venta = '{precio}' WHERE link = '{str(link[1])}'")
                #con.commit()
                #logging.error(f'El jugador {link[0]} nunca fue vendido o fue visto en los palcos, con cara de aburrimiento')
                pass
    except Exception as e:
        logging.error(f'Error al obtener el precio de venta y la semana {e} ')



if __name__ == '__main__':
    #create_table()
    obtener_precio_semana()

