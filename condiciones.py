import streamlit as st
import pandas as pd

# Función para detectar la fila de inicio de datos
def detect_header_row(df):
    for i, row in df.iterrows():
        if row.notna().sum() > 3:  # Puedes ajustar el número según sea necesario
            return i
    return 0

# Función para cargar la hoja de "POSGRADO Y EXTERIOR"
def cargar_hoja_posgrado_y_exterior(df):
    encabezado_fila = 2
    df.columns = df.iloc[encabezado_fila]
    df = df.drop(index=list(range(encabezado_fila + 1)))
    df = df.reset_index(drop=True)
    return df

# Función para manejar nombres de columnas duplicados
def handle_duplicate_columns(df):
    # Reemplaza los valores NaN por un string vacío para evitar errores
    df.columns = df.columns.fillna('')
    cols = pd.Series(df.columns)
    
    # Crear un índice para cada nombre de columna duplicado
    for dup in cols[cols.duplicated()].unique():
        cols[cols[cols == dup].index.values.tolist()] = [f"{dup}_{i+1}" if i != 0 else dup for i in range(sum(cols == dup))]
    
    # Asignar nombres únicos a las columnas
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

    if sheet_to_work == 'POSGRADO Y EXTERIOR':
        df = cargar_hoja_posgrado_y_exterior(raw_df)
    else:
        header_row = detect_header_row(raw_df)
        df = pd.read_excel(xls, sheet_name=sheet_to_work, header=header_row)

    # Limpiar el DataFrame
    df = df.dropna(axis=1, how='all')  # Eliminar columnas vacías
    df = df.dropna(axis=0, how='any')   # Eliminar filas con datos nulos

    # Manejar columnas duplicadas
    df = handle_duplicate_columns(df)

    # Intentar mostrar el DataFrame
    try:
        st.write(f"Datos de la hoja '{sheet_to_work}':")
        st.write(df.head())  # Mostrar las primeras filas
    except Exception as e:
        st.error(f"Ocurrió un error al mostrar los datos: {e}")
        st.write("Aquí hay una vista previa del DataFrame:")
        st.write(df)
else:
    st.write("Por favor, carga un archivo Excel.")

