from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from time import sleep


# variables
user = 'chiruza'
password = ''
edad_minima = '22'
edad_maxima = '18'
habilidad_1 = 'Jugadas'
hab_1_min = '7'
hab_1_max = '11'

website = 'https://www.hattrick.org/es/'
chromeDriver = './chromedriver.exe'

s = Service(chromeDriver)
driver = webdriver.Chrome(service=s)
driver.get(website)
# driver.maximize_window()
sleep(5)


# Login
user_texfield = driver.find_element(
    By.ID, 'ctl00_CPContent_ucLogin_txtUserName')
password_texfield = driver.find_element(
    By.ID, 'ctl00_CPContent_ucLogin_txtPassword')
login_buton = driver.find_element(
    By.ID, 'ctl00_CPContent_ucLogin_butLogin')

user_texfield.send_keys(user)
sleep(2)
password_texfield.send_keys(password)
sleep(2)
login_buton.click()
sleep(10)

# ir a transfer
transfer_buton = driver.find_element(
    By.XPATH, '//*[@id="shortcutsNoSupporter"]/div/a[4]')
transfer_buton.click()
sleep(5)

# Seleccionar dropdowns
dropdown_edad_min = Select(driver.find_element(
    By.ID, 'ctl00_ctl00_CPContent_CPMain_ddlAgeMin'))
dropdown_edad_min.select_by_visible_text(edad_minima)
sleep(2)

drop_habilidad_1 = Select(driver.find_element(
    By.ID, 'ctl00_ctl00_CPContent_CPMain_ddlSkill1'))
drop_habilidad_1.select_by_visible_text(habilidad_1)
sleep(2)
drop_hab_min_1 = Select(driver.find_element(
    By.ID, 'ctl00_ctl00_CPContent_CPMain_ddlSkill1Min'))
drop_hab_min_1.select_by_value(hab_1_min)
sleep(3)
drop_hab_max_1 = Select(driver.find_element(
    By.ID, 'ctl00_ctl00_CPContent_CPMain_ddlSkill1Max'))
drop_hab_max_1.select_by_value(hab_1_max)
sleep(2)

# borrar especialidad
borrar_buton = driver.find_element(
    By.XPATH, '//*[@id="mainBody"]/table/tbody/tr[7]/td[2]/a[2]')
borrar_buton.click()
sleep(3)

# boton buscar
buscar_buton = driver.find_element(
    By.ID, 'ctl00_ctl00_CPContent_CPMain_butSearch')
buscar_buton.click()
sleep(4)
