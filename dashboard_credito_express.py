import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px


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
        'Ingreso Mensual': np.random.randint(1300000, 20000000, size=n),
        'Estado Civil': np.random.choice(['Soltero', 'Casado', 'Divorciado', 'Viudo'], n),
        'Patrimonio (Rango)': np.random.choice(['<4000000', '4000000-12000000', '12000000-20000000', '>20000000'], n),
        'Periodo Académico': np.random.choice(['2023-1', '2023-2', '2024-1', '2024-2'], n),
        'Cantidad de Desembolsos Requeridos': np.random.randint(1, 5, size=n),
        'Etapa': np.random.choice(['OTORGAMIENTO', 'ETAPA DE ESTUDIOS', 'ETAPA DE AMORTIZACIÓN', 'TRANSVERSALES'], n),
        'Estado': np.random.choice(['No pre-aprobado', 'Pre-aprobado', 'En estudio', 'Aprobado', 'No aprobado', 'Desistido', 
                                    'Legalizado', 'No legalizado', 'Girado', 'Pendiente de renovación', 'Renovación', 
                                    'Aplazado', 'Terminación de crédito', 'Pendiente paso a cobro', 'Novedad cartera', 
                                    'En amortización', 'Cancelado', 'Bloqueado', 'Anulado'], n),
        'Cantidad': np.random.randint(50, 300, size=n)
    })

    return data

# Definir etapas y estados válidos
etapas_estados_validos = {
    'OTORGAMIENTO': ['No pre-aprobado', 'Pre-aprobado', 'En estudio', 'Aprobado', 'No aprobado', 'Desistido', 'Legalizado', 'No legalizado'],
    'ETAPA DE ESTUDIOS': ['Girado', 'Pendiente de renovación', 'Renovación', 'Aplazado', 'Terminación de crédito'],
    'ETAPA DE AMORTIZACIÓN': ['Pendiente paso a cobro', 'Novedad cartera', 'En amortización', 'Cancelado'],
    'TRANSVERSALES': ['Bloqueado', 'Anulado']
}

# Filtrar combinaciones válidas
def filtrar_combinaciones_validas(data, etapas_estados_validos):
    df_filtrado = pd.DataFrame()
    for etapa, estados in etapas_estados_validos.items():
        df_filtrado = pd.concat([df_filtrado, data[(data['Etapa'] == etapa) & (data['Estado'].isin(estados))]])
    return df_filtrado

# Generar los datos dummy
data = generar_datos_dummy()

# Filtrar combinaciones válidas
data_filtrada = filtrar_combinaciones_validas(data, etapas_estados_validos)

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
        'Renovaciones Requeridas': np.random.randint(1, 100, size=n),
        'Total Renovaciones Desembolsadas': np.random.randint(1, 100, size=n),
        'Deserciones': np.random.randint(1, 50, size=n),
        'Suspensiones': np.random.randint(1, 50, size=n)
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

# Función para el gráfico de modalidad
def grafico_modalidad(data_ies):
    fig = go.Figure()
    modalidad_counts = data_ies['Modalidad'].value_counts()
    fig.add_trace(go.Pie(
        labels=modalidad_counts.index,
        values=modalidad_counts.values,
        name='Modalidad'
    ))
    fig.update_layout(title='Distribución por Modalidad')
    return fig

# Función para el gráfico de nivel de estudios
def grafico_nivel_estudios(data_ies):
    fig = go.Figure()
    nivel_counts = data_ies['Nivel de Estudios'].value_counts()
    fig.add_trace(go.Bar(
        x=nivel_counts.index,
        y=nivel_counts.values,
        name='Nivel de Estudios'
    ))
    fig.update_layout(title='Distribución por Nivel de Estudios',
                      xaxis_title='Nivel de Estudios',
                      yaxis_title='Cantidad')
    return fig

# Función para el gráfico de institución pública vs privada
def grafico_institucion_publica_privada(data_ies):
    fig = go.Figure()
    institucion_counts = data_ies['Institución Pública o Privada'].value_counts()
    fig.add_trace(go.Pie(
        labels=institucion_counts.index,
        values=institucion_counts.values,
        name='Institución Pública o Privada'
    ))
    fig.update_layout(title='Distribución por Tipo de Institución')
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

# Función para el gráfico de total de renovaciones desembolsadas
def grafico_total_renovaciones_desembolsadas(data_ies):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data_ies['Nombre de Institución'],
        y=data_ies['Total Renovaciones Desembolsadas'],
        name='Total Renovaciones Desembolsadas'
    ))
    fig.update_layout(title='Total de Renovaciones Desembolsadas',
                      xaxis_title='Nombre de Institución',
                      yaxis_title='Monto Total')
    return fig

# Función para el gráfico de deserciones y suspensiones
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
    fig.update_layout(title='Deserciones y Suspensiones',
                      xaxis_title='Nombre de Institución',
                      yaxis_title='Número',
                      barmode='group')
    return fig

# Función para el gráfico de nombre de la institución
def grafico_nombre_institucion(data_ies):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=data_ies['Nombre de Institución'],
        y=data_ies['Renovaciones Realizadas'],
        name='Renovaciones Realizadas'
    ))
    fig.update_layout(title='Nombre de la Institución vs Renovaciones Realizadas',
                      xaxis_title='Nombre de Institución',
                      yaxis_title='Número de Renovaciones')
    return fig

