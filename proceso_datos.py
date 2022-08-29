import pandas as pd
from pathlib import Path
import os
from datetime import datetime
from time import sleep


path = Path(__file__).parent
path_descargas = path.joinpath('dowload_files')
path_link = path.joinpath('links_transitorios')
path_datos_finales = path.joinpath('datos_finales')



def create_links_mas_ides():
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
        df_link_finales.to_csv(f"{path_link}\link{str(numero)}.csv")
        numero +=1


def data_mas_links():
    contador = 1
    for folder, subfolders, files in os.walk(path_descargas):
        for file in files:
            if file.endswith('.csv'):
                sleep(2)
                today = datetime.now()
                today = today.strftime("%Y-%m-%d-%H-%M-%S")
        
                datos_totales = pd.read_csv(f'{folder}/{file}')
                link = pd.read_csv(f'{path_link}/link{contador}.csv')

                datos_totales['link'] = link['link']
                datos_totales.to_csv(f'{path_datos_finales}/lista_final-{today}.csv')
                contador += 1
               
                

                #path = os.path.join(folder, file)
                #os.remove(path)

'''
if __name__ == '__main__':
    data_mas_links()
'''