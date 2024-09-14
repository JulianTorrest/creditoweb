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
        'Estado de Empleo': np.random.choice(['Empleado', 'Desempleado', 'Independiente'], num_solicitudes),
        'Ingreso Mensual (COP)': np.random.randint(1000000, 15000000, num_solicitudes),
        'Rango de Edad': np.random.choice(['18-25', '26-35', '36-45', '46-60'], num_solicitudes),
        'Estado Civil': np.random.choice(['Soltero', 'Casado', 'Divorciado'], num_solicitudes),
        'Área del Conocimiento (Pregrado)': np.random.choice(['Ciencias Sociales', 'Ingeniería', 'Salud', 'Humanidades'], num_solicitudes),
        'Patrimonio (Rango)': np.random.choice(['Bajo', 'Medio', 'Alto'], num_solicitudes),
        'Cantidad de Desembolsos Requeridos': np.random.randint(1, 10, num_solicitudes),
        'Periodo Académico': np.random.choice([f'Semestre {i+1}' for i in range(10)], num_solicitudes)
    })
    return data

# Función para generar datos dummy para el bloque IES
def generar_datos_ies(num_instituciones=20):
    np.random.seed(1)  # Para reproducibilidad
    universidades = [
        'Universidad Nacional de Colombia', 'Universidad de los Andes', 'Universidad Javeriana',
        'Universidad de Antioquia', 'Universidad del Rosario', 'Universidad EAFIT',
        'Universidad de la Sabana', 'Universidad de Cartagena', 'Universidad del Norte',
        'Universidad de San Buenaventura'
    ]
    modalidades = np.random.choice(['Presencial', 'Virtual', 'A Distancia'], num_instituciones)
    niveles_estudio = np.random.choice(['Especialización', 'Maestría', 'Doctorado', 'Especialidades Médicas'], num_instituciones)
    nombres_institucion = np.random.choice(universidades, num_instituciones)
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

# Función para el gráfico de distribución de ingreso mensual
def grafico_ingreso_mensual(data):
    bins = [0, 1000000, 3000000, 6000000, 9000000, 12000000, 15000000, 18000000, 21000000, 24000000, 27000000, 30000000, 120000000]
    labels = ['≤1M', '1M-3M', '3M-6M', '6M-9M', '9M-12M', '12M-15M', '15M-18M', '18M-21M', '21M-24M', '24M-27M', '27M-30M', '30M+']
    data['Ingreso Mensual (COP)'] = pd.cut(data['Ingreso Mensual (COP)'], bins=bins, labels=labels)
    ingreso_mensual_dist = data['Ingreso Mensual (COP)'].value_counts().sort_index()

    fig = go.Figure(go.Bar(
        x=ingreso_mensual_dist.index,
        y=ingreso_mensual_dist.values,
        text=ingreso_mensual_dist.values,
        textposition='auto'
    ))

    fig.update_layout(title='Distribución de Ingreso Mensual', xaxis_title='Rango de Ingreso Mensual', yaxis_title='Número de Postulantes')

    return fig

# Función para el gráfico de distribución por patrimonio
def grafico_patrimonio_rango(data):
    # Ajustar para manejar valores ficticios
    data['Patrimonio (Rango)'] = pd.Categorical(data['Patrimonio (Rango)'], categories=['Bajo', 'Medio', 'Alto'], ordered=True)
    patrimonio_dist = data['Patrimonio (Rango)'].value_counts().sort_index()

    fig = go.Figure(go.Bar(
        x=patrimonio_dist.index,
        y=patrimonio_dist.values,
        text=patrimonio_dist.values,
        textposition='auto'
    ))

    fig.update_layout(title='Distribución por Patrimonio (Rango)', xaxis_title='Rango de Patrimonio', yaxis_title='Número de Postulantes')

    return fig

# Función para el gráfico de cantidad de desembolsos requeridos vs periodos definidos
def grafico_desembolsos_periodos(data):
    periodos_definidos = [f'Semestre {i+1}' for i in range(10)]
    desembolsos_periodos = data[data['Periodo Académico'].isin(periodos_definidos)]
    cantidad_desembolsos_periodos = desembolsos_periodos.groupby('Periodo Académico')['Cantidad de Desembolsos Requeridos'].sum().reindex(periodos_definidos).fillna(0)

    fig = go.Figure(go.Bar(
        x=cantidad_desembolsos_periodos.index,
        y=cantidad_desembolsos_periodos.values,
        text=cantidad_desembolsos_periodos.values,
        textposition='auto'
    ))

    fig.update_layout(title='Cantidad de Desembolsos Requeridos vs Periodos Definidos del Programa Académico', xaxis_title='Periodo Académico', yaxis_title='Cantidad de Desembolsos Requeridos')

    return fig

# Función para el gráfico de renovaciones realizadas vs requeridas
def grafico_renovaciones(data_ies):
    universidades_principales = [
        'Universidad Nacional de Colombia', 'Universidad de los Andes', 'Universidad Javeriana',
        'Universidad de Antioquia', 'Universidad del Rosario', 'Universidad EAFIT',
        'Universidad de la Sabana', 'Universidad de Cartagena', 'Universidad del Norte',
        'Universidad de San Buenaventura'
    ]
    data_ies_filtrado = data_ies[data_ies['Nombre de Institución'].isin(universidades_principales)]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data_ies_filtrado['Nombre de Institución'],
        y=data_ies_filtrado['Renovaciones Requeridas'],
        name='Renovaciones Requeridas'
    ))
    fig.add_trace(go.Bar(
        x=data_ies_filtrado['Nombre de Institución'],
        y=data_ies_filtrado['Renovaciones Realizadas'],
        name='Renovaciones Realizadas'
    ))

    fig.update_layout(title='Renovaciones Realizadas vs Renovaciones Requeridas', barmode='group', xaxis_title='Nombre de Institución', yaxis_title='Cantidad')

    return fig

