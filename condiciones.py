import streamlit as st
import pandas as pd

# Función para detectar la fila de inicio de datos
def detect_header_row(df):
    """
    Detecta la primera fila que parece contener los encabezados de las columnas.
    Retorna el índice de la fila donde comienzan los datos (encabezados).
    """
    for i, row in df.iterrows():
        if row.notna().sum() > 3:  # Umbral para detectar una fila válida con más de 3 valores no nulos
            return i
    return 0  # Por defecto, si no encuentra ninguna, usar la primera fila

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

    # Leer los datos de la hoja seleccionada sin encabezado inicialmente
    raw_df = pd.read_excel(xls, sheet_name=sheet_to_work, header=None)

    # Detectar la fila donde comienzan los encabezados de las columnas
    header_row = detect_header_row(raw_df)
    
    # Volver a leer los datos utilizando la fila detectada como encabezado
    df = pd.read_excel(xls, sheet_name=sheet_to_work, header=header_row)

    # Mostrar la tabla procesada
    st.write(f"Datos de la hoja '{sheet_to_work}':")
    st.write(df.head())  # Mostrar las primeras filas
else:
    st.write("Por favor, carga un archivo Excel.")

