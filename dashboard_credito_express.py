import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Función para generar datos dummy para el bloque general
def generar_datos_dummy(num_solicitudes=300):
    np.random.seed(1)  # Para reproducibilidad
    data = pd.DataFrame({
        'Postulante': [f'Postulante {i+1}' for i in range(num_solicitudes)],
        'Aprobado': np.random.choice([True, False], num_solicitudes),
        'Legalizado': np.random.choice([True, False], num_solicitudes),
        'Desembolso': np.random.choice([True, False], num_solicitudes),
        'Monto Solicitado (COP)': np.random.randint(1000000, 5000000, num_solicitudes),
        'Monto Aprobado (COP)': np.random.randint(1000000, 5000000, num_solicitudes),
        'Monto Legalizado (COP)': np.random.randint(1000000, 5000000, num_solicitudes),
        'Monto Desembolsado (COP)': np.random.randint(1000000, 5000000, num_solicitudes),
        'Estrato Socioeconómico': np.random.choice([1, 2, 3, 4, 5], num_solicitudes),
        'Sexo Biológico': np.random.choice(['Masculino', 'Femenino'], num_solicitudes),
        'Estado de Empleo': np.random.choice(['Empleado', 'Desempleado'], num_solicitudes),
        'Ingreso Mensual (COP)': np.random.randint(1000000, 6000000, num_solicitudes),
        'Rango de Edad': np.random.choice(['18-25', '26-35', '36-45', '46-60'], num_solicitudes),
        'Estado Civil': np.random.choice(['Soltero', 'Casado', 'Divorciado'], num_solicitudes),
        'Área del Conocimiento (Pregrado)': np.random.choice(['Ciencias Sociales', 'Ingeniería', 'Salud', 'Humanidades'], num_solicitudes),
        'Patrimonio (Rango)': np.random.choice(['Bajo', 'Medio', 'Alto'], num_solicitudes)
    })
    return data

# Función para generar datos dummy para el bloque IES
def generar_datos_ies(num_instituciones=20):
    np.random.seed(1)  # Para reproducibilidad
    modalidades = np.random.choice(['Presencial', 'Virtual', 'A Distancia'], num_instituciones)
    niveles_estudio = np.random.choice(['Especialización', 'Maestría', 'Doctorado', 'Especialidades Médicas'], num_instituciones)
    nombres_institucion = [f'Institución {i+1}' for i in range(num_instituciones)]
    tipo_institucion = np.random.choice(['Pública', 'Privada'], num_instituciones)
    renovaciones_requeridas = np.random.randint(5, 20, num_instituciones)
    renovaciones_realizadas = np.random.randint(0, 15, num_instituciones)
    estudiantes_renovaciones = np.random.randint(0, 100, num_instituciones)
    deserciones = np.random.randint(0, 10, num_instituciones)
    suspensiones = np.random.randint(0, 10, num_instituciones)

    data_ies = pd.DataFrame({
        'Modalidad': modalidades,
        'Nivel de Estudios': niveles_estudio,
        'Nombre de Institución': nombres_institucion,
        'Tipo de Institución': tipo_institucion,
        'Renovaciones Requeridas': renovaciones_requeridas,
        'Renovaciones Realizadas': renovaciones_realizadas,
        'Estudiantes con Renovaciones Desembolsadas': estudiantes_renovaciones,
        'Deserciones': deserciones,
        'Suspensiones': suspensiones
    })

    return data_ies

# Función para el gráfico embudo de cantidad
def grafico_funnel_cantidad(data):
    total_solicitudes = len(data)
    total_aprobados = len(data[data['Aprobado']])
    total_legalizados = len(data[data['Legalizado']])
    total_desembolsos = len(data[data['Desembolso']])

    etapas = ['Postulantes', 'Aprobados', 'Legalizados', 'Desembolsos']
    valores = [total_solicitudes, total_aprobados, total_legalizados, total_desembolsos]

    # Ajustar valores para evitar inconsistencias
    valores[1] = min(valores[1], valores[0])
    valores[2] = min(valores[2], valores[1])
    valores[3] = min(valores[3], valores[2])

    fig = go.Figure(go.Funnel(
        y=etapas,
        x=valores,
        textinfo="value+percent initial"
    ))

    fig.update_layout(title='Cantidad de Postulantes → Aprobados → Legalizados → Desembolsos')

    return fig

