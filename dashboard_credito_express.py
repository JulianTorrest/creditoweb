import streamlit as st
import pandas as pd
import numpy as np
import random

# Función para generar datos dummy
def generar_datos_dummy(num_solicitudes=300):
    estrato = np.random.choice([1, 2, 3, 4, 5, 6], num_solicitudes)
    sexo = np.random.choice(['Masculino', 'Femenino'], num_solicitudes)
    rango_edad = np.random.choice(['18-25', '26-30', '31-35', '36-40', '40+'], num_solicitudes)
    ubicacion = np.random.choice(['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena', 'Pereira', 'Manizales', 'Bucaramanga'], num_solicitudes)
    año_pregrado = np.random.choice([f'{a}' for a in range(2000, 2024)], num_solicitudes)
    area_pregrado = np.random.choice(['Ciencias Sociales', 'Ingeniería', 'Ciencias de la Salud', 'Artes', 'Ciencias Naturales'], num_solicitudes)
    area_aplicacion = np.random.choice(['Ciencias Sociales', 'Ingeniería', 'Ciencias de la Salud', 'Artes', 'Ciencias Naturales'], num_solicitudes)
    empleo_status = np.random.choice(['Empleado', 'Desempleado', 'Independiente'], num_solicitudes)
    antiguedad_empleo = np.random.choice(['Menos de 1 año', '1-3 años', 'Más de 3 años'], num_solicitudes)
    ingreso_mensual = np.random.randint(1000000, 10000000, num_solicitudes)
    estado_civil = np.random.choice(['Soltero/a', 'Casado/a', 'Divorciado/a', 'Viudo/a'], num_solicitudes)
    patrimonio = np.random.choice(['< 10 millones', '10-50 millones', '50-100 millones', '100+ millones'], num_solicitudes)
    desembolsos = np.random.randint(1, 13, num_solicitudes)

    # Crear DataFrame con los datos dummy
    data = pd.DataFrame({
        'Estrato Socioeconómico': estrato,
        'Sexo Biológico': sexo,
        'Rango de Edad': rango_edad,
        'Ubicación de Residencia': ubicacion,
        'Año de Finalización del Pregrado': año_pregrado,
        'Área del Conocimiento (Pregrado)': area_pregrado,
        'Área del Conocimiento (Aplicación)': area_aplicacion,
        'Estado de Empleo': empleo_status,
        'Antigüedad del Último Empleo': antiguedad_empleo,
        'Ingreso Mensual (COP)': ingreso_mensual,
        'Estado Civil': estado_civil,
        'Patrimonio (Rango)': patrimonio,
        'Cantidad de Desembolsos': desembolsos
    })

    return data

# Función para la página principal del dashboard
def pagina_principal():
    st.title("Dashboard - Créditos Educativos ICETEX")
    
    # Generar datos dummy
    num_solicitudes = 300
    data = generar_datos_dummy(num_solicitudes)
    
    st.header("Resumen de Información del Postulante")
    
    # Mostrar DataFrame
    st.subheader(f"Mostrando los primeros {num_solicitudes} registros:")
    st.dataframe(data.head(10))
    
    # Mostrar métricas principales
    st.metric(label="Número Total de Solicitudes", value=num_solicitudes)
    
    # Mostrar histogramas y gráficas
    st.subheader("Distribución por Estrato Socioeconómico")
    st.bar_chart(data['Estrato Socioeconómico'].value_counts())

    st.subheader("Distribución por Sexo Biológico")
    st.bar_chart(data['Sexo Biológico'].value_counts())

    st.subheader("Distribución por Estado de Empleo")
    st.bar_chart(data['Estado de Empleo'].value_counts())

    st.subheader("Distribución de Ingreso Mensual")
    st.bar_chart(data['Ingreso Mensual (COP)'].value_counts(bins=10))
    
    # Botón para ir a la segunda página
    if st.button("Ir a más detalles"):
        st.session_state['page'] = 'segunda_pagina'

# Función para la segunda página
def segunda_pagina():
    st.title("Segunda Página - Información Adicional")
    
    # Generar datos dummy
    num_solicitudes = 300
    data = generar_datos_dummy(num_solicitudes)

    # Mostrar más detalles en gráficos
    st.subheader("Distribución por Rango de Edad")
    st.bar_chart(data['Rango de Edad'].value_counts())

    st.subheader("Distribución por Estado Civil")
    st.bar_chart(data['Estado Civil'].value_counts())
    
    st.subheader("Distribución por Área del Conocimiento (Pregrado)")
    st.bar_chart(data['Área del Conocimiento (Pregrado)'].value_counts())

    st.subheader("Distribución por Ubicación de Residencia")
    st.bar_chart(data['Ubicación de Residencia'].value_counts())

    # Botón para regresar a la página principal
    if st.button("Regresar al dashboard principal"):
        st.session_state['page'] = 'pagina_principal'

# Inicializar la sesión de navegación
if 'page' not in st.session_state:
    st.session_state['page'] = 'pagina_principal'

# Control de navegación entre páginas
if st.session_state['page'] == 'pagina_principal':
    pagina_principal()
elif st.session_state['page'] == 'segunda_pagina':
    segunda_pagina()
