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

# Función para el gráfico de cantidad de postulantes, aprobados, legalizados y con desembolso
def grafico_cantidad_postulantes(data):
    cantidad_postulantes = len(data)
    cantidad_aprobados = data['Monto Aprobado'].apply(lambda x: x > 0).sum()
    cantidad_legalizados = data['Monto Legalizado'].apply(lambda x: x > 0).sum()
    cantidad_con_desembolso = data['Monto Desembolsado'].apply(lambda x: x > 0).sum()
    
    fig = go.Figure(go.Bar(
        x=['Postulantes Totales', 'Aprobados', 'Legalizados', 'Con Desembolso'],
        y=[cantidad_postulantes, cantidad_aprobados, cantidad_legalizados, cantidad_con_desembolso],
        marker_color=['lightblue', 'lightgreen', 'lightcoral', 'lightgoldenrodyellow']
    ))
    
    fig.update_layout(
        title='Cantidad de Postulantes y Estado de Desembolsos',
        xaxis_title='Categoría',
        yaxis_title='Cantidad',
        template='plotly_dark'
    )
    
    return fig

# Función para el gráfico embudo de cantidad
def grafico_funnel_cantidad(data):
    total_solicitudes = len(data)
    total_aprobados = len(data[data['Monto Aprobado'] > 0])
    total_legalizados = len(data[data['Monto Legalizado'] > 0])
    total_desembolsos = len(data[data['Monto Desembolsado'] > 0])

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
    monto_solicitado = data['Monto Solicitado'].sum()
    monto_aprobado = data['Monto Aprobado'].sum()
    monto_legalizado = data['Monto Legalizado'].sum()
    monto_desembolsado = data['Monto Desembolsado'].sum()

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
    data['Ingreso Mensual (COP)'] = pd.cut(data['Ingreso Mensual'], bins=bins, labels=labels)
    ingreso_mensual_dist = data['Ingreso Mensual (COP)'].value_counts().sort_index()

    fig = go.Figure(go.Bar(
        x=ingreso_mensual_dist.index,
        y=ingreso_mensual_dist.values,
        text=ingreso_mensual_dist.values,
        textposition='auto'
    ))

    fig.update_layout(title='Distribución de Ingreso Mensual', xaxis_title='Rango de Ingreso Mensual', yaxis_title='Número de Postulantes')

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


# Función para el gráfico de monto solicitado, aprobado, legalizado y desembolsado
def grafico_monto_solicitado(data):
    monto_solicitado = data['Monto Solicitado'].sum()
    monto_aprobado = data['Monto Aprobado'].sum()
    monto_legalizado = data['Monto Legalizado'].sum()
    monto_desembolsado = data['Monto Desembolsado'].sum()
    
    fig = go.Figure(go.Bar(
        x=['Monto Solicitado', 'Monto Aprobado', 'Monto Legalizado', 'Monto Desembolsado'],
        y=[monto_solicitado, monto_aprobado, monto_legalizado, monto_desembolsado],
        marker_color=['lightblue', 'lightgreen', 'lightcoral', 'lightgoldenrodyellow']
    ))
    
    fig.update_layout(
        title='Monto Solicitado, Aprobado, Legalizado y Desembolsado',
        xaxis_title='Categoría',
        yaxis_title='Monto',
        template='plotly_dark'
    )
    
    return fig

