import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Generación de datos dummy para propósitos demostrativos
def generar_datos_dummy():
    np.random.seed(0)
    n = 1000
    data = pd.DataFrame({
        'Periodo Académico': np.random.choice(['2023-I', '2023-II', '2024-I'], n),
        'Cantidad de Desembolsos Requeridos': np.random.randint(1, 10000, n),
        'Ingreso Mensual': np.random.randint(1300000, 20000000, n),
        'Estrato Socioeconómico': np.random.choice(['1', '2', '3', '4', '5','6'], n),
        'Sexo Biológico': np.random.choice(['Masculino', 'Femenino'], n),
        'Rango de Edad': np.random.choice(['18-24', '25-34', '35-44', '45-54', '55+'], n),
        'Ubicación de Residencia': np.random.choice(['Urbano', 'Rural'], n),
        'Año de Finalización del Pregrado': np.random.randint(2010, 2022, n),
        'Área del Conocimiento (Pregrado)': np.random.choice(['Ciencias Sociales', 'Ingeniería', 'Ciencias Naturales'], n),
        'Área del Conocimiento (Aplicación)': np.random.choice(['Economía', 'Tecnología', 'Salud'], n),
        'Estado de Empleo': np.random.choice(['Empleado', 'Desempleado', 'Independiente'], n),
        'Antigüedad del Último Empleo': np.random.randint(0, 10, n),
        'Estado Civil': np.random.choice(['Soltero', 'Casado', 'Divorciado'], n),
        'Patrimonio': np.random.randint(1300000, 500000000, n)
    })
    return data

def generar_datos_ies():
    np.random.seed(0)
    n = 10000
    data = pd.DataFrame({
        'Nombre de Institución': np.random.choice(['Universidad de los Andes', 'Universidad Nacional', 'Universidad Javeriana','Universidad del Rosario','Universidad Externado'], n),
        'Modalidad': np.random.choice(['Presencial', 'Virtual', 'Distancia'], n),
        'Nivel de Estudios': np.random.choice(['Pregrado', 'Maestría', 'Doctorado'], n),
        'Institución Pública o Privada': np.random.choice(['Pública', 'Privada'], n),
        'Deserciones': np.random.randint(1, 10000, n),
        'Suspensiones': np.random.randint(1, 10000, n)
    })
    return data

# Funciones para gráficos Página 1
def grafico_funnel_cantidad(data):
    fig = go.Figure()
    fig.add_trace(go.Funnel(
        y=['Postulantes', 'Aprobados', 'Rechazados'],
        x=[data.shape[0], data[data['Ingreso Mensual'] > 1000].shape[0], data[data['Ingreso Mensual'] <= 1000].shape[0]],
        name='Cantidad'
    ))
    fig.update_layout(title='Embudo de Cantidad')
    return fig

def grafico_funnel_monto(data):
    fig = go.Figure()
    fig.add_trace(go.Funnel(
        y=['Postulantes', 'Aprobados', 'Rechazados'],
        x=[data['Ingreso Mensual'].sum(), data[data['Ingreso Mensual'] > 1000]['Ingreso Mensual'].sum(), data[data['Ingreso Mensual'] <= 1000]['Ingreso Mensual'].sum()],
        name='Monto'
    ))
    fig.update_layout(title='Embudo de Monto')
    return fig

def grafico_ingreso_mensual(data):
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=data['Ingreso Mensual'],
        name='Ingreso Mensual'
    ))
    fig.update_layout(title='Distribución del Ingreso Mensual',
                      xaxis_title='Ingreso Mensual',
                      yaxis_title='Frecuencia')
    return fig

def grafico_estrato_socioeconomico(data):
    fig = go.Figure()
    estrato_counts = data['Estrato Socioeconómico'].value_counts()
    fig.add_trace(go.Pie(
        labels=estrato_counts.index,
        values=estrato_counts.values,
        name='Estrato Socioeconómico'
    ))
    fig.update_layout(title='Distribución por Estrato Socioeconómico')
    return fig

def grafico_sexo_biologico(data):
    fig = go.Figure()
    sexo_counts = data['Sexo Biológico'].value_counts()
    fig.add_trace(go.Pie(
        labels=sexo_counts.index,
        values=sexo_counts.values,
        name='Sexo Biológico'
    ))
    fig.update_layout(title='Distribución por Sexo Biológico')
    return fig

def grafico_rango_edad(data):
    fig = go.Figure()
    rango_counts = data['Rango de Edad'].value_counts()
    fig.add_trace(go.Pie(
        labels=rango_counts.index,
        values=rango_counts.values,
        name='Rango de Edad'
    ))
    fig.update_layout(title='Distribución por Rango de Edad')
    return fig

def grafico_ubicacion_residencia(data):
    fig = go.Figure()
    ubicacion_counts = data['Ubicación de Residencia'].value_counts()
    fig.add_trace(go.Pie(
        labels=ubicacion_counts.index,
        values=ubicacion_counts.values,
        name='Ubicación de Residencia'
    ))
    fig.update_layout(title='Distribución por Ubicación de Residencia')
    return fig

