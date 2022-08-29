import pandas as pd
from pathlib import Path


path = Path(__file__).parent
path_descargas = path.joinpath('files')
path_link = path.joinpath('links')


numero = 1
df_links = pd.read_csv(f"{path_link}\link.csv")
for i in df_links['links']:
    lista_links = []

    cadena = i.split('=')
    for a in cadena:
        ides = a.split(',')
    for e in ides:
        link = cadena[0]+'='+e
        lista_links.append(link)  

    df_link_finales = pd.DataFrame({'link': lista_links})
    df_link_finales.to_csv(f"{path_link}\link{str(numero)}.csv")
    numero +=1

datos_totales_1 = pd.read_csv(f'{path_descargas}/transferresultsplayers_28_8_2022, 21_55_10.csv')
link1 = pd.read_csv(f'{path_link}\link1.csv')

datos_totales_1['link'] = link1['link']
datos_totales_1.to_csv(f'{path_descargas}/total1.csv ')