# Función para el gráfico de estudiantes con total de renovaciones desembolsadas
def grafico_estudiantes_renovaciones(data_ies):
    universidades_principales = [
        'Universidad Nacional de Colombia', 'Universidad de los Andes', 'Universidad Javeriana',
        'Universidad de Antioquia', 'Universidad del Rosario', 'Universidad EAFIT',
        'Universidad de la Sabana', 'Universidad de Cartagena', 'Universidad del Norte',
        'Universidad de San Buenaventura'
    ]
    data_ies_filtrado = data_ies[data_ies['Nombre de Institución'].isin(universidades_principales)]

    fig = go.Figure(go.Bar(
        x=data_ies_filtrado['Nombre de Institución'],
        y=data_ies_filtrado['Estudiantes con Renovaciones Desembolsadas'],
        text=data_ies_filtrado['Estudiantes con Renovaciones Desembolsadas'],
        textposition='auto'
    ))

    fig.update_layout(title='Estudiantes con Total de Renovaciones Desembolsadas', xaxis_title='Nombre de Institución', yaxis_title='Número de Estudiantes')

    return fig

# Función para el gráfico de deserciones y suspensiones
def grafico_deserciones_suspensiones(data_ies):
    universidades_principales = [
        'Universidad Nacional de Colombia', 'Universidad de los Andes', 'Universidad Javeriana',
        'Universidad de Antioquia', 'Universidad del Rosario', 'Universidad EAFIT',
        'Universidad de la Sabana', 'Universidad de Cartagena', 'Universidad del Norte',
        'Universidad de San Buenaventura'
    ]
    data_ies_filtrado = data_ies[data_ies['Nombre de Institución'].isin(universidades_principales)]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data_ies_filtrado['Nombre de Institución'],
        y=data_ies_filtrado['Deserciones'],
        name='Deserciones'
    ))
    fig.add_trace(go.Bar(
        x=data_ies_filtrado['Nombre de Institución'],
        y=data_ies_filtrado['Suspensiones'],
        name='Suspensiones'
    ))

    fig.update_layout(title='Deserciones y Suspensiones', barmode='group', xaxis_title='Nombre de Institución', yaxis_title='Número')

    return fig

# Función principal de la aplicación Streamlit
def pagina_principal():
    st.title('Dashboard de Convocatorias y Postulantes')

    # Cargar datos
    data = generar_datos_dummy()
    data_ies = generar_datos_ies()

    # Sección General
    st.header("Información de la Convocatoria")
    st.markdown("Consulta más información en [página de la convocatoria](http://example.com).")
    st.markdown("Cronograma de la convocatoria: Fechas de apertura y cierre.")

    st.subheader("Cantidad de Postulantes → Aprobados → Legalizados → Desembolsos")
    st.plotly_chart(grafico_funnel_cantidad(data))

    st.subheader("Monto Solicitado → Monto Aprobado → Monto Legalizado → Monto Desembolsado")
    st.plotly_chart(grafico_funnel_monto(data))

    st.subheader("Distribución de Ingreso Mensual")
    st.plotly_chart(grafico_ingreso_mensual(data))

    st.subheader("Distribución por Patrimonio (Rango)")
    st.plotly_chart(grafico_patrimonio_rango(data))

    st.subheader("Cantidad de Desembolsos Requeridos vs Periodos Definidos del Programa Académico")
    st.plotly_chart(grafico_desembolsos_periodos(data))

    # Sección Información del Postulante
    st.header("Información del Postulante")

    st.subheader("Distribución por Estrato Socioeconómico")
    st.bar_chart(data['Estrato Socioeconómico'].value_counts())

    st.subheader("Distribución por Sexo Biológico")
    st.bar_chart(data['Sexo Biológico'].value_counts())

    st.subheader("Distribución por Rango de Edad")
    st.bar_chart(data['Rango de Edad'].value_counts())

    st.subheader("Distribución por Área del Conocimiento del Título de Pregrado")
    st.bar_chart(data['Área del Conocimiento (Pregrado)'].value_counts())

    st.subheader("Distribución por Estado Civil")
    st.bar_chart(data['Estado Civil'].value_counts())

    st.subheader("Distribución por Patrimonio (Rango)")
    st.bar_chart(data['Patrimonio (Rango)'].value_counts())

    st.subheader("Cantidad de Desembolsos Requeridos vs Periodos Definidos del Programa Académico")
    cantidad_desembolsos_periodos = data.groupby('Periodo Académico')['Cantidad de Desembolsos Requeridos'].sum().reset_index()
    st.bar_chart(cantidad_desembolsos_periodos.set_index('Periodo Académico'))

    # Sección Información de las Instituciones de Educación Superior (IES)
    st.header("Información de las Instituciones de Educación Superior (IES)")

    st.subheader("Modalidad de la IES")
    st.bar_chart(data_ies['Modalidad'].value_counts())

    st.subheader("Nivel de Estudios Ofrecido")
    st.bar_chart(data_ies['Nivel de Estudios'].value_counts())

    st.subheader("Tipo de Institución")
    st.bar_chart(data_ies['Tipo de Institución'].value_counts())

    st.subheader("Renovaciones Realizadas vs Renovaciones Requeridas")
    st.plotly_chart(grafico_renovaciones(data_ies))

    st.subheader("Estudiantes con Total de Renovaciones Desembolsadas")
    st.plotly_chart(grafico_estudiantes_renovaciones(data_ies))

    st.subheader("Deserciones y Suspensiones")
    st.plotly_chart(grafico_deserciones_suspensiones(data_ies))

# Ejecutar la aplicación de Streamlit
pagina_principal()

