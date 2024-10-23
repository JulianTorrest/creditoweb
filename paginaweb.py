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

    # Permitir que el usuario seleccione una hoja para visualizarla
    selected_sheet = st.selectbox("Selecciona una hoja para ver su contenido:", sheets)

    # Mostrar el contenido de la hoja seleccionada
    df = pd.read_excel(url, sheet_name=selected_sheet, engine='openpyxl')

    # Limpiar todas las columnas de valores nulos, vacíos y espacios
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)  
    df = df.apply(lambda x: x.str.lower() if x.dtype == "object" else x)  

    # Crear nueva columna 'Tipo de línea de crédito' basada en la función asignar_tipo_linea_credito
    if 'Línea de crédito' in df.columns:
        df['Tipo de línea de crédito'] = df['Línea de crédito'].apply(asignar_tipo_linea_credito)

    # Permitir al usuario seleccionar las columnas a mostrar
    selected_columns = st.multiselect("Selecciona las columnas que deseas ver:", df.columns)

    # Mostrar las columnas seleccionadas
    if selected_columns:
        st.write(f"Contenido de las columnas seleccionadas: {selected_columns}")
        st.write(df[selected_columns])

    # Gráficos
    st.subheader("Gráficos")

    # Seleccionar el tipo de gráfico
    chart_type = st.selectbox("Selecciona el tipo de gráfico:", ["Barras", "Torta", "Puntos"])

    # Crear gráfico basado en la selección
    if chart_type == "Barras":
        if selected_columns:
            for col in selected_columns:
                count_data = df[col].value_counts()
                plt.figure(figsize=(8, 4))
                count_data.plot(kind='bar')
                plt.title(f"Gráfico de barras para la columna '{col}'")
                plt.xlabel(col)
                plt.ylabel("Cantidad de registros")
                st.pyplot(plt)

    elif chart_type == "Torta":
        if selected_columns:
            for col in selected_columns:
                count_data = df[col].value_counts()
                if count_data.size <= 10:  # Limita a 10 valores únicos para la torta
                    plt.figure(figsize=(8, 4))
                    plt.pie(count_data, labels=count_data.index, autopct='%1.1f%%', startangle=90)
                    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                    st.pyplot(plt)
                else:
                    st.write(f"La columna '{col}' tiene más de 10 categorías únicas, no se puede graficar en torta.")

    elif chart_type == "Puntos":
        if selected_columns and len(selected_columns) >= 2:
            x_axis = st.selectbox("Selecciona la columna para el eje X", selected_columns)
            y_axis = st.selectbox("Selecciona la columna para el eje Y", selected_columns)
            if pd.api.types.is_numeric_dtype(df[x_axis]) and pd.api.types.is_numeric_dtype(df[y_axis]):
                plt.figure(figsize=(8, 4))
                plt.scatter(df[x_axis], df[y_axis])
                plt.title(f"Gráfico de dispersión: {x_axis} vs {y_axis}")
                plt.xlabel(x_axis)
                plt.ylabel(y_axis)
                st.pyplot(plt)
            else:
                st.write("Ambas columnas deben ser numéricas para generar un gráfico de puntos.")
except Exception as e:
    st.write("Error al cargar el archivo Excel:", e)

