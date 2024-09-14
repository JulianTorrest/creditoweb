import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Función para generar datos dummy para postulantes
def generar_datos_dummy():
    np.random.seed(0)
    n = 1000
    data = pd.DataFrame({
        'Estrato Socioeconómico': np.random.choice(['1', '2', '3','4','5','6'], n),
        'Sexo Biológico': np.random.choice(['Masculino', 'Femenino'], n),
        'Rango de Edad': np.random.choice(['18-24', '25-34', '35-44', '45-54', '55-64', '65+'], n),
        'Ubicación de Residencia': np.random.choice(['Urbana', 'Rural'], n),
        'Año de Finalización del Pregrado': np.random.choice(range(2000, 2023), n),
        'Área del Conocimiento (Pregrado)': np.random.choice(['Ciencias Sociales', 'Ingeniería', 'Ciencias de la Salud', 'Ciencias Exactas', 'Humanidades'], n),
        'Área del Conocimiento (Aplicación)': np.random.choice(['Negocios', 'Tecnología', 'Salud', 'Educación', 'Ciencias'], n),
        'Empleado, Desempleado o Independiente': np.random.choice(['Empleado', 'Desempleado', 'Independiente'], n),
        'Antigüedad Último Empleo': np.random.choice(['<1 año', '1-3 años', '4-6 años', '7-10 años', '>10 años'], n),
        'Ingreso Mensual': np.random.randint(500, 5000, size=n),
        'Estado Civil': np.random.choice(['Soltero', 'Casado', 'Divorciado', 'Viudo'], n),
        'Patrimonio (Rango)': np.random.choice(['<10,000', '10,000-50,000', '50,000-100,000', '>100,000'], n),
        'Periodo Académico': np.random.choice(['2023-1', '2023-2', '2024-1', '2024-2'], n),
        'Cantidad de Desembolsos Requeridos': np.random.randint(1, 5, size=n)
    })
    return data

# Función para generar datos dummy para IES
def generar_datos_ies():
    np.random.seed(1)
    n = 10
    data_ies = pd.DataFrame({
        'Nombre de Institución': ['Universidad Nacional de Colombia', 'Universidad de los Andes', 'Universidad de Antioquia', 
                                  'Universidad del Rosario', 'Universidad Javeriana', 'Universidad del Norte',
                                  'Universidad de la Sabana', 'Universidad EAFIT', 'Universidad Externado de Colombia',
                                  'Universidad Industrial de Santander'],
        'Modalidad': np.random.choice(['Presencial', 'Virtual', 'A Distancia'], n),
        'Nivel de Estudios': np.random.choice(['Especialización', 'Maestría', 'Doctorado', 'Especialidades Médicas'], n),
        'Institución Pública o Privada': np.random.choice(['Pública', 'Privada'], n),
        'Renovaciones Realizadas': np.random.randint(1, 100, size=n),
        'Renovaciones Requeridas': np.random.randint(1, 100, size=n)
    })
    return data_ies

# Función para el gráfico de embudo de cantidad
def grafico_funnel_cantidad(data):
    cantidad_total = data.shape[0]
    
    cantidad_aprobados = int(cantidad_total * 0.8)
    cantidad_legalizados = int(cantidad_aprobados * 0.9)
    cantidad_desembolsos = int(cantidad_legalizados * 0.85)
    
    cantidad = {
        'Estado': ['Postulantes', 'Aprobados', 'Legalizados', 'Desembolsos'],
        'Cantidad': [cantidad_total, cantidad_aprobados, cantidad_legalizados, cantidad_desembolsos]
    }
    
    df_cantidad = pd.DataFrame(cantidad)

    fig = go.Figure()
    fig.add_trace(go.Funnel(
        y=df_cantidad['Estado'],
        x=df_cantidad['Cantidad'],
        textinfo='value'
    ))

    fig.update_layout(title='Embudo de Cantidad')

    return fig

# Función para el gráfico de embudo de monto
def grafico_funnel_monto(data):
    monto_solicitado = data['Ingreso Mensual'].sum()
    monto_aprobado = monto_solicitado * 0.8
    monto_legalizado = monto_aprobado * 0.9
    monto_desembolsado = monto_legalizado * 0.85

    monto = {
        'Estado': ['Monto Solicitado', 'Monto Aprobado', 'Monto Legalizado', 'Monto Desembolsado'],
        'Monto': [monto_solicitado, monto_aprobado, monto_legalizado, monto_desembolsado]
    }
    
    df_monto = pd.DataFrame(monto)

    fig = go.Figure()
    fig.add_trace(go.Funnel(
        y=df_monto['Estado'],
        x=df_monto['Monto'],
        textinfo='value'
    ))

    fig.update_layout(title='Embudo de Monto')

    return fig

# Función para el gráfico de renovaciones realizadas vs requeridas
def grafico_renovaciones_vs_requeridas(data_ies):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=data_ies['Nombre de Institución'],
        y=data_ies['Renovaciones Realizadas'],
        name='Renovaciones Realizadas'
    ))

    fig.add_trace(go.Bar(
        x=data_ies['Nombre de Institución'],
        y=data_ies['Renovaciones Requeridas'],
        name='Renovaciones Requeridas'
    ))

    fig.update_layout(title='Renovaciones Realizadas vs Requeridas',
                      xaxis_title='Nombre de Institución',
                      yaxis_title='Número de Renovaciones',
                      barmode='group')

    return fig

# Función para el gráfico de distribución del ingreso mensual
def grafico_ingreso_mensual(data):
    fig = go.Figure()

    fig.add_trace(go.Histogram(
        x=data['Ingreso Mensual'],
        nbinsx=20,
        name='Ingreso Mensual'
    ))

    fig.update_layout(title='Distribución del Ingreso Mensual',
                      xaxis_title='Ingreso Mensual',
                      yaxis_title='Frecuencia')

    return fig

# Función para el gráfico de distribución por estrato socioeconómico
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

# Función para el gráfico de distribución por sexo biológico
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

# Función para el gráfico de distribución por rango de edad
def grafico_rango_edad(data):
    fig = go.Figure()

    edad_counts = data['Rango de Edad'].value_counts()
    fig.add_trace(go.Bar(
        x=edad_counts.index,
        y=edad_counts.values,
        name='Rango de Edad'
    ))

    fig.update_layout(title='Distribución por Rango de Edad',
                      xaxis_title='Rango de Edad',
                      yaxis_title='Cantidad')

    return fig

# Función para el gráfico de distribución por ubicación de residencia
def grafico_ubicacion_residencia(data):
    fig = go.Figure()

    ubicacion_counts = data['Ubicación de Residencia'].value_counts()
    fig.add_trace(go.Bar(
        x=ubicacion_counts.index,
        y=ubicacion_counts.values,
        name='Ubicación de Residencia'
    ))

    fig.update_layout(title='Distribución por Ubicación de Residencia',
                      xaxis_title='Ubicación de Residencia',
                      yaxis_title='Cantidad')

    return fig

# Función para el gráfico de distribución por año de finalización del pregrado
def grafico_anio_finalizacion_pregrado(data):
    fig = go.Figure()

    anio_counts = data['Año de Finalización del Pregrado'].value_counts()
    fig.add_trace(go.Bar(
        x=anio_counts.index,
        y=anio_counts.values,
        name='Año de Finalización del Pregrado'
    ))

    fig.update_layout(title='Distribución por Año de Finalización del Pregrado',
                      xaxis_title='Año de Finalización del Pregrado',
                      yaxis_title='Cantidad')

    return fig

# Función para el gráfico de distribución por área del conocimiento (pregrado)
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

# Función para el gráfico de distribución por área del conocimiento (aplicación)
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

# Función para el gráfico de distribución por empleado, desempleado o independiente
def grafico_empleado_desempleado_independiente(data):
    fig = go.Figure()

    estado_counts = data['Empleado, Desempleado o Independiente'].value_counts()
    fig.add_trace(go.Pie(
        labels=estado_counts.index,
        values=estado_counts.values,
        name='Empleado, Desempleado o Independiente'
    ))

    fig.update_layout(title='Distribución por Estado Laboral')

    return fig

# Función para el gráfico de distribución por antigüedad en el último empleo
def grafico_antiguedad_ultimo_empleo(data):
    fig = go.Figure()

    antiguedad_counts = data['Antigüedad Último Empleo'].value_counts()
    fig.add_trace(go.Bar(
        x=antiguedad_counts.index,
        y=antiguedad_counts.values,
        name='Antigüedad Último Empleo'
    ))

    fig.update_layout(title='Distribución por Antigüedad en el Último Empleo',
                      xaxis_title='Antigüedad Último Empleo',
                      yaxis_title='Cantidad')

    return fig

# Función para el gráfico de distribución por estado civil
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

# Función para el gráfico de distribución por patrimonio
def grafico_patrimonio(data):
    fig = go.Figure()

    patrimonio_counts = data['Patrimonio (Rango)'].value_counts()
    fig.add_trace(go.Pie(
        labels=patrimonio_counts.index,
        values=patrimonio_counts.values,
        name='Patrimonio'
    ))

    fig.update_layout(title='Distribución por Patrimonio')

    return fig