# Función para el gráfico embudo de monto
def grafico_funnel_monto(data):
    monto_solicitado = data['Monto Solicitado (COP)'].sum()
    monto_aprobado = data['Monto Aprobado (COP)'].sum()
    monto_legalizado = data['Monto Legalizado (COP)'].sum()
    monto_desembolsado = data['Monto Desembolsado (COP)'].sum()

    etapas = ['Monto Solicitado', 'Monto Aprobado', 'Monto Legalizado', 'Monto Desembolsado']
    valores = [monto_solicitado, monto_aprobado, monto_legalizado, monto_desembolsado]

    fig = go.Figure(go.Funnel(
        y=etapas,
        x=valores,
        textinfo="value+percent initial"
    ))

    fig.update_layout(title='Monto Solicitado → Monto Aprobado → Monto Legalizado → Monto Desembolsado')

    return fig

# Función para la página principal del dashboard
def pagina_principal():
    st.title("Dashboard - Créditos Educativos ICETEX")
    
    # Generar datos dummy
    num_solicitudes = 300
    data = generar_datos_dummy(num_solicitudes)
    
    # Datos para el bloque IES
    num_instituciones = 20
    data_ies = generar_datos_ies(num_instituciones)

    st.header("Bloque General")
    
    # Gráfico embudo para cantidad de postulantes, aprobados, legalizados y desembolsos
    st.subheader("Cantidad de Postulantes → Aprobados → Legalizados → Desembolsos")
    fig_funnel_cantidad = grafico_funnel_cantidad(data)
    st.plotly_chart(fig_funnel_cantidad)

    # Gráfico embudo para monto solicitado, aprobado, legalizado y desembolsado
    st.subheader("Monto Solicitado → Monto Aprobado → Monto Legalizado → Monto Desembolsado")
    fig_funnel_monto = grafico_funnel_monto(data)
    st.plotly_chart(fig_funnel_monto)
    
    st.header("Información del Postulante")
    
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
    
    # Gráficos del bloque IES
    st.header("Bloque IES")
    
    st.subheader("Modalidad de Estudio")
    st.bar_chart(data_ies['Modalidad'].value_counts())

    st.subheader("Nivel de Estudios Ofrecido")
    st.bar_chart(data_ies['Nivel de Estudios'].value_counts())

    st.subheader("Tipo de Institución")
    st.bar_chart(data_ies['Tipo de Institución'].value_counts())

    st.subheader("Renovaciones Realizadas vs Requeridas")
    renovaciones_data = pd.DataFrame({
        'Institución': data_ies['Nombre de Institución'],
        'Renovaciones Requeridas': data_ies['Renovaciones Requeridas'],
        'Renovaciones Realizadas': data_ies['Renovaciones Realizadas']
    })
    st.bar_chart(renovaciones_data.set_index('Institución'))

    st.subheader("Estudiantes con el Total de Renovaciones Desembolsadas")
    st.bar_chart(data_ies['Estudiantes con Renovaciones Desembolsadas'])
    
    st.subheader("Deserciones y Suspensiones")
    deserciones_suspensiones_data = pd.DataFrame({
        'Institución': data_ies['Nombre de Institución'],
        'Deserciones': data_ies['Deserciones'],
        'Suspensiones': data_ies['Suspensiones']
    })
    st.bar_chart(deserciones_suspensiones_data.set_index('Institución'))

# Ejecutar la aplicación de Streamlit
pagina_principal()

