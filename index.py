from dowload_data_selenium import Hattrick_proyect
from proceso_datos import create_links_mas_ides, data_mas_links
import logging
from datetime import datetime
from pathlib import Path

# configuracion del logging
# Formato del log: %Y-%m-%d - nombre_logger - mensaje
logging.basicConfig(filename='logging.log', format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG,
                    datefmt='%Y-%m-%d')
## Por si necesitamos que los logs tengan el nombre del archivo donde se encuentra
logger = logging.getLogger(__name__)

path = Path(__file__).parent
path_descargas = path.joinpath('dowload_files')
path_gurdar_link = path.joinpath('links_transitorios')
path_datos_finales = path.joinpath('datos_finales')

if __name__ == '__main__':
    hora_inicio = datetime.now()
    logger.info(f'Comienza la ejecucion del programa: {hora_inicio} \n')
    hattrick = Hattrick_proyect()
    hattrick.setup()
    hattrick.login()
    hattrick.tranfer()
    hattrick.borrar_archivos_antiguos(path_descargas)
    hattrick.dowload_file()
    hattrick.paginar()
    hattrick.create_df()
    create_links_mas_ides()
    hattrick.borrar_archivos_antiguos(path_datos_finales)
    data_mas_links()
    hora_fin = datetime.now()
    logger.info(f'Fin de la ejecucion del programa: {hora_fin} \n')
    logger.info(f'Tiempo total de ejecucion: {hora_fin - hora_inicio}')