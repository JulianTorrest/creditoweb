import streamlit as st
import pandas as pd

# Cargar el archivo de Excel directamente desde la ruta proporcionada
file_path = '/mnt/data/tabla Condiciones Credito ICETEX 2024-1 - Revisión Pagina Web.xlsx'

# Leer el archivo Excel
df = pd.read_excel(file_path)

# Mostrar la tabla en Streamlit
st.write("Datos del archivo Excel:")
st.write(df.head())  # Mostrar las primeras filas
