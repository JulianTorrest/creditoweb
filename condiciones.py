import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio

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

# Función para calcular estadísticas sin incluir encabezados
def calcular_estadisticas(df):
    estadisticas = {}

    for col in df.columns:
        # Convertir todos los valores a strings para evitar errores de comparación
        df[col] = df[col].astype(str)

        # Excluir filas que contengan valores vacíos o que sean iguales a los encabezados
        conteo = df[col].value_counts(dropna=False)

        # Filtrar para no incluir el encabezado mismo como opción de respuesta
        conteo = conteo[conteo.index != col]

        estadisticas[col] = conteo

    return pd.DataFrame(estadisticas)

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
                # Excluir el encabezado de la columna en el conteo de valores
                conteo = df[col].value_counts().reset_index()
                conteo.columns = [col, 'count']  # Renombrar las columnas para el gráfico
                
                # Filtrar para no incluir el nombre de la columna como opción
                conteo = conteo[conteo[col] != col]

                st.write(f"**{col}:**")
                st.write(conteo)

                # 3. Seleccionar el tipo de gráfico
                grafico_tipo = st.selectbox(f"Selecciona tipo de gráfico para {col}", 
                                             ["Barras", "Puntos", "Apiladas", "Líneas", "Área", 
                                              "Mapa de Calor", "Violín", "Caja", "Radar", "Dispersión"], 
                                             key=col)

                # 4. Seleccionar color para el gráfico
                color_options = [
                    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", 
                    "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", 
                    "#bcbd22", "#17becf"
                ]
                color = st.selectbox(f"Selecciona un color para {col}", color_options)

                # 5. Título del gráfico
                titulo_grafico = st.text_input(f"Título del gráfico para {col}", f"Gráfico de {col}")

                # 6. Generar el gráfico
                if grafico_tipo == "Barras":
                    fig = px.bar(conteo, x=col, y='count', labels={col: col, 'count': 'Conteo'}, title=titulo_grafico)
                    fig.update_traces(marker_color=color)
                elif grafico_tipo == "Puntos":
                    fig = px.scatter(conteo, x=col, y='count', title=titulo_grafico)
                    fig.update_traces(marker=dict(color=color))
                elif grafico_tipo == "Apiladas":
                    fig = px.bar(conteo, x=col, y='count', title=titulo_grafico, text='count')
                    fig.update_traces(marker_color=color)
                elif grafico_tipo == "Líneas":
                    fig = px.line(conteo, x=col, y='count', title=titulo_grafico)
                elif grafico_tipo == "Área":
                    fig = px.area(conteo, x=col, y='count', title=titulo_grafico)
                elif grafico_tipo == "Mapa de Calor":
                    fig = px.imshow(conteo.pivot(index=col, columns='count', values='count'), title=titulo_grafico)
                elif grafico_tipo == "Violín":
                    fig = px.violin(conteo, y='count', title=titulo_grafico)
                elif grafico_tipo == "Caja":
                    fig = px.box(conteo, y='count', title=titulo_grafico)
                elif grafico_tipo == "Radar":
                    fig = px.line_polar(conteo, r='count', theta=col, line_close=True, title=titulo_grafico)
                elif grafico_tipo == "Dispersión":
                    fig = px.scatter(conteo, x=col, y='count', title=titulo_grafico)

                # Mostrar el gráfico
                st.plotly_chart(fig)

                # 7. Botones para descargar gráfico en PDF y PNG
                btn_pdf = st.button(f"Descargar gráfico en PDF para {col}")
                btn_png = st.button(f"Descargar gráfico en PNG para {col}")

                if btn_pdf:
                    pio.write_image(fig, f"grafico_{col}.pdf")
                    with open(f"grafico_{col}.pdf", "rb") as f:
                        st.download_button("Descargar PDF", f, file_name=f"grafico_{col}.pdf", mime="application/pdf")

                if btn_png:
                    pio.write_image(fig, f"grafico_{col}.png")
                    with open(f"grafico_{col}.png", "rb") as f:
                        st.download_button("Descargar PNG", f, file_name=f"grafico_{col}.png", mime="image/png")

    except Exception as e:
        st.error(f"Ocurrió un error: {e}")
