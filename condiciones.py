import streamlit as st
import pandas as pd
import plotly.express as px

# Función para cargar la hoja de "PREGRADO" o "POSGRADO Y EXTERIOR"
def cargar_hoja_pregrado_posgrado(df):
    encabezado_fila = 2  # Iniciar desde la fila 2, que corresponde al índice 1
    df.columns = df.iloc[encabezado_fila]  # Establecer los encabezados
    df = df.drop(index=list(range(encabezado_fila + 1)))  # Eliminar filas hasta el encabezado
    df = df.reset_index(drop=True)  # Reiniciar los índices
    return df

# Función para cargar la hoja de "RECURSOS ICETEX" y "TERCEROS", "Hoja1"
def cargar_hoja_recursos(df):
    encabezado_fila = 2  # Iniciar desde la fila 3, que corresponde al índice 2
    df.columns = df.iloc[encabezado_fila]  # Establecer los encabezados
    df = df.drop(index=list(range(encabezado_fila + 1)))  # Eliminar filas hasta el encabezado
    df = df.reset_index(drop=True)  # Reiniciar los índices
    return df

# Función para cargar la hoja de "Tabla 1"
def cargar_hoja_tabla_1(df):
    encabezado_fila = 0  # Para "Tabla 1", comenzamos desde la fila 0
    df.columns = df.iloc[encabezado_fila]  # Establecer los encabezados
    df = df.drop(index=list(range(encabezado_fila + 1)))  # Eliminar filas hasta el encabezado
    df = df.reset_index(drop=True)  # Reiniciar los índices
    return df

# Función para limpiar el DataFrame
def limpiar_dataframe(df):
    # Eliminar columnas vacías
    df = df.dropna(axis=1, how='all')
    
    # Eliminar filas vacías
    df = df.dropna(axis=0, how='all')
    
    # Manejar nombres de columnas duplicados
    df.columns = df.columns.fillna('')  # Llenar los NaN con cadenas vacías
    cols = pd.Series(df.columns)
    
    for dup in cols[cols.duplicated()].unique():
        cols[cols[cols == dup].index.values.tolist()] = [f"{dup}_{i+1}" if i != 0 else dup for i in range(sum(cols == dup))]
    
    df.columns = cols
    return df

# Función para calcular estadísticas
def calcular_estadisticas(df):
    # Asegurarnos de que solo tomamos columnas numéricas para estadísticas
    estadisticas = df.select_dtypes(include='number').describe()  # Calcular estadísticas de columnas numéricas
    return estadisticas

# Cargar el archivo desde la interfaz de Streamlit
uploaded_file = st.file_uploader("Elige un archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    try:
        xls = pd.ExcelFile(uploaded_file)
        st.write("Hojas disponibles en el archivo:")
        sheet_names = xls.sheet_names
        st.write(sheet_names)

        sheet_to_work = st.selectbox("Selecciona una hoja para trabajar", sheet_names)
        raw_df = pd.read_excel(xls, sheet_name=sheet_to_work, header=None)  # Leer sin encabezados

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
            df = pd.read_excel(xls, sheet_name=sheet_to_work, header=0)  # Cargar sin cambios

        # Limpiar el DataFrame
        df = limpiar_dataframe(df)

        # Mostrar el DataFrame después de limpiar
        st.write("DataFrame después de establecer encabezados y limpiar:")
        if df.empty:
            st.warning("El DataFrame está vacío después de limpiar los datos.")
        else:
            st.write(df.head())  # Mostrar las primeras filas
            
            # 1. Listar las columnas
            st.write("Columnas disponibles en el DataFrame:")
            st.write(df.columns.tolist())

            # 2. Contar opciones de respuesta de cada columna
            for col in df.columns:
                conteo = df[col].value_counts().reset_index()
                conteo.columns = [col, 'count']  # Renombrar las columnas para el gráfico
                st.write(f"**{col}:**")
                st.write(conteo)

                # 3. Seleccionar el tipo de gráfico
                grafico_tipo = st.selectbox(f"Selecciona tipo de gráfico para {col}", ["Barra", "Torta", "Histograma"], key=col)

                # 4. Generar el gráfico
                if grafico_tipo == "Barra":
                    fig = px.bar(conteo, x=col, y='count', labels={col: col, 'count': 'Conteo'})
                elif grafico_tipo == "Torta":
                    fig = px.pie(conteo, names=col, values='count', title=f'Distribución de {col}')
                elif grafico_tipo == "Histograma":
                    fig = px.histogram(conteo, x=col, y='count', title=f'Histograma de {col}')

                # Mostrar el gráfico
                st.plotly_chart(fig)

            # 5. Mostrar estadísticas descriptivas
            st.write("Estadísticas descriptivas:")
            estadisticas = calcular_estadisticas(df)
            if not estadisticas.empty:
                st.write(estadisticas)  # Mostrar las estadísticas
            else:
                st.warning("No se encontraron columnas numéricas para calcular estadísticas.")

    except Exception as e:
        st.error(f"Ocurrió un error: {e}")
else:
    st.write("Por favor, carga un archivo Excel.")
