import streamlit as st
import pandas as pd

# Función para cargar la hoja de "PREGRADO" o "POSGRADO Y EXTERIOR"
def cargar_hoja_pregrado_posgrado(df):
    encabezado_fila = 2  # Encabezado inicia en la fila 2 (índice 2)
    df.columns = df.iloc[encabezado_fila]
    df = df.drop(index=list(range(encabezado_fila + 1)))
    df = df.reset_index(drop=True)
    return df

# Función para cargar la hoja de "RECURSOS ICETEX" y "TERCEROS", "Hoja1"
def cargar_hoja_recursos(df):
    encabezado_fila = 3  # Encabezado inicia en la fila 3 (índice 3)
    df.columns = df.iloc[encabezado_fila]
    df = df.drop(index=list(range(encabezado_fila + 1)))
    df = df.reset_index(drop=True)
    return df

# Función para cargar la hoja de "Tabla 1"
def cargar_hoja_tabla_1(df):
    encabezado_fila = 0  # Encabezado inicia en la fila 0 (índice 0)
    df.columns = df.iloc[encabezado_fila]
    df = df.drop(index=list(range(encabezado_fila + 1)))
    df = df.reset_index(drop=True)
    return df

# Función para manejar nombres de columnas duplicados
def handle_duplicate_columns(df):
    df.columns = df.columns.fillna('')
    cols = pd.Series(df.columns)
    
    for dup in cols[cols.duplicated()].unique():
        cols[cols[cols == dup].index.values.tolist()] = [f"{dup}_{i+1}" if i != 0 else dup for i in range(sum(cols == dup))]
    
    df.columns = cols
    return df

# Cargar el archivo desde la interfaz de Streamlit
uploaded_file = st.file_uploader("Elige un archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    xls = pd.ExcelFile(uploaded_file)
    st.write("Hojas disponibles en el archivo:")
    sheet_names = xls.sheet_names
    st.write(sheet_names)

    sheet_to_work = st.selectbox("Selecciona una hoja para trabajar", sheet_names)
    raw_df = pd.read_excel(xls, sheet_name=sheet_to_work, header=None)

    # Mostrar datos crudos para ver si hay datos
    st.write("Datos crudos de la hoja seleccionada:")
    st.write(raw_df)

    # Cargar datos según la hoja seleccionada
    if sheet_to_work in ['PREGRADO', 'POSGRADO Y EXTERIOR']:
        df = cargar_hoja_pregrado_posgrado(raw_df)
    elif sheet_to_work in ['RECURSOS ICETEX', 'TERCEROS', 'Hoja1']:
        df = cargar_hoja_recursos(raw_df)
    elif sheet_to_work == 'Tabla 1':
        df = cargar_hoja_tabla_1(raw_df)
    else:
        # Para otras hojas, puedes elegir un encabezado por defecto o adaptarlo
        df = pd.read_excel(xls, sheet_name=sheet_to_work, header=0)

    # Limpiar el DataFrame
    df = df.dropna(axis=1, how='all')  # Eliminar columnas vacías
    df = df.dropna(axis=0, how='any')   # Eliminar filas con datos nulos

    # Manejar columnas duplicadas
    df = handle_duplicate_columns(df)

    # Verificar si el DataFrame está vacío
    if df.empty:
        st.warning("El DataFrame está vacío después de limpiar los datos.")
    else:
        st.write(f"Datos de la hoja '{sheet_to_work}':")
        st.write(df.head())  # Mostrar las primeras filas
else:
    st.write("Por favor, carga un archivo Excel.")

