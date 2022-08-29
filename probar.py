from pathlib import Path
from datetime import datetime
import os


path = Path(__file__).parent
path_descargas = path.joinpath('files')
path_gurdar = path.joinpath('files/')
ahora = datetime.now()
print(path_descargas)
print(path)
print(f'{path_gurdar}link.csv')

os.remove(path)