# Función principal de Streamlit
def main():
    st.title('Dashboard de Datos de Postulantes')

    data = generar_datos_dummy()
    datos_ies = generar_datos_ies()

    # Filtros para el DataFrame `data`
    st.sidebar.header('Filtros de Postulantes')
    estrato_socioeconomico = st.sidebar.multiselect('Estrato Socioeconómico', options=data['Estrato Socioeconómico'].unique(), default=data['Estrato Socioeconómico'].unique())
    sexo_biologico = st.sidebar.multiselect('Sexo Biológico', options=data['Sexo Biológico'].unique(), default=data['Sexo Biológico'].unique())
    rango_edad = st.sidebar.multiselect('Rango de Edad', options=data['Rango de Edad'].unique(), default=data['Rango de Edad'].unique())
    ubicacion_residencia = st.sidebar.multiselect('Ubicación de Residencia', options=data['Ubicación de Residencia'].unique(), default=data['Ubicación de Residencia'].unique())
    area_conocimiento_pregrado = st.sidebar.multiselect('Área del Conocimiento (Pregrado)', options=data['Área del Conocimiento (Pregrado)'].unique(), default=data['Área del Conocimiento (Pregrado)'].unique())
    area_conocimiento_aplicacion = st.sidebar.multiselect('Área del Conocimiento (Aplicación)', options=data['Área del Conocimiento (Aplicación)'].unique(), default=data['Área del Conocimiento (Aplicación)'].unique())
    periodo_academico = st.sidebar.multiselect('Periodo Académico', options=data['Periodo Académico'].unique(), default=data['Periodo Académico'].unique())
    
    # Aplicar filtros
    filtered_data = data[
        (data['Estrato Socioeconómico'].isin(estrato_socioeconomico)) &
        (data['Sexo Biológico'].isin(sexo_biologico)) &
        (data['Rango de Edad'].isin(rango_edad)) &
        (data['Ubicación de Residencia'].isin(ubicacion_residencia)) &
        (data['Área del Conocimiento (Pregrado)'].isin(area_conocimiento_pregrado)) &
        (data['Área del Conocimiento (Aplicación)'].isin(area_conocimiento_aplicacion)) &
        (data['Periodo Académico'].isin(periodo_academico))
    ]
    
    # Filtros para el DataFrame `datos_ies`
    st.sidebar.header('Filtros de IES')
    modalidad = st.sidebar.multiselect('Modalidad', options=datos_ies['Modalidad'].unique(), default=datos_ies['Modalidad'].unique())
    nivel_estudios = st.sidebar.multiselect('Nivel de Estudios', options=datos_ies['Nivel de Estudios'].unique(), default=datos_ies['Nivel de Estudios'].unique())
    institucion_publica_privada = st.sidebar.multiselect('Institución Pública o Privada', options=datos_ies['Institución Pública o Privada'].unique(), default=datos_ies['Institución Pública o Privada'].unique())
    
    # Aplicar filtros
    filtered_datos_ies = datos_ies[
        (datos_ies['Modalidad'].isin(modalidad)) &
        (datos_ies['Nivel de Estudios'].isin(nivel_estudios)) &
        (datos_ies['Institución Pública o Privada'].isin(institucion_publica_privada))
    ]

    # Gráficos para los postulantes
    st.header('Gráficos de Postulantes')

    st.subheader('1. Embudo de Cantidad')
    fig_cantidad = grafico_funnel_cantidad(data)
    st.plotly_chart(fig_cantidad)

    st.subheader('2. Embudo de Monto')
    fig_monto = grafico_funnel_monto(data)
    st.plotly_chart(fig_monto)

    # Gráfico de Área Separado por Etapa
    st.subheader('Gráfico de Área por Etapa')

    # Verificar si las columnas existen
    if all(col in data_filtrada.columns for col in ['Estado', 'Cantidad', 'Etapa']):
    # Obtener una lista de etapas únicas
        etapas = data_filtrada['Etapa'].unique()
    
    # Iterar sobre cada etapa y crear un gráfico
    for etapa in etapas:
        st.write(f'### {etapa}')
        
        # Filtrar datos para la etapa actual
        data_etapa = data_filtrada[data_filtrada['Etapa'] == etapa]
        
        # Crear gráfico de área usando Plotly
        fig = px.area(data_etapa, x='Estado', y='Cantidad', color='Etapa', title=f'Distribución de Cantidad por Estado - {etapa}')
        
        # Configurar la leyenda fuera del gráfico
        fig.update_layout(legend_title_text='', legend=dict(x=1, y=1))
        
        # Mostrar el gráfico
        st.plotly_chart(fig)
    else:
        st.error("Las columnas 'Estado', 'Cantidad' o 'Etapa' no están presentes en el DataFrame.")

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
    fig_renovaciones_vs_requeridas = grafico_renovaciones_vs_requeridas(datos_ies)
    st.plotly_chart(fig_renovaciones_vs_requeridas)

    st.subheader('17. Distribución por Modalidad')
    st.plotly_chart(grafico_modalidad(datos_ies))

    st.subheader('18. Distribución por Nivel de Estudios')
    st.plotly_chart(grafico_nivel_estudios(datos_ies))

    st.subheader('19. Distribución por Tipo de Institución (Pública vs Privada)')
    st.plotly_chart(grafico_institucion_publica_privada(datos_ies))

    st.subheader('20. Renovaciones Realizadas vs Requeridas')
    st.plotly_chart(grafico_renovaciones_vs_requeridas(datos_ies))

    st.subheader('21. Total de Renovaciones Desembolsadas')
    st.plotly_chart(grafico_total_renovaciones_desembolsadas(datos_ies))

    st.subheader('22. Deserciones y Suspensiones')
    st.plotly_chart(grafico_deserciones_suspensiones(datos_ies))

    st.subheader('23. Nombre de la Institución vs Renovaciones Realizadas')
    st.plotly_chart(grafico_nombre_institucion(datos_ies))

if __name__ == "__main__":
    main()