# Función para gráficos de información del postulante
def grafico_informacion_postulante(data, columna, title):
    dist = data[columna].value_counts()

    fig = go.Figure(go.Pie(
        labels=dist.index,
        values=dist.values,
        hole=0.3
    ))

    fig.update_layout(
        title=title,
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

# Función para el gráfico de modalidades de IES
def grafico_modalidad_ies(data_ies):
    modalidad_dist = data_ies['Modalidad'].value_counts()

    fig = go.Figure(go.Pie(
        labels=modalidad_dist.index,
        values=modalidad_dist.values,
        hole=0.3
    ))

    fig.update_layout(
        title='Modalidades de Instituciones de Educación Superior (IES)',
        template='plotly_dark'
    )

    return fig

# Función para el gráfico de nivel de estudios ofrecidos por IES
def grafico_nivel_estudios_ies(data_ies):
    nivel_estudios_dist = data_ies['Nivel de Estudios'].value_counts()

    fig = go.Figure(go.Pie(
        labels=nivel_estudios_dist.index,
        values=nivel_estudios_dist.values,
        hole=0.3
    ))

    fig.update_layout(
        title='Niveles de Estudios Ofrecidos por IES',
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
        y=data_ies_filtrado['Renovaciones Realizadas'],
        name='Renovaciones Realizadas',
        marker_color='mediumseagreen'
    ))
    fig.add_trace(go.Bar(
        x=data_ies_filtrado['Nombre de Institución'],
        y=data_ies_filtrado['Renovaciones Requeridas'],
        name='Renovaciones Requeridas',
        marker_color='orange'
    ))

    fig.update_layout(
        title='Renovaciones Realizadas vs Renovaciones Requeridas',
        xaxis_title='Nombre de Institución',
        yaxis_title='Número de Renovaciones',
        barmode='group',
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

# Cantidad de postulantes vs cantidad aprobados vs legalizados vs estudiantes con desembolso
st.subheader("Cantidad de Postulantes, Aprobados, Legalizados y Con Desembolso")
fig_cantidad_postulantes = grafico_cantidad_postulantes(data)
st.plotly_chart(fig_cantidad_postulantes)

# Monto solicitado vs monto aprobado vs monto legalizado vs monto desembolsado
st.subheader("Monto Solicitado, Aprobado, Legalizado y Desembolsado")
fig_monto_solicitado = grafico_monto_solicitado(data)
st.plotly_chart(fig_monto_solicitado)

st.header("Información del Postulante")

# Gráficos de información del postulante
st.subheader("Estrato Socioeconómico")
fig_estrato_socioeconomico = grafico_informacion_postulante(data, 'Estrato Socioeconómico', 'Distribución por Estrato Socioeconómico')
st.plotly_chart(fig_estrato_socioeconomico)

st.subheader("Sexo Biológico")
fig_sexo_biologico = grafico_informacion_postulante(data, 'Sexo Biológico', 'Distribución por Sexo Biológico')
st.plotly_chart(fig_sexo_biologico)

st.subheader("Rango de Edad")
fig_rango_edad = grafico_informacion_postulante(data, 'Rango de Edad', 'Distribución por Rango de Edad')
st.plotly_chart(fig_rango_edad)

st.subheader("Ubicación de Residencia")
fig_ubicacion_residencia = grafico_informacion_postulante(data, 'Ubicación de Residencia', 'Distribución por Ubicación de Residencia')
st.plotly_chart(fig_ubicacion_residencia)

st.subheader("Año de Finalización del Pregrado")
fig_ano_finalizacion = go.Figure(go.Histogram(
    x=data['Año de Finalización del Pregrado'],
    marker_color='lightcoral'
))
fig_ano_finalizacion.update_layout(
    title='Año de Finalización del Pregrado',
    xaxis_title='Año',
    yaxis_title='Cantidad',
    template='plotly_dark'
)
st.plotly_chart(fig_ano_finalizacion)

st.subheader("Área del Conocimiento del Título de Pregrado")
fig_area_conocimiento_pregrado = grafico_informacion_postulante(data, 'Área del Conocimiento (Pregrado)', 'Distribución por Área del Conocimiento del Título de Pregrado')
st.plotly_chart(fig_area_conocimiento_pregrado)

st.subheader("Áreas de Conocimiento de los Programas a los Cuales Desean Aplicar")
fig_area_conocimiento_aplicacion = grafico_informacion_postulante(data, 'Área del Conocimiento (Aplicación)', 'Distribución por Área de Conocimiento de Programas')
st.plotly_chart(fig_area_conocimiento_aplicacion)

st.subheader("Empleado, Desempleado o Independiente")
fig_empleo_estado = grafico_informacion_postulante(data, 'Empleado, Desempleado o Independiente', 'Distribución por Estado de Empleo')
st.plotly_chart(fig_empleo_estado)

st.subheader("Antigüedad de su Último Empleo")
fig_antiguedad_empleo = grafico_informacion_postulante(data, 'Antigüedad Último Empleo', 'Distribución por Antigüedad de Último Empleo')
st.plotly_chart(fig_antiguedad_empleo)

st.subheader("Ingreso Mensual del Postulante")
fig_ingreso_mensual = go.Figure(go.Histogram(
    x=data['Ingreso Mensual'],
    marker_color='lightseagreen'
))
fig_ingreso_mensual.update_layout(
    title='Ingreso Mensual del Postulante',
    xaxis_title='Ingreso Mensual',
    yaxis_title='Cantidad',
    template='plotly_dark'
)
st.plotly_chart(fig_ingreso_mensual)

st.subheader("Estado Civil")
fig_estado_civil = grafico_informacion_postulante(data, 'Estado Civil', 'Distribución por Estado Civil')
st.plotly_chart(fig_estado_civil)

st.subheader("Patrimonio (Rango)")
fig_patrimonio_rango = grafico_informacion_postulante(data, 'Patrimonio (Rango)', 'Distribución por Patrimonio (Rango)')
st.plotly_chart(fig_patrimonio_rango)

st.subheader("Cantidad de Desembolsos Requeridos vs Periodos Definidos del Programa Académico")
fig_desembolsos_periodos = grafico_desembolsos_periodos(data)
st.plotly_chart(fig_desembolsos_periodos)

st.header("Información de Instituciones de Educación Superior (IES)")

# Gráficos de IES
st.subheader("Modalidades de Instituciones de Educación Superior (IES)")
fig_modalidad_ies = grafico_modalidad_ies(data_ies)
st.plotly_chart(fig_modalidad_ies)

st.subheader("Niveles de Estudios Ofrecidos por IES")
fig_nivel_estudios_ies = grafico_nivel_estudios_ies(data_ies)
st.plotly_chart(fig_nivel_estudios_ies)

st.header("Renovaciones y Deserciones")

# Gráficos de renovaciones y deserciones
st.subheader("Renovaciones Realizadas vs Renovaciones Requeridas")
fig_renovaciones = grafico_renovaciones(data_ies)
st.plotly_chart(fig_renovaciones)

st.subheader("Deserciones y Suspensiones")
fig_deserciones_suspensiones = grafico_deserciones_suspensiones(data_ies)
st.plotly_chart(fig_deserciones_suspensiones)

