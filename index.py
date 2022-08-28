#from distutils.command.config import config
from os import link
from tkinter.tix import ListNoteBook
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from time import sleep
from decouple import config
from pathlib import Path
import pandas as pd


# variables
user = config('USER')
password = config('PASSWORD')

edad_minima = '22'
edad_maxima = '18'
habilidad_1 = 'Jugadas'
hab_1_min = '7'
hab_1_max = '11'

link_list = []
path = Path(__file__).parent
path_descargas = path.joinpath('files')
print(path)

website = 'https://www.hattrick.org/es/'
chromeDriver = 'C:/Users\Jamoncito del medio\Documents\programacion\selenium\Proyecto-hattrick-selenium\chromedriver.exe'
#option = webdriver.ChromeOptions()
#option.binary_location = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'

# con brave descomentar esto y poner option=options en el driver
'''
options = Options()
options.binary_location = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
options.add_experimental_option("prefs", {
  "download.default_directory": path_descargas,
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})
'''
class Hattrick_proyect():
    def setup(self):
        s = Service(chromeDriver)
        self.driver = webdriver.Chrome(service=s)
        
    


# Login
    def login(self):
        self.driver.get(website)
        #self.driver.maximize_window()
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
        

# ir a transfer
    def tranfer(self):
        sleep(10)
        transfer_buton = self.driver.find_element(
            By.XPATH, '//*[@id="shortcutsNoSupporter"]/div/a[4]')
        transfer_buton.click()
        sleep(5)

        # Seleccionar dropdowns
        dropdown_edad_min = Select(self.driver.find_element(
            By.ID, 'ctl00_ctl00_CPContent_CPMain_ddlAgeMin'))
        dropdown_edad_min.select_by_visible_text(edad_minima)
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

        # boton buscar
        buscar_buton = self.driver.find_element(
            By.ID, 'ctl00_ctl00_CPContent_CPMain_butSearch')
        buscar_buton.click()
        sleep(6)
    
    
    def dowload_file(self):
        table_buton = self.driver.find_element(By.XPATH, '//*[@id="mainBody"]/a')
        table_buton.click()
        sleep(4)
        
        dowload_buton = self.driver.find_element(By.XPATH, '//*[@id="playersTable"]/div[2]/table/tfoot/tr/td/a')
        dowload_buton.click()
        sleep(3)

        link = self.driver.find_element(By.XPATH, '//*[@id="playersTable"]/div[2]/table/tbody/tr[1]/td[2]/a').text
        link_list.append(str(link))
        
        cerrar_buton = self.driver.find_element(By.ID, 'ctl00_ctl00_CPContent_CPMain_ucPlayersTable_imgCloseShop').click()
        sleep(4)

    def paginar(self):
        for i in range(1, 4):
            boton = self.driver.find_element(By.ID, f'ctl00_ctl00_CPContent_CPMain_ucPager_repPages_ctl0{i}_p{i}')
            boton.click()
            sleep(6)
            hattrick.dowload_file()
    
    def create_df(self):
        df = pd.DataFrame()
        df['links'] = link_list
        

if __name__ == '__main__':
    hattrick = Hattrick_proyect()
    hattrick.setup()
    hattrick.login()
    hattrick.tranfer()
    hattrick.dowload_file()
    hattrick.paginar()
    hattrick.create_df()