def grafico_anio_finalizacion_pregrado(data):
    fig = go.Figure()
    anio_counts = data['Año de Finalización del Pregrado'].value_counts().sort_index()
    fig.add_trace(go.Bar(
        x=anio_counts.index,
        y=anio_counts.values,
        name='Año de Finalización del Pregrado'
    ))
    fig.update_layout(title='Distribución por Año de Finalización del Pregrado',
                      xaxis_title='Año de Finalización',
                      yaxis_title='Cantidad')
    return fig

def grafico_area_conocimiento_pregrado(data):
    fig = go.Figure()
    area_counts = data['Área del Conocimiento (Pregrado)'].value_counts()
    fig.add_trace(go.Pie(
        labels=area_counts.index,
        values=area_counts.values,
        name='Área del Conocimiento (Pregrado)'
    ))
    fig.update_layout(title='Distribución por Área del Conocimiento (Pregrado)')
    return fig

def grafico_area_conocimiento_aplicacion(data):
    fig = go.Figure()
    area_counts = data['Área del Conocimiento (Aplicación)'].value_counts()
    fig.add_trace(go.Pie(
        labels=area_counts.index,
        values=area_counts.values,
        name='Área del Conocimiento (Aplicación)'
    ))
    fig.update_layout(title='Distribución por Área del Conocimiento (Aplicación)')
    return fig

def grafico_empleo_estado(data):
    fig = go.Figure()
    estado_counts = data['Estado de Empleo'].value_counts()
    fig.add_trace(go.Pie(
        labels=estado_counts.index,
        values=estado_counts.values,
        name='Estado de Empleo'
    ))
    fig.update_layout(title='Distribución por Estado de Empleo')
    return fig

def grafico_antiguedad_empleo(data):
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=data['Antigüedad del Último Empleo'],
        name='Antigüedad del Último Empleo'
    ))
    fig.update_layout(title='Distribución por Antigüedad del Último Empleo',
                      xaxis_title='Antigüedad (Años)',
                      yaxis_title='Frecuencia')
    return fig

def grafico_estado_civil(data):
    fig = go.Figure()
    estado_civil_counts = data['Estado Civil'].value_counts()
    fig.add_trace(go.Pie(
        labels=estado_civil_counts.index,
        values=estado_civil_counts.values,
        name='Estado Civil'
    ))
    fig.update_layout(title='Distribución por Estado Civil')
    return fig

def grafico_patrimonio(data):
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=data['Patrimonio'],
        name='Patrimonio'
    ))
    fig.update_layout(title='Distribución por Patrimonio',
                      xaxis_title='Patrimonio',
                      yaxis_title='Frecuencia')
    return fig

def grafico_desembolsos_vs_periodos(data):
    fig = go.Figure()
    periodos_counts = data.groupby('Periodo Académico')['Cantidad de Desembolsos Requeridos'].sum()
    fig.add_trace(go.Bar(
        x=periodos_counts.index,
        y=periodos_counts.values,
        name='Desembolsos Requeridos'
    ))
    fig.update_layout(title='Cantidad de Desembolsos Requeridos vs Periodos Académicos',
                      xaxis_title='Periodo Académico',
                      yaxis_title='Cantidad de Desembolsos Requeridos')
    return fig

# Funciones para gráficos Página 2
def grafico_modalidad_ies(data_ies):
    fig = go.Figure()
    modalidad_counts = data_ies['Modalidad'].value_counts()
    fig.add_trace(go.Pie(
        labels=modalidad_counts.index,
        values=modalidad_counts.values,
        name='Modalidad'
    ))
    fig.update_layout(title='Distribución por Modalidad')
    return fig

def grafico_nivel_estudios_ies(data_ies):
    fig = go.Figure()
    nivel_counts = data_ies['Nivel de Estudios'].value_counts()
    fig.add_trace(go.Pie(
        labels=nivel_counts.index,
        values=nivel_counts.values,
        name='Nivel de Estudios'
    ))
    fig.update_layout(title='Distribución por Nivel de Estudios')
    return fig

def grafico_publica_privada_ies(data_ies):
    fig = go.Figure()
    tipo_counts = data_ies['Institución Pública o Privada'].value_counts()
    fig.add_trace(go.Pie(
        labels=tipo_counts.index,
        values=tipo_counts.values,
        name='Tipo de Institución'
    ))
    fig.update_layout(title='Distribución por Tipo de Institución')
    return fig

def grafico_total_renovaciones(data_ies):
    fig = go.Figure()
    renovaciones_total = data_ies['Deserciones'] + data_ies['Suspensiones']
    fig.add_trace(go.Bar(
        x=data_ies['Nombre de Institución'],
        y=renovaciones_total,
        name='Total Renovaciones'
    ))
    fig.update_layout(title='Total de Renovaciones (Deserciones + Suspensiones)',
                      xaxis_title='Nombre de Institución',
                      yaxis_title='Total de Renovaciones')
    return fig

