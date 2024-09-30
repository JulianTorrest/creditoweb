import streamlit as st
import pandas as pd

# Cargar el archivo desde la interfaz de Streamlit
uploaded_file = st.file_uploader("Elige un archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    # Leer el archivo Excel cargado por el usuario
    df = pd.read_excel(uploaded_file)

    # Mostrar la tabla en Streamlit
    st.write("Datos del archivo Excel:")
    st.write(df.head())  # Mostrar las primeras filas
else:
    st.write("Por favor, carga un archivo Excel.")
