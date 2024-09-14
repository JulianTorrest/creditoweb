import streamlit as st
import plotly.graph_objs as go
import pandas as pd
import numpy as np

# Generar datos dummy para postulantes
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

# Generar datos dummy para IES
def generar_datos_ies():
    np.random.seed(42)
    num_ies = 20
    data_ies = pd.DataFrame({
        'Nombre de Institución': np.random.choice(['IES 1', 'IES 2', 'IES 3', 'IES 4', 'IES 5', 'IES 6', 'IES 7', 'IES 8', 'IES 9', 'IES 10', 'IES 11', 'IES 12', 'IES 13', 'IES 14', 'IES 15', 'IES 16', 'IES 17', 'IES 18', 'IES 19', 'IES 20'], num_ies),
        'Modalidad': np.random.choice(['Presencial', 'Virtual', 'Híbrida'], num_ies),
        'Nivel de Estudios': np.random.choice(['Pregrado', 'Especialización', 'Maestría', 'Doctorado'], num_ies),
        'Renovaciones Realizadas': np.random.randint(0, 50, num_ies),
        'Renovaciones Requeridas': np.random.randint(0, 50, num_ies),
        'Deserciones': np.random.randint(0, 20, num_ies),
        'Suspensiones': np.random.randint(0, 20, num_ies),
        'Institución Pública o Privada': np.random.choice(['Pública', 'Privada'], num_ies)
    })
    return data_ies

# Función para el gráfico embudo de cantidad
def grafico_funnel_cantidad(data):
    total_postulantes = len(data)
    total_aprobados = len(data[data['Monto Aprobado'] > 0])
    total_legalizados = len(data[data['Monto Legalizado'] > 0])
    total_desembolsos = len(data[data['Monto Desembolsado'] > 0])

    etapas = ['Postulantes', 'Aprobados', 'Legalizados', 'Con Desembolso']
    valores = [total_postulantes, total_aprobados, total_legalizados, total_desembolsos]

    # Ajustar valores para evitar inconsistencias
    valores[1] = min(valores[1], valores[0])
    valores[2] = min(valores[2], valores[1])
    valores[3] = min(valores[3], valores[2])

    fig = go.Figure(go.Funnel(
        y=etapas,
        x=valores,
        textinfo="value+percent initial"
    ))

    fig.update_layout(title='Embudo de Cantidad')

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

    fig.update_layout(title='Embudo de Monto')

    return fig

# Función para el gráfico de distribución de ingreso mensual
def grafico_ingreso_mensual(data):
    bins = [0, 1000000, 3000000, 6000000, 9000000, 12000000, 15000000, 18000000, 21000000, 24000000, 27000000, 30000000, 120000000]
    labels = ['≤1M', '1M-3M', '3M-6M', '6M-9M', '9M-12M', '12M-15M', '15M-18M', '18M-21M', '21M-24M', '24M-27M', '27M-30M', '30M+']
    data['Ingreso Mensual (COP)'] = pd.cut(data['Ingreso Mensual'], bins=bins, labels=labels)
    ingreso_mensual = data['Ingreso Mensual (COP)'].value_counts().sort_index()

    fig = go.Figure(go.Bar(
        x=ingreso_mensual.index,
        y=ingreso_mensual.values
    ))

    fig.update_layout(title='Distribución del Ingreso Mensual',
                      xaxis_title='Ingreso Mensual',
                      yaxis_title='Número de Postulantes')

    return fig

# Función para el gráfico de distribución por estrato socioeconómico
def grafico_estrato_socioeconomico(data):
    estratos = data['Estrato Socioeconómico'].value_counts()

    fig = go.Figure(go.Bar(
        x=estratos.index,
        y=estratos.values
    ))

    fig.update_layout(title='Distribución por Estrato Socioeconómico',
                      xaxis_title='Estrato Socioeconómico',
                      yaxis_title='Número de Postulantes')

    return fig

# Función para el gráfico de distribución por sexo biológico
def grafico_sexo_biologico(data):
    sexos = data['Sexo Biológico'].value_counts()

    fig = go.Figure(go.Pie(
        labels=sexos.index,
        values=sexos.values,
        hole=0.3
    ))

    fig.update_layout(title='Distribución por Sexo Biológico')

    return fig

# Función para el gráfico de distribución por rango de edad
def grafico_rango_edad(data):
    rangos_edad = data['Rango de Edad'].value_counts()

    fig = go.Figure(go.Bar(
        x=rangos_edad.index,
        y=rangos_edad.values
    ))

    fig.update_layout(title='Distribución por Rango de Edad',
                      xaxis_title='Rango de Edad',
                      yaxis_title='Número de Postulantes')

    return fig

# Función para el gráfico de distribución por ubicación de residencia
def grafico_ubicacion_residencia(data):
    ubicaciones = data['Ubicación de Residencia'].value_counts()

    fig = go.Figure(go.Pie(
        labels=ubicaciones.index,
        values=ubicaciones.values,
        hole=0.3
    ))

    fig.update_layout(title='Distribución por Ubicación de Residencia')

    return fig

