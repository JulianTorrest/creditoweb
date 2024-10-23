import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Título de la aplicación
st.title("Visualización de Hojas en un Archivo Excel")

# URL del archivo Excel en el repositorio público de GitHub (versión raw)
url = 'https://github.com/JulianTorrest/creditoweb/raw/main/tabla%20Condiciones%20Credito%20ICETEX%202024-1%20-%20Revisi%C3%B3n%20Pagina%20Web%20(1).xlsx'

# Cargar el archivo Excel
try:
    # Abrimos el archivo Excel desde la URL
    xls = pd.ExcelFile(url, engine='openpyxl')

    # Listar las hojas (páginas) del archivo Excel
    sheets = xls.sheet_names

    # Mostrar la lista de hojas en Streamlit
    st.write("Hojas en el archivo Excel:")
    st.write(sheets)

    # Permitir que el usuario seleccione una hoja para visualizarla
    selected_sheet = st.selectbox("Selecciona una hoja para ver su contenido:", sheets)

    # Mostrar el contenido de la hoja seleccionada
    df = pd.read_excel(url, sheet_name=selected_sheet, engine='openpyxl')

    # Permitir al usuario seleccionar las columnas a mostrar
    selected_columns = st.multiselect("Selecciona las columnas que deseas ver:", df.columns)

    # Mostrar las columnas seleccionadas
    if selected_columns:
        st.write(f"Contenido de las columnas seleccionadas: {selected_columns}")
        st.write(df[selected_columns])

        # Agregar resumen estadístico debajo del contenido, omitiendo los valores nulos
        st.write("Resumen estadístico de los datos (sin valores nulos):")
        df_clean = df[selected_columns].dropna()  # Elimina las filas con valores nulos en las columnas seleccionadas
        st.write(df_clean.describe())

        # Mostrar valores únicos (distinct) de las columnas seleccionadas sin tomar en cuenta los encabezados
        st.write("Valores únicos en las columnas seleccionadas (sin títulos de columnas):")
        for col in selected_columns:
            st.write(f"Columna '{col}':")
            # Tomar solo los datos a partir de la segunda fila (omitir encabezados)
            st.write(df[col].iloc[1:].dropna().unique())  # Mostrar valores únicos omitiendo nulos

        # Gráficos
        st.subheader("Gráficos")

        # Seleccionar el tipo de gráfico
        chart_type = st.selectbox("Selecciona el tipo de gráfico:", ["Barras", "Torta", "Puntos"])

        # Crear gráfico basado en la selección
        if chart_type == "Barras":
            if selected_columns:
                for col in selected_columns:
                    if pd.api.types.is_numeric_dtype(df[col]):
                        st.bar_chart(df[col].dropna())
                    else:
                        st.write(f"La columna '{col}' no es numérica, no se puede graficar en barras.")
        
        elif chart_type == "Torta":
            if selected_columns:
                for col in selected_columns:
                    if df[col].nunique() <= 10:  # Limitamos a 10 valores únicos para la torta
                        data = df[col].value_counts()
                        plt.figure(figsize=(8, 4))
                        plt.pie(data, labels=data.index, autopct='%1.1f%%', startangle=90)
                        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                        st.pyplot(plt)
                    else:
                        st.write(f"La columna '{col}' tiene más de 10 categorías únicas, no se puede graficar en torta.")

        elif chart_type == "Puntos":
            if selected_columns and len(selected_columns) >= 2:  # Se requieren al menos 2 columnas para un gráfico de dispersión
                x_col = st.selectbox("Selecciona la columna para el eje X:", selected_columns)
                y_col = st.selectbox("Selecciona la columna para el eje Y:", selected_columns)
                if pd.api.types.is_numeric_dtype(df[x_col]) and pd.api.types.is_numeric_dtype(df[y_col]):
                    plt.figure(figsize=(8, 4))
                    plt.scatter(df[x_col], df[y_col])
                    plt.xlabel(x_col)
                    plt.ylabel(y_col)
                    plt.title(f"Gráfico de dispersión: {y_col} vs {x_col}")
                    st.pyplot(plt)
                else:
                    st.write("Asegúrate de seleccionar columnas numéricas para el gráfico de dispersión.")

    else:
        st.write("No se han seleccionado columnas para mostrar.")

except Exception as e:
    st.error(f"No se pudo cargar el archivo Excel. Error: {e}")

