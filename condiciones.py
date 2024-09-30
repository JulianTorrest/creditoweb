import streamlit as st
import pandas as pd

# Cargar el archivo desde la interfaz de Streamlit
uploaded_file = st.file_uploader("Elige un archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    # Cargar todas las hojas del archivo Excel
    xls = pd.ExcelFile(uploaded_file)
    
    # Mostrar las hojas disponibles
    st.write("Hojas disponibles en el archivo:")
    sheet_names = xls.sheet_names
    st.write(sheet_names)

    # Seleccionar la hoja con la que el usuario quiere trabajar
    sheet_to_work = st.selectbox("Selecciona una hoja para trabajar", sheet_names)

    # Leer los datos de la hoja seleccionada
    df = pd.read_excel(xls, sheet_name=sheet_to_work)

    # Mostrar los primeros datos de la hoja seleccionada
    st.write(f"Datos de la hoja '{sheet_to_work}':")
    st.write(df.head())  # Mostrar las primeras filas
else:
    st.write("Por favor, carga un archivo Excel.")