# Función para el gráfico de distribución por año de finalización del pregrado
def grafico_anio_finalizacion_pregrado(data):
    años = data['Año de Finalización del Pregrado'].value_counts().sort_index()

    fig = go.Figure(go.Bar(
        x=años.index,
        y=años.values
    ))

    fig.update_layout(title='Distribución por Año de Finalización del Pregrado',
                      xaxis_title='Año de Finalización',
                      yaxis_title='Número de Postulantes')

    return fig

# Función para el gráfico de distribución por área del conocimiento del título de pregrado
def grafico_area_conocimiento_pregrado(data):
    áreas = data['Área del Conocimiento (Pregrado)'].value_counts()

    fig = go.Figure(go.Bar(
        x=áreas.index,
        y=áreas.values
    ))

    fig.update_layout(title='Distribución por Área del Conocimiento del Título de Pregrado',
                      xaxis_title='Área del Conocimiento',
                      yaxis_title='Número de Postulantes')

    return fig

# Función para el gráfico de distribución por área del conocimiento de los programas a los cuales desean aplicar
def grafico_area_conocimiento_aplicacion(data):
    áreas = data['Área del Conocimiento (Aplicación)'].value_counts()

    fig = go.Figure(go.Bar(
        x=áreas.index,
        y=áreas.values
    ))

    fig.update_layout(title='Distribución por Área del Conocimiento de los Programas a los Cuales Desean Aplicar',
                      xaxis_title='Área del Conocimiento',
                      yaxis_title='Número de Postulantes')

    return fig

# Función para el gráfico de distribución por estado laboral
def grafico_estado_laboral(data):
    estados_laborales = data['Empleado, Desempleado o Independiente'].value_counts()

    fig = go.Figure(go.Pie(
        labels=estados_laborales.index,
        values=estados_laborales.values,
        hole=0.3
    ))

    fig.update_layout(title='Distribución por Estado Laboral')

    return fig

# Función para el gráfico de distribución por antigüedad del último empleo
def grafico_antiguedad_empleo(data):
    antigüedades = data['Antigüedad Último Empleo'].value_counts()

    fig = go.Figure(go.Bar(
        x=antigüedades.index,
        y=antigüedades.values
    ))

    fig.update_layout(title='Distribución por Antigüedad del Último Empleo',
                      xaxis_title='Antigüedad',
                      yaxis_title='Número de Postulantes')

    return fig

# Función para el gráfico de distribución por estado civil
def grafico_estado_civil(data):
    estados_civiles = data['Estado Civil'].value_counts()

    fig = go.Figure(go.Pie(
        labels=estados_civiles.index,
        values=estados_civiles.values,
        hole=0.3
    ))

    fig.update_layout(title='Distribución por Estado Civil')

    return fig

# Función para el gráfico de distribución por patrimonio
def grafico_patrimonio(data):
    patrimonios = data['Patrimonio (Rango)'].value_counts()

    fig = go.Figure(go.Bar(
        x=patrimonios.index,
        y=patrimonios.values
    ))

    fig.update_layout(title='Distribución por Patrimonio',
                      xaxis_title='Patrimonio',
                      yaxis_title='Número de Postulantes')

    return fig

# Función para el gráfico de cantidad de desembolsos requeridos vs periodos académicos
def grafico_cantidad_desembolsos_vs_periodos(data):
    desembolsos_vs_periodos = data.groupby('Periodo Académico')['Cantidad de Desembolsos Requeridos'].sum().reset_index()

    fig = go.Figure(go.Bar(
        x=desembolsos_vs_periodos['Periodo Académico'],
        y=desembolsos_vs_periodos['Cantidad de Desembolsos Requeridos']
    ))

    fig.update_layout(title='Cantidad de Desembolsos Requeridos vs Periodos Académicos',
                      xaxis_title='Periodo Académico',
                      yaxis_title='Cantidad de Desembolsos Requeridos')

    return fig

# Función para el gráfico de datos de IES
def grafico_datos_ies(data_ies):
    fig = go.Figure()

    # Gráfico de modalidades
    modalidad_counts = data_ies['Modalidad'].value_counts()
    fig.add_trace(go.Bar(
        x=modalidad_counts.index,
        y=modalidad_counts.values,
        name='Modalidad'
    ))

    # Gráfico de niveles de estudio
    nivel_estudios_counts = data_ies['Nivel de Estudios'].value_counts()
    fig.add_trace(go.Bar(
        x=nivel_estudios_counts.index,
        y=nivel_estudios_counts.values,
        name='Nivel de Estudios'
    ))

    fig.update_layout(title='Datos de Instituciones de Educación Superior (IES)',
                      xaxis_title='Categoría',
                      yaxis_title='Número de Instituciones')

    return fig

