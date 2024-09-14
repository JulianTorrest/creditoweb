import streamlit as st
import plotly.graph_objs as go
import pandas as pd
import numpy as np

# Generar datos dummy para ejemplo
def generar_datos_dummy():
    np.random.seed(42)
    num_postulantes = 1000
    data = pd.DataFrame({
        'Estrato Socioeconómico': np.random.choice(['Estrato 1', 'Estrato 2', 'Estrato 3', 'Estrato 4', 'Estrato 5'], num_postulantes),
        'Sexo Biológico': np.random.choice(['Masculino', 'Femenino'], num_postulantes),
        'Rango de Edad': np.random.choice(['18-25', '26-35', '36-45', '46-55', '56+'], num_postulantes),
        'Ubicación de Residencia': np.random.choice(['Zona Urbana', 'Zona Rural'], num_postulantes),
        'Año de Finalización del Pregrado': np.random.choice(range(2010, 2021), num_postulantes),
        'Área del Conocimiento (Pregrado)': np.random.choice(['Ciencias Sociales', 'Ciencias Exactas', 'Ingeniería', 'Salud', 'Humanidades'], num_postulantes),
        'Área del Conocimiento (Aplicación)': np.random.choice(['Ciencias Sociales', 'Ciencias Exactas', 'Ingeniería', 'Salud', 'Humanidades'], num_postulantes),
        'Empleado, Desempleado o Independiente': np.random.choice(['Empleado', 'Desempleado', 'Independiente'], num_postulantes),
        'Antigüedad Último Empleo': np.random.choice(['Menos de 1 año', '1-3 años', '4-6 años', 'Más de 6 años'], num_postulantes),
        'Ingreso Mensual': np.random.randint(1000000, 120000000, num_postulantes),
        'Estado Civil': np.random.choice(['Soltero', 'Casado', 'Divorciado', 'Viudo'], num_postulantes),
        'Patrimonio (Rango)': np.random.choice(['Menos de 1M', '1M-3M', '3M-6M', '6M-10M', '10M-20M', '20M-50M', '50M-100M', '100M-120M', 'Más de 120M'], num_postulantes),
        'Cantidad de Desembolsos Requeridos': np.random.randint(1, 6, num_postulantes),
        'Periodo Académico': np.random.choice([f'Semestre {i+1}' for i in range(10)], num_postulantes),
        'Monto Solicitado': np.random.randint(1000000, 50000000, num_postulantes),
        'Monto Aprobado': np.random.randint(1000000, 50000000, num_postulantes),
        'Monto Legalizado': np.random.randint(1000000, 50000000, num_postulantes),
        'Monto Desembolsado': np.random.randint(1000000, 50000000, num_postulantes)
    })
    return data

# Datos ficticios para Instituciones de Educación Superior (IES)
def generar_datos_ies():
    universidades = [
        'Universidad Nacional de Colombia', 'Universidad de los Andes', 'Universidad Javeriana',
        'Universidad de Antioquia', 'Universidad del Rosario', 'Universidad EAFIT',
        'Universidad de la Sabana', 'Universidad de Cartagena', 'Universidad del Norte',
        'Universidad de San Buenaventura'
    ]
    num_ies = len(universidades)
    data = pd.DataFrame({
        'Nombre de Institución': np.random.choice(universidades, 100),
        'Modalidad': np.random.choice(['Presencial', 'Virtual', 'A Distancia'], 100),
        'Nivel de Estudios': np.random.choice(['Especialización', 'Maestría', 'Doctorado', 'Especialidades Médicas'], 100),
        'Tipo de Institución': np.random.choice(['Pública', 'Privada'], 100),
        'Renovaciones Realizadas': np.random.randint(0, 50, 100),
        'Renovaciones Requeridas': np.random.randint(0, 50, 100),
        'Estudiantes con Renovaciones Desembolsadas': np.random.randint(0, 50, 100),
        'Deserciones': np.random.randint(0, 10, 100),
        'Suspensiones': np.random.randint(0, 10, 100)
    })
    return data

# Función para el gráfico de distribución de ingreso mensual
def grafico_ingreso_mensual(data):
    bins = [0, 1000000, 3000000, 6000000, 9000000, 12000000, 15000000, 20000000, 50000000, 100000000, 120000000, float('inf')]
    labels = ['Menos de 1M', '1M-3M', '3M-6M', '6M-9M', '9M-12M', '12M-15M', '15M-20M', '20M-50M', '50M-100M', '100M-120M', 'Más de 120M']
    data['Ingreso Mensual Rango'] = pd.cut(data['Ingreso Mensual'], bins=bins, labels=labels, right=False)
    
    ingreso_dist = data['Ingreso Mensual Rango'].value_counts().sort_index()

    fig = go.Figure(go.Bar(
        x=ingreso_dist.index,
        y=ingreso_dist.values,
        text=ingreso_dist.values,
        textposition='auto',
        marker_color='royalblue'
    ))

    fig.update_layout(
        title='Distribución de Ingreso Mensual',
        xaxis_title='Rango de Ingreso Mensual',
        yaxis_title='Número de Postulantes',
        template='plotly_dark'
    )

    return fig