# Función para el gráfico de cantidad de desembolsos requeridos por periodo académico
def grafico_desembolsos_periodo_academico(data):
    fig = go.Figure()

    desembolsos_counts = data.groupby('Periodo Académico')['Cantidad de Desembolsos Requeridos'].sum().reset_index()
    fig.add_trace(go.Bar(
        x=desembolsos_counts['Periodo Académico'],
        y=desembolsos_counts['Cantidad de Desembolsos Requeridos'],
        name='Cantidad de Desembolsos Requeridos'
    ))

    fig.update_layout(title='Cantidad de Desembolsos Requeridos por Periodo Académico',
                      xaxis_title='Periodo Académico',
                      yaxis_title='Cantidad de Desembolsos Requeridos')

    return fig

# Función principal de Streamlit
def main():
    st.title('Dashboard de Datos de Postulantes')

    data = generar_datos_dummy()
    data_ies = generar_datos_ies()

    # Gráficos para los postulantes
    st.header('Gráficos de Postulantes')

    st.subheader('1. Embudo de Cantidad')
    fig_cantidad = grafico_funnel_cantidad(data)
    st.plotly_chart(fig_cantidad)

    st.subheader('2. Embudo de Monto')
    fig_monto = grafico_funnel_monto(data)
    st.plotly_chart(fig_monto)

    st.subheader('3. Distribución del Ingreso Mensual')
    fig_ingreso_mensual = grafico_ingreso_mensual(data)
    st.plotly_chart(fig_ingreso_mensual)

    st.subheader('4. Distribución por Estrato Socioeconómico')
    fig_estrato_socioeconomico = grafico_estrato_socioeconomico(data)
    st.plotly_chart(fig_estrato_socioeconomico)

    st.subheader('5. Distribución por Sexo Biológico')
    fig_sexo_biologico = grafico_sexo_biologico(data)
    st.plotly_chart(fig_sexo_biologico)

    st.subheader('6. Distribución por Rango de Edad')
    fig_rango_edad = grafico_rango_edad(data)
    st.plotly_chart(fig_rango_edad)

    st.subheader('7. Distribución por Ubicación de Residencia')
    fig_ubicacion_residencia = grafico_ubicacion_residencia(data)
    st.plotly_chart(fig_ubicacion_residencia)

    st.subheader('8. Distribución por Año de Finalización del Pregrado')
    fig_anio_finalizacion_pregrado = grafico_anio_finalizacion_pregrado(data)
    st.plotly_chart(fig_anio_finalizacion_pregrado)

    st.subheader('9. Distribución por Área del Conocimiento (Pregrado)')
    fig_area_conocimiento_pregrado = grafico_area_conocimiento_pregrado(data)
    st.plotly_chart(fig_area_conocimiento_pregrado)

    st.subheader('10. Distribución por Área del Conocimiento (Aplicación)')
    fig_area_conocimiento_aplicacion = grafico_area_conocimiento_aplicacion(data)
    st.plotly_chart(fig_area_conocimiento_aplicacion)

    st.subheader('11. Distribución por Empleado, Desempleado o Independiente')
    fig_empleado_desempleado_independiente = grafico_empleado_desempleado_independiente(data)
    st.plotly_chart(fig_empleado_desempleado_independiente)

    st.subheader('12. Distribución por Antigüedad en el Último Empleo')
    fig_antiguedad_ultimo_empleo = grafico_antiguedad_ultimo_empleo(data)
    st.plotly_chart(fig_antiguedad_ultimo_empleo)

    st.subheader('13. Distribución por Estado Civil')
    fig_estado_civil = grafico_estado_civil(data)
    st.plotly_chart(fig_estado_civil)

    st.subheader('14. Distribución por Patrimonio')
    fig_patrimonio = grafico_patrimonio(data)
    st.plotly_chart(fig_patrimonio)

    st.subheader('15. Cantidad de Desembolsos Requeridos por Periodo Académico')
    fig_desembolsos_periodo_academico = grafico_desembolsos_periodo_academico(data)
    st.plotly_chart(fig_desembolsos_periodo_academico)

    # Gráficos para las instituciones educativas
    st.header('Gráficos de Instituciones Educativas')

    st.subheader('16. Renovaciones Realizadas vs Requeridas')
    fig_renovaciones_vs_requeridas = grafico_renovaciones_vs_requeridas(data_ies)
    st.plotly_chart(fig_renovaciones_vs_requeridas)

if __name__ == "__main__":
    main()
