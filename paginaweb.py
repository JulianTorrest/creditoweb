import pandas as pd

# URL del archivo Excel en el repositorio público de GitHub
url = 'https://github.com/usuario/repositorio/raw/main/ruta_al_archivo/archivo.xlsx'

# Lee el archivo Excel desde la URL
df = pd.read_excel(url)

# Muestra el contenido del archivo
print(df.head())

