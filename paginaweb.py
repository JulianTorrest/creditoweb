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
        "Posgrado País con Deudor Solidario", 
        "Posgrado País sin Deudor Solidario", 
        "Posgrado País Medicina con Deudor Solidario", 
        "Posgrado País Medicina sin Deudor Solidario", 
        "Posgrado País - Servidores Públicos - con Deudor Solidario", 
        "Posgrado País - Servidores Públicos - sin Deudor Solidario", 
        "Posgrado País - Funcionarios del MEN y entidades adscritas - sin Deudor Solidario"]):
        return "posgrado país"

    # Clasificación en Posgrado Exterior
    elif any(sub in linea_credito for sub in [
        "Posgrado Exterior Largo Plazo USD 25.000", 
        "Posgrado Exterior USD 25.000 como complemento a las becas", 
        "Posgrado o Pregrado Exterior Largo Plazo para Sostenimiento USD 12.500", 
        "Posgrado Exterior - Servidores Públicos", 
        "Posgrado Exterior - Funcionarios del MEN y entidades adscritas"]):
        return "posgrado exterior"

    # Clasificación en Pregrado Largo Plazo
    elif any(sub in linea_credito for sub in [
        "País Largo Plazo Tú Eliges 0% Fondo de Garantía Covid19 Afectación Económica", 
        "País Largo Plazo Tú Eliges 0% Fondo de Garantía Covid19 Afectación en Salud", 
        "País Largo Plazo Tú Eliges 10% Fondo de Garantía Covid19 Afectación Económica", 
        "País Largo Plazo Tú Eliges 10% Fondo de Garantía Covid19 Afectación en Salud", 
        "País Largo Plazo Tú Eliges 25% con Fondo de Garantía Covid19 Afectación Económica", 
        "País Largo Plazo Tú Eliges 25% con Fondo de Garantía Covid19 Afectación en Salud", 
        "País Largo Plazo Estudiantes de Comunidades de Especial Protección Constitucional", 
        "País Largo Plazo - Territorial", 
        "País Largo Plazo - Talento de mi Territorio", 
        "País Largo Plazo Mas Colombiano que Nunca", 
        "País Largo Plazo Estudiantes beneficiarios rezagados de programas", 
        "País Largo Plazo Línea para estudiantes que cuentan con apoyo económico", 
        "País Largo Plazo Reservistas de Honor", 
        "País Largo Plazo Oficiales", 
        "País Largo Plazo Suboficiales", 
        "País Largo Plazo Funcionarios del MEN y entidades adscritas"]):
        return "pregrado largo plazo"

    # Clasificación en Pregrado Mediano Plazo
    elif any(sub in linea_credito for sub in [
        "País Mediano Plazo Tú Eliges 30%", 
        "País Mediano Plazo Tú Eliges 40%", 
        "País Mediano Plazo Tú Eliges 60%", 
        "País Mediano Plazo - Reservistas Primera Clase 30%", 
        "País Mediano Plazo Volvamos a Clases", 
        "País Mediano Plazo Francisco José de Caldas", 
        "País Mediano Plazo Funcionarios del MEN y entidades adscritas", 
        "País Mediano Plazo Servidores Públicos"]):
        return "pregrado mediano plazo"

    # Clasificación en Pregrado Corto Plazo
    elif any(sub in linea_credito for sub in [
        "País Corto Plazo Tú Eliges 100%", 
        "País Corto Plazo - Línea Funcionarios del MEN y entidades adscritas - con pago del 100%", 
        "País Corto Plazo Servidores Públicos - con pago del 100%"]):
        return "pregrado corto plazo"

    # Clasificación en Otros Programas
    elif any(sub in linea_credito for sub in [
        "Capacitación de Idiomas en el exterior", 
        "Pasantías e Intercambio Educativo en el exterior", 
        "Capacitación de idiomas en el país"]):
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

    # Limpiar todas las columnas de valores nulos, vacíos y espacios
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)  # Eliminar espacios
    df = df.apply(lambda x: x.str.lower() if x.dtype == "object" else x)  # Convertir a minúsculas
    df = df.dropna()  # Eliminar filas con valores nulos

    # Crear nueva columna 'Tipo de línea de crédito' basada en la función asignar_tipo_linea_credito
    if 'Línea de crédito' in df.columns:
        df['Tipo de línea de crédito'] = df['Línea de crédito'].apply(asignar_tipo_linea_credito)

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

        # Gráficos
        st.subheader("Gráficos")

        # Seleccionar el tipo de gráfico
        chart_type = st.selectbox("Selecciona el tipo de gráfico:", ["Barras", "Torta", "Puntos"])

        # Crear gráfico basado en la selección
        if chart_type == "Barras":
            if selected_columns:
                for col in selected_columns:
                    # Contar la cantidad de registros por categoría
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
                    if count_data.size > 10:
                        count_data = count_data[:9].append(pd.Series(count_data[9:].sum(), index=["Otros"]))
                        plt.figure(figsize=(8, 4))
                        plt.pie(count_data, labels=count_data.index, autopct='%1.1f%%', startangle=90)
                        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                        st.pyplot(plt)
                    else:
                        st.write(f"La columna '{col}' tiene más de 10 categorías únicas, no se puede graficar en torta.")

        elif chart_type == "Puntos":
            if selected_columns and len(selected_columns) >= 2:
                # Mostrar gráfico de dispersión con dos columnas numéricas seleccionadas
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