# Función para el gráfico de distribución por patrimonio
def grafico_patrimonio_rango(data):
    patrimonio_dist = data['Patrimonio (Rango)'].value_counts().sort_index()

    fig = go.Figure(go.Bar(
        x=patrimonio_dist.index,
        y=patrimonio_dist.values,
        text=patrimonio_dist.values,
        textposition='auto',
        marker_color='darkorange'
    ))

    fig.update_layout(
        title='Distribución por Patrimonio (Rango)',
        xaxis_title='Rango de Patrimonio',
        yaxis_title='Número de Postulantes',
        template='plotly_dark'
    )

    return fig

# Función para el gráfico de cantidad de desembolsos requeridos vs periodos definidos
def grafico_desembolsos_periodos(data):
    periodos_definidos = [f'Semestre {i+1}' for i in range(10)]
    desembolsos_periodos = data[data['Periodo Académico'].isin(periodos_definidos)]
    cantidad_desembolsos_periodos = desembolsos_periodos.groupby('Periodo Académico')['Cantidad de Desembolsos Requeridos'].sum().reindex(periodos_definidos).fillna(0)

    fig = go.Figure(go.Line(
        x=cantidad_desembolsos_periodos.index,
        y=cantidad_desembolsos_periodos.values,
        mode='lines+markers',
        line=dict(color='deepskyblue', width=2),
        marker=dict(color='darkblue', size=8)
    ))

    fig.update_layout(
        title='Cantidad de Desembolsos Requeridos vs Periodos Definidos del Programa Académico',
        xaxis_title='Periodo Académico',
        yaxis_title='Cantidad de Desembolsos Requeridos',
        template='plotly_dark'
    )

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
        name='Renovaciones Requeridas',
        marker_color='lightcoral'
    ))
    fig.add_trace(go.Bar(
        x=data_ies_filtrado['Nombre de Institución'],
        y=data_ies_filtrado['Renovaciones Realizadas'],
        name='Renovaciones Realizadas',
        marker_color='limegreen'
    ))

    fig.update_layout(
        title='Renovaciones Realizadas vs Renovaciones Requeridas',
        xaxis_title='Nombre de Institución',
        yaxis_title='Número de Renovaciones',
        barmode='group',
        template='plotly_dark'
    )

    return fig

# Función para el gráfico de estudiantes con total de renovaciones desembolsadas
def grafico_renovaciones_desembolsadas(data_ies):
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
        textposition='auto',
        marker_color='mediumseagreen'
    ))

    fig.update_layout(
        title='Estudiantes con Total de Renovaciones Desembolsadas',
        xaxis_title='Nombre de Institución',
        yaxis_title='Número de Estudiantes',
        template='plotly_dark'
    )

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
        name='Deserciones',
        marker_color='orangered'
    ))
    fig.add_trace(go.Bar(
        x=data_ies_filtrado['Nombre de Institución'],
        y=data_ies_filtrado['Suspensiones'],
        name='Suspensiones',
        marker_color='gold'
    ))

    fig.update_layout(
        title='Deserciones y Suspensiones',
        xaxis_title='Nombre de Institución',
        yaxis_title='Número de Casos',
        barmode='group',
        template='plotly_dark'
    )

    return fig

# Página principal de Streamlit
st.title("Dashboard de Convocatorias y Estudiantes")

# Cargar datos
data = generar_datos_dummy()
data_ies = generar_datos_ies()

st.header("Información General")

# Monto solicitado vs monto aprobado vs monto legalizado vs monto desembolsado
st.subheader("Monto Solicitado, Aprobado, Legalizado y Desembolsado")
monto_solicitado = data['Monto Solicitado'].sum()
monto_aprobado = data['Monto Aprobado'].sum()
monto_legalizado = data['Monto Legalizado'].sum()
monto_desembolsado = data['Monto Desembolsado'].sum()

st.write(f"Monto Solicitado: ${monto_solicitado:,.0f}")
st.write(f"Monto Aprobado: ${monto_aprobado:,.0f}")
st.write(f"Monto Legalizado: ${monto_legalizado:,.0f}")
st.write(f"Monto Desembolsado: ${monto_desembolsado:,.0f}")

st.header("Gráficos de Datos")

st.subheader("Distribución de Ingreso Mensual")
fig_ingreso_mensual = grafico_ingreso_mensual(data)
st.plotly_chart(fig_ingreso_mensual)

st.subheader("Distribución por Patrimonio (Rango)")
fig_patrimonio_rango = grafico_patrimonio_rango(data)
st.plotly_chart(fig_patrimonio_rango)

st.subheader("Cantidad de Desembolsos Requeridos vs Periodos Definidos del Programa Académico")
fig_desembolsos_periodos = grafico_desembolsos_periodos(data)
st.plotly_chart(fig_desembolsos_periodos)

st.subheader("Renovaciones Realizadas vs Renovaciones Requeridas")
fig_renovaciones = grafico_renovaciones(data_ies)
st.plotly_chart(fig_renovaciones)

st.subheader("Estudiantes con Total de Renovaciones Desembolsadas")
fig_renovaciones_desembolsadas = grafico_renovaciones_desembolsadas(data_ies)
st.plotly_chart(fig_renovaciones_desembolsadas)

st.subheader("Deserciones y Suspensiones")
fig_deserciones_suspensiones = grafico_deserciones_suspensiones(data_ies)
st.plotly_chart(fig_deserciones_suspensiones)