# Función para el gráfico de renovaciones realizadas vs requeridas
def grafico_renovaciones_vs_requeridas(data_ies):
    renovaciones = data_ies.groupby('Nombre de Institución').agg({
        'Renovaciones Realizadas': 'sum',
        'Renovaciones Requeridas': 'sum'
    }).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=renovaciones['Nombre de Institución'],
        y=renovaciones['Renovaciones Realizadas'],
        name='Renovaciones Realizadas'
    ))
    fig.add_trace(go.Bar(
        x=renovaciones['Nombre de Institución'],
        y=renovaciones['Renovaciones Requeridas'],
        name='Renovaciones Requeridas'
    ))

    fig.update_layout(title='Renovaciones Realizadas vs Requeridas',
                      xaxis_title='Institución',
                      yaxis_title='Cantidad')

    return fig

# Función principal
def main():
    st.title('Dashboard de Análisis de Postulantes e IES')

    data = generar_datos_dummy()
    data_ies = generar_datos_ies()

    # Gráfico del embudo de cantidad
    st.subheader('Embudo de Cantidad')
    fig_cantidad = grafico_funnel_cantidad(data)
    st.plotly_chart(fig_cantidad)

    # Gráfico del embudo de monto
    st.subheader('Embudo de Monto')
    fig_monto = grafico_funnel_monto(data)
    st.plotly_chart(fig_monto)

    # Gráfico de distribución de ingreso mensual
    st.subheader('Distribución del Ingreso Mensual')
    fig_ingreso_mensual = grafico_ingreso_mensual(data)
    st.plotly_chart(fig_ingreso_mensual)

    # Gráfico de distribución por estrato socioeconómico
    st.subheader('Distribución por Estrato Socioeconómico')
    fig_estrato_socioeconomico = grafico_estrato_socioeconomico(data)
    st.plotly_chart(fig_estrato_socioeconomico)

    # Gráfico de distribución por sexo biológico
    st.subheader('Distribución por Sexo Biológico')
    fig_sexo_biologico = grafico_sexo_biologico(data)
    st.plotly_chart(fig_sexo_biologico)

    # Gráfico de distribución por rango de edad
    st.subheader('Distribución por Rango de Edad')
    fig_rango_edad = grafico_rango_edad(data)
    st.plotly_chart(fig_rango_edad)

    # Gráfico de distribución por ubicación de residencia
    st.subheader('Distribución por Ubicación de Residencia')
    fig_ubicacion_residencia = grafico_ubicacion_residencia(data)
    st.plotly_chart(fig_ubicacion_residencia)

    # Gráfico de distribución por año de finalización del pregrado
    st.subheader('Distribución por Año de Finalización del Pregrado')
    fig_anio_finalizacion_pregrado = grafico_anio_finalizacion_pregrado(data)
    st.plotly_chart(fig_anio_finalizacion_pregrado)

    # Gráfico de distribución por área del conocimiento del título de pregrado
    st.subheader('Distribución por Área del Conocimiento del Título de Pregrado')
    fig_area_conocimiento_pregrado = grafico_area_conocimiento_pregrado(data)
    st.plotly_chart(fig_area_conocimiento_pregrado)

    # Gráfico de distribución por área del conocimiento de los programas a los cuales desean aplicar
    st.subheader('Distribución por Área del Conocimiento de los Programas a los Cuales Desean Aplicar')
    fig_area_conocimiento_aplicacion = grafico_area_conocimiento_aplicacion(data)
    st.plotly_chart(fig_area_conocimiento_aplicacion)

    # Gráfico de distribución por estado laboral
    st.subheader('Distribución por Estado Laboral')
    fig_estado_laboral = grafico_estado_laboral(data)
    st.plotly_chart(fig_estado_laboral)

    # Gráfico de distribución por antigüedad del último empleo
    st.subheader('Distribución por Antigüedad del Último Empleo')
    fig_antiguedad_empleo = grafico_antiguedad_empleo(data)
    st.plotly_chart(fig_antiguedad_empleo)

    # Gráfico de distribución por estado civil
    st.subheader('Distribución por Estado Civil')
    fig_estado_civil = grafico_estado_civil(data)
    st.plotly_chart(fig_estado_civil)

    # Gráfico de distribución por patrimonio
    st.subheader('Distribución por Patrimonio')
    fig_patrimonio = grafico_patrimonio(data)
    st.plotly_chart(fig_patrimonio)

    # Gráfico de cantidad de desembolsos requeridos vs periodos académicos
    st.subheader('Cantidad de Desembolsos Requeridos vs Periodos Académicos')
    fig_desembolsos_vs_periodos = grafico_cantidad_desembolsos_vs_periodos(data)
    st.plotly_chart(fig_desembolsos_vs_periodos)

    # Gráfico de datos de IES
    st.subheader('Datos de Instituciones de Educación Superior (IES)')
    fig_datos_ies = grafico_datos_ies(data_ies)
    st.plotly_chart(fig_datos_ies)

    # Gráfico de renovaciones realizadas vs requeridas
    st.subheader('Renovaciones Realizadas vs Requeridas')
    fig_renovaciones_vs_requeridas = grafico_renovaciones_vs_requeridas(data_ies)
    st.plotly_chart(fig_renovaciones_vs_requeridas)

if __name__ == "__main__":
    main()
