import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Título de la aplicación
st.title("Visualización de Hojas en un Archivo Excel")

# URL del archivo Excel en el repositorio público de GitHub (versión raw)
url = 'https://github.com/JulianTorrest/creditoweb/raw/main/tabla%20Condiciones%20Credito%20ICETEX%202024-1%20-%20Revisi%C3%B3n%20Pagina%20Web%20(1).xlsx'

# Función para asignar tipo de línea de crédito (anteriormente subcategoría)
def asignar_tipo_linea_credito(linea_credito):
    # Clasificación en Posgrado País
    if any(sub in linea_credito for sub in [
        "posgrado país con deudor solidario", 
        "posgrado país sin deudor solidario", 
        "posgrado país medicina con deudor solidario", 
        "posgrado país medicina sin deudor solidario", 
        "posgrado país - servidores públicos - con deudor solidario", 
        "posgrado país - servidores públicos - sin deudor solidario", 
        "posgrado país - funcionarios del men y entidades adscritas - sin deudor solidario"]):
        return "posgrado país"

    # Clasificación en Posgrado Exterior
    elif any(sub in linea_credito for sub in [
        "posgrado exterior largo plazo usd 25.000", 
        "posgrado exterior usd 25.000 como complemento a las becas", 
        "posgrado o pregrado exterior largo plazo para sostenimiento usd 12.500", 
        "posgrado exterior - servidores públicos", 
        "posgrado exterior - funcionarios del men y entidades adscritas"]):
        return "posgrado exterior"

    # Clasificación en Pregrado Largo Plazo
    elif any(sub in linea_credito for sub in [
        "país largo plazo tú eliges 0% fondo de garantía covid19 afectación económica", 
        "país largo plazo tú eliges 0% fondo de garantía covid19 afectación en salud", 
        "país largo plazo tú eliges 10% fondo de garantía covid19 afectación económica", 
        "país largo plazo tú eliges 10% fondo de garantía covid19 afectación en salud", 
        "país largo plazo tú eliges 25% con fondo de garantía covid19 afectación económica", 
        "país largo plazo tú eliges 25% con fondo de garantía covid19 afectación en salud", 
        "país largo plazo estudiantes de comunidades de especial protección constitucional", 
        "país largo plazo - territorial", 
        "país largo plazo - talento de mi territorio", 
        "país largo plazo mas colombiano que nunca", 
        "país largo plazo estudiantes beneficiarios rezagados de programas", 
        "país largo plazo línea para estudiantes que cuentan con apoyo económico", 
        "país largo plazo reservistas de honor", 
        "país largo plazo oficiales", 
        "país largo plazo suboficiales", 
        "país largo plazo funcionarios del men y entidades adscritas"]):
        return "pregrado largo plazo"

    # Clasificación en Pregrado Mediano Plazo
    elif any(sub in linea_credito for sub in [
        "país mediano plazo tú eliges 30%", 
        "país mediano plazo tú eliges 40%", 
        "país mediano plazo tú eliges 60%", 
        "país mediano plazo - reservistas primera clase 30%", 
        "país mediano plazo volvamos a clases", 
        "país mediano plazo francisco josé de caldas", 
        "país mediano plazo funcionarios del men y entidades adscritas", 
        "país mediano plazo servidores públicos"]):
        return "pregrado mediano plazo"

    # Clasificación en Pregrado Corto Plazo
    elif any(sub in linea_credito for sub in [
        "país corto plazo tú eliges 100%", 
        "país corto plazo - línea funcionarios del men y entidades adscritas - con pago del 100%", 
        "país corto plazo servidores públicos - con pago del 100%"]):
        return "pregrado corto plazo"

    # Clasificación en Otros Programas
    elif any(sub in linea_credito for sub in [
        "capacitación de idiomas en el exterior", 
        "pasantías e intercambio educativo en el exterior", 
        "capacitación de idiomas en el país"]):
        return "otros programas"

    # Si no coincide con ninguna categoría
    else:
        return "otra categoría"

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

    # Depuración: Mostrar primeras filas del DataFrame original
    st.write("DataFrame original:")
    st.write(df.head())

    # Limpiar todas las columnas de valores nulos, vacíos y espacios
    # Eliminar espacios solo en columnas de texto
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)  
    # Convertir a minúsculas solo en columnas de texto
    df = df.apply(lambda x: x.str.lower() if x.dtype == "object" else x)  

    # Depuración: Mostrar primeras filas después de limpiar los datos
    st.write("DataFrame después de limpieza (sin espacios y en minúsculas):")
    st.write(df.head())

    # Crear nueva columna 'Tipo de línea de crédito' basada en la función asignar_tipo_linea_credito
    if 'Línea de crédito' in df.columns:
        df['Tipo de línea de crédito'] = df['Línea de crédito'].apply(asignar_tipo_linea_credito)

    # Depuración: Mostrar primeras filas con la nueva columna 'Tipo de línea de crédito'
    st.write("DataFrame con 'Tipo de línea de crédito':")
    st.write(df[['Línea de crédito', 'Tipo de línea de crédito']].head())

    # Mostrar los valores únicos en la columna 'Línea de crédito' para verificar los datos
    st.write("Valores únicos en la columna 'Línea de crédito':")
    st.write(df['Línea de crédito'].unique())

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
        st.write("Valores únicos en las columnas seleccionadas:")
        for col in selected_columns:
            st.write(f"Columna '{col}':")
            st.write(df[col].dropna().unique())  # Mostrar valores únicos omitiendo nulos
except Exception as e:
    st.write("Error al cargar el archivo Excel:", e)

