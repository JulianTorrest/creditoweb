import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
import base64
import os

# Función para cargar la hoja de "PREGRADO" o "POSGRADO Y EXTERIOR"
def cargar_hoja_pregrado_posgrado(df):
    encabezado_fila = 2
    df.columns = df.iloc[encabezado_fila]
    df = df.drop(index=list(range(encabezado_fila + 1)))
    df = df.reset_index(drop=True)
    return df

# Función para cargar la hoja de "RECURSOS ICETEX" y "TERCEROS", "Hoja1"
def cargar_hoja_recursos(df):
    encabezado_fila = 2
    df.columns = df.iloc[encabezado_fila]
    df = df.drop(index=list(range(encabezado_fila + 1)))
    df = df.reset_index(drop=True)
    return df

# Función para cargar la hoja de "Tabla 1"
def cargar_hoja_tabla_1(df):
    encabezado_fila = 0
    df.columns = df.iloc[encabezado_fila]
    df = df.drop(index=list(range(encabezado_fila + 1)))
    df = df.reset_index(drop=True)
    return df

# Función para limpiar el DataFrame
def limpiar_dataframe(df):
    df = df.dropna(axis=1, how='all')
    df = df.dropna(axis=0, how='all')
    df.columns = df.columns.fillna('')
    cols = pd.Series(df.columns)
    
    for dup in cols[cols.duplicated()].unique():
        cols[cols[cols == dup].index.values.tolist()] = [f"{dup}_{i+1}" if i != 0 else dup for i in range(sum(cols == dup))]

    df.columns = cols
    return df

# Función para calcular estadísticas sin incluir encabezados
def calcular_estadisticas(df):
    estadisticas = {}

    for col in df.columns:
        df[col] = df[col].astype(str)
        conteo = df[col].value_counts(dropna=False)
        conteo = conteo[conteo.index != col]
        estadisticas[col] = conteo

    return pd.DataFrame(estadisticas)

# Función para convertir gráficos a base64 para descarga
def get_image_download_link(fig, filename, file_format="png"):
    # Guardar la imagen temporalmente
    image_bytes = fig.to_image(format=file_format)
    
    # Codificar en base64 para descargar
    b64 = base64.b64encode(image_bytes).decode()

    href = f'<a href="data:image/{file_format};base64,{b64}" download="{filename}.{file_format}">Descargar como {file_format.upper()}</a>'
    return href

# Función para descargar como PDF usando la librería jsPDF en el frontend
def add_print_button(fig_id):
    # Agregamos un botón para imprimir el gráfico en formato PDF usando jsPDF en el frontend
    print_js = f"""
    <script>
        function printPDF{fig_id}() {{
            var element = document.getElementById('{fig_id}');
            html2canvas(element).then(function(canvas) {{
                var imgData = canvas.toDataURL('image/png');
                var pdf = new jsPDF();
                pdf.addImage(imgData, 'PNG', 10, 10);
                pdf.save("{fig_id}.pdf");
            }});
        }}
    </script>
    <button onclick="printPDF{fig_id}()">Descargar como PDF</button>
    """
    return print_js

# Cargar el archivo desde la interfaz de Streamlit
uploaded_file = st.file_uploader("Elige un archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    try:
        xls = pd.ExcelFile(uploaded_file)
        st.write("Hojas disponibles en el archivo:")
        sheet_names = xls.sheet_names
        st.write(sheet_names)

        sheet_to_work = st.selectbox("Selecciona una hoja para trabajar", sheet_names)
        raw_df = pd.read_excel(xls, sheet_name=sheet_to_work, header=None)

        st.write("Datos crudos de la hoja seleccionada:")
        st.write(raw_df)

        if sheet_to_work in ['PREGRADO', 'POSGRADO Y EXTERIOR']:
            df = cargar_hoja_pregrado_posgrado(raw_df)
        elif sheet_to_work in ['RECURSOS ICETEX', 'TERCEROS', 'Hoja1']:
            df = cargar_hoja_recursos(raw_df)
        elif sheet_to_work == 'Tabla 1':
            df = cargar_hoja_tabla_1(raw_df)
        else:
            df = pd.read_excel(xls, sheet_name=sheet_to_work, header=0)

        df = limpiar_dataframe(df)

        st.write("DataFrame después de limpiar:")
        if df.empty:
            st.warning("El DataFrame está vacío después de limpiar los datos.")
        else:
            st.write(df.head())

            st.write("Columnas disponibles en el DataFrame:")
            st.write(df.columns.tolist())

            for col in df.columns:
                conteo = df[col].value_counts().reset_index()
                conteo.columns = [col, 'count']
                conteo = conteo[conteo[col] != col]

                st.write(f"**{col}:**")
                st.write(conteo)

                grafico_tipo = st.selectbox(f"Selecciona tipo de gráfico para {col}", 
                                             ["Barras", "Puntos", "Apiladas", "Líneas", "Área", 
                                              "Mapa de Calor", "Violín", "Caja", "Radar", "Dispersión"], 
                                             key=col)

                color_options = [
                    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", 
                    "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", 
                    "#bcbd22", "#17becf"
                ]
                color = st.selectbox(f"Selecciona un color para {col}", color_options)

                titulo_grafico = st.text_input(f"Título del gráfico para {col}", f"Gráfico de {col}")

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

                # Botón para descargar como imagen
                st.markdown(get_image_download_link(fig, f"grafico_{col}"), unsafe_allow_html=True)

                # Agregar el botón para descargar como PDF
                st.markdown(add_print_button(f"grafico_{col}"), unsafe_allow_html=True)

                # Botón para imprimir el gráfico
                st.markdown(f'<button onclick="window.print()">Imprimir Gráfico</button>', unsafe_allow_html=True)

            st.write("Estadísticas descriptivas (sin encabezados):")
            estadisticas = calcular_estadisticas(df)
            st.write(estadisticas)

    except Exception as e:
        st.error(f"Error al procesar el archivo: {e}")
