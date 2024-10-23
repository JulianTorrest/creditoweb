import pandas as pd

# URL del archivo Excel en el repositorio público de GitHub
url = 'https://github.com/JulianTorrest/creditoweb/blob/main/tabla%20Condiciones%20Credito%20ICETEX%202024-1%20-%20Revisi%C3%B3n%20Pagina%20Web%20(1).xlsx'

# Lee el archivo Excel desde la URL
df = pd.read_excel(url)

# Muestra el contenido del archivo
print(df.head())

