from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from datetime import datetime
from time import sleep
from decouple import config
from pathlib import Path
import pandas as pd
import os
import logging
#from proceso_datos import create_links_mas_ides, data_mas_links




user = config('USER')
password = config('PASSWORD')

# variables para el buscador
#edad_minima = '27'
#edad_maxima = '40'
#habilidad_1 = 'Portería'
#hab_1_min = '11'
#hab_1_max = '16'

link_list = []
path = Path(__file__).parent
#path_descargas = path.joinpath('dowload_files')
#path_gurdar_link = path.joinpath('links_transitorios')

logging.basicConfig(filename='logging.log', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d', level=logging.INFO)

website = 'https://www.hattrick.org/es/'
chromeDriver = f'{path}\chromedriver.exe'
#option = webdriver.ChromeOptions()
#option.binary_location = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'


class Hattrick_proyect():
    def setup(self, path_descargas):
        try:
            options = Options()
            options.binary_location = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
            options.add_experimental_option("prefs", {
            "download.default_directory": str(path_descargas),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
            })
            s = Service(chromeDriver)
            self.driver = webdriver.Chrome(service=s, options=options)
            logging.info('Driver Generado')
        except Exception as e:
            logging.error(f'Fallo al generar el driver {e}')
# Login
    def login(self):
        """ loguea al usuario en la pagina con usuario y contraseña """
        try:
            self.driver.get(website)
            self.driver.maximize_window()
            sleep(5)
            user_texfield = self.driver.find_element(
                By.ID, 'ctl00_CPContent_ucLogin_txtUserName')
            password_texfield = self.driver.find_element(
                By.ID, 'ctl00_CPContent_ucLogin_txtPassword')
            #login_buton = driver.find_element(
            #    By.ID, 'ctl00_CPContent_ucLogin_butLogin')
            user_texfield.send_keys(user)
            #sleep(2)
            password_texfield.send_keys(password)
            #sleep(2)
            password_texfield.send_keys(Keys.ENTER)
            #login_buton.click()
            logging.info(f'Usuario logueado en: {website}')
        except Exception as e:
            logging.error(f'Fallo al loguearse: {e}')
        

# ir a transfer
    def tranfer(self, edad_minima, edad_maxima, habilidad_1, hab_1_min, hab_1_max, puja_maxima):
        """ 
        se dirige a la pagina de tranferencias para ingresar los parametros de busqueda, 
        para luego hacer clic en el boton de buscar 
        """
        try:
            sleep(10)
            transfer_buton = self.driver.find_element(
                By.XPATH, '//*[@id="shortcutsNoSupporter"]/div/a[4]')
            transfer_buton.click()
            sleep(5)

            # Seleccionar dropdowns
            dropdown_edad_min = Select(self.driver.find_element(
                By.ID, 'ctl00_ctl00_CPContent_CPMain_ddlAgeMin'))
            dropdown_edad_min.select_by_visible_text(edad_minima)

            dropdown_edad_max = Select(self.driver.find_element(By.ID, 'ctl00_ctl00_CPContent_CPMain_ddlAgeMax'))
            dropdown_edad_max.select_by_visible_text(edad_maxima)
            #sleep(2)

            drop_habilidad_1 = Select(self.driver.find_element(
                By.ID, 'ctl00_ctl00_CPContent_CPMain_ddlSkill1'))
            drop_habilidad_1.select_by_visible_text(habilidad_1)
            #sleep(2)
            drop_hab_min_1 = Select(self.driver.find_element(
                By.ID, 'ctl00_ctl00_CPContent_CPMain_ddlSkill1Min'))
            drop_hab_min_1.select_by_value(hab_1_min)
            #sleep(3)
            drop_hab_max_1 = Select(self.driver.find_element(
                By.ID, 'ctl00_ctl00_CPContent_CPMain_ddlSkill1Max'))
            drop_hab_max_1.select_by_value(hab_1_max)
            sleep(2)

            # borrar especialidad
            borrar_buton = self.driver.find_element(
                By.XPATH, '//*[@id="mainBody"]/table/tbody/tr[7]/td[2]/a[2]')
            borrar_buton.click()
            sleep(3)

            input_puja_maxima = self.driver.find_element(By.ID, 'ctl00_ctl00_CPContent_CPMain_txtBidMax')
            input_puja_maxima.clear()
            input_puja_maxima.send_keys(puja_maxima)
           

            # boton buscar
            buscar_buton = self.driver.find_element(
                By.ID, 'ctl00_ctl00_CPContent_CPMain_butSearch')
            buscar_buton.click()
            logging.info('Busqueda de jugadores en tranferencia hecha')
            sleep(6)
        except Exception as e:
            logging.error(f'Fallo al ingresar parametros de tranferencia: {e}')
        

    def borrar_archivos_antiguos(self, path):
        """ borra los archivos .csv antiguos antes de descargas los nuevos """
        for folder, subfolder, files in os.walk(path):
            if len(files) != 0:
                for file in files:
                    if file.endswith('csv'):
                        os.remove(f'{path}/{file}')
        logging.info('Archivos .csv antiguos borrados.')


    def dowload_file(self):
        """ descarga los csv del cuadro de descargas y los link de los jugadores """
        try:
            table_buton = self.driver.find_element(By.XPATH, '//*[@id="mainBody"]/a')
            table_buton.click()
            sleep(6)
            
            dowload_buton = self.driver.find_element(By.XPATH, '//*[@id="playersTable"]/div[2]/table/tfoot/tr/td/a')
            dowload_buton.click()
            sleep(3)

            link = self.driver.find_element(By.XPATH, '//*[@id="playersTable"]/div[2]/table/tbody/tr[1]/td[2]/a[@href]')
            link_list.append(link.get_attribute('href'))
            
            cerrar_buton = self.driver.find_element(By.ID, 'ctl00_ctl00_CPContent_CPMain_ucPlayersTable_imgCloseShop').click()
            
            sleep(4)
        except Exception as e:
            logging.error(f'Fallo al descargar lista de tranferencias: {e}')

    def paginar(self):
        """ Pagina las 4 paginas de jugadores en venta que puede haber para hacer la descarga """
        try:
            logging.info('Archivo csv en pagina 1 descargado')
            for i in range(1, 4):
                boton = self.driver.find_element(By.ID, f'ctl00_ctl00_CPContent_CPMain_ucPager_repPages_ctl0{i}_p{i}')
                boton.click()
                sleep(6)
                self.dowload_file()
                logging.info(f'Archivo csv en pagina {i+1} descargado')
        except Exception as e:
            logging.warning(f'La paginacin no llego a la pagina 4 de descargas. Error: {e} ')
            pass
    
    def create_df(self, path_gurdar_link):
        """
        Crea el .csv que contiene los links en crudo con los numeros id de los jugadores
        para luego poder procesarlos
        """
        try:
            df = pd.DataFrame()
            df['links'] = link_list
            df.to_csv(f"{path_gurdar_link}\link.csv", encoding='utf-8-sig')
            sleep(1)
            self.driver.close()
            logging.info('Archivo link.csv creado ')
        except Exception as e:
            logging.error(f'Error en la creacion del archivo link: {e} ')
        
        