def grafico_deserciones_suspensiones(data_ies):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data_ies['Nombre de Institución'],
        y=data_ies['Deserciones'],
        name='Deserciones'
    ))
    fig.add_trace(go.Bar(
        x=data_ies['Nombre de Institución'],
        y=data_ies['Suspensiones'],
        name='Suspensiones'
    ))
    fig.update_layout(title='Deserciones y Suspensiones por Institución',
                      xaxis_title='Nombre de Institución',
                      yaxis_title='Monto Promedio',
                      barmode='group')
    return fig

# Página 1
def pagina1():
    st.title("Análisis de Datos - Página 1")

    st.header("Embudo de Cantidad y Monto")
    st.subheader("Embudo de Cantidad")
    data = generar_datos_dummy()
    fig_funnel_cantidad = grafico_funnel_cantidad(data)
    st.plotly_chart(fig_funnel_cantidad)

    st.subheader("Embudo de Monto")
    fig_funnel_monto = grafico_funnel_monto(data)
    st.plotly_chart(fig_funnel_monto)

    st.header("Distribución de Ingresos y Características Demográficas")
    st.subheader("Distribución del Ingreso Mensual")
    fig_ingreso_mensual = grafico_ingreso_mensual(data)
    st.plotly_chart(fig_ingreso_mensual)

    st.subheader("Distribución por Estrato Socioeconómico")
    fig_estrato_socioeconomico = grafico_estrato_socioeconomico(data)
    st.plotly_chart(fig_estrato_socioeconomico)

    st.subheader("Distribución por Sexo Biológico")
    fig_sexo_biologico = grafico_sexo_biologico(data)
    st.plotly_chart(fig_sexo_biologico)

    st.subheader("Distribución por Rango de Edad")
    fig_rango_edad = grafico_rango_edad(data)
    st.plotly_chart(fig_rango_edad)

    st.subheader("Distribución por Ubicación de Residencia")
    fig_ubicacion_residencia = grafico_ubicacion_residencia(data)
    st.plotly_chart(fig_ubicacion_residencia)

    st.subheader("Distribución por Año de Finalización del Pregrado")
    fig_anio_finalizacion_pregrado = grafico_anio_finalizacion_pregrado(data)
    st.plotly_chart(fig_anio_finalizacion_pregrado)

    st.subheader("Distribución por Área del Conocimiento (Pregrado)")
    fig_area_conocimiento_pregrado = grafico_area_conocimiento_pregrado(data)
    st.plotly_chart(fig_area_conocimiento_pregrado)

    st.subheader("Distribución por Área del Conocimiento (Aplicación)")
    fig_area_conocimiento_aplicacion = grafico_area_conocimiento_aplicacion(data)
    st.plotly_chart(fig_area_conocimiento_aplicacion)

    st.subheader("Distribución por Estado de Empleo")
    fig_empleo_estado = grafico_empleo_estado(data)
    st.plotly_chart(fig_empleo_estado)

    st.subheader("Distribución por Antigüedad del Último Empleo")
    fig_antiguedad_empleo = grafico_antiguedad_empleo(data)
    st.plotly_chart(fig_antiguedad_empleo)

    st.subheader("Distribución por Estado Civil")
    fig_estado_civil = grafico_estado_civil(data)
    st.plotly_chart(fig_estado_civil)

    st.subheader("Distribución por Patrimonio")
    fig_patrimonio = grafico_patrimonio(data)
    st.plotly_chart(fig_patrimonio)

    st.header("Desembolsos Requeridos por Período Académico")
    fig_desembolsos_vs_periodos = grafico_desembolsos_vs_periodos(data)
    st.plotly_chart(fig_desembolsos_vs_periodos)

    st.header("Datos de Instituciones de Educación Superior (IES)")
    data_ies = generar_datos_ies()

    st.subheader("Distribución por Modalidad")
    fig_modalidad_ies = grafico_modalidad_ies(data_ies)
    st.plotly_chart(fig_modalidad_ies)

    st.subheader("Distribución por Nivel de Estudios")
    fig_nivel_estudios_ies = grafico_nivel_estudios_ies(data_ies)
    st.plotly_chart(fig_nivel_estudios_ies)

    st.subheader("Distribución por Institución Pública o Privada")
    fig_publica_privada_ies = grafico_publica_privada_ies(data_ies)
    st.plotly_chart(fig_publica_privada_ies)

    st.subheader("Total de Renovaciones (Deserciones + Suspensiones)")
    fig_total_renovaciones = grafico_total_renovaciones(data_ies)
    st.plotly_chart(fig_total_renovaciones)

    st.subheader("Deserciones y Suspensiones por Institución")
    fig_deserciones_suspensiones = grafico_deserciones_suspensiones(data_ies)
    st.plotly_chart(fig_deserciones_suspensiones)

# Ejecutar la aplicación
if __name__ == "__main__":
    main()




