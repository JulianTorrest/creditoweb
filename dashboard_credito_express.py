import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

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

    aprobado = np.random.choice([True, False], num_solicitudes, p=[0.7, 0.3])
    legalizado = np.random.choice([True, False], num_solicitudes, p=[0.8, 0.2])
    desembolso = np.random.choice([True, False], num_solicitudes, p=[0.9, 0.1])
    
    monto_solicitado = np.random.randint(5000000, 80000000, num_solicitudes)
    monto_aprobado = monto_solicitado * np.random.uniform(0.7, 1, num_solicitudes)
    monto_legalizado = monto_aprobado * np.random.uniform(0.8, 1, num_solicitudes)
    monto_desembolsado = monto_legalizado * np.random.uniform(0.9, 1, num_solicitudes)

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
        'Cantidad de Desembolsos': desembolsos,
        'Aprobado': aprobado,
        'Legalizado': legalizado,
        'Desembolso': desembolso,
        'Monto Solicitado': monto_solicitado,
        'Monto Aprobado': monto_aprobado,
        'Monto Legalizado': monto_legalizado,
        'Monto Desembolsado': monto_desembolsado
    })

    return data

# Función para crear gráfico embudo para la cantidad de postulantes
def grafico_funnel_cantidad(data):
    total_solicitudes = len(data)
    total_aprobados = len(data[data['Aprobado']])
    total_legalizados = len(data[data['Legalizado']])
    total_desembolsos = len(data[data['Desembolso']])

    etapas = ['Postulantes', 'Aprobados', 'Legalizados', 'Desembolsos']
    valores = [total_solicitudes, total_aprobados, total_legalizados, total_desembolsos]

    fig = go.Figure(go.Funnel(
        y=etapas,
        x=valores,
        textinfo="value+percent initial"
    ))

    fig.update_layout(title='Cantidad de Postulantes → Aprobados → Legalizados → Desembolsos')

    return fig

# Función para crear gráfico embudo para el monto de desembolso
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

# Función para la página principal del dashboard
def pagina_principal():
    st.title("Dashboard - Créditos Educativos ICETEX")
    
    # Generar datos dummy
    num_solicitudes = 300
    data = generar_datos_dummy(num_solicitudes)
    
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
    
    # Ejemplo de gráfico de dispersión (ingreso vs. monto solicitado)
    st.subheader("Gráfico de Dispersión: Ingreso Mensual vs Monto Solicitado")
    fig_scatter = go.Figure()
    fig_scatter.add_trace(go.Scatter(
        x=data['Ingreso Mensual (COP)'],
        y=data['Monto Solicitado'],
        mode='markers',
        marker=dict(size=10, color='rgba(156, 165, 196, 0.95)', line=dict(width=2, color='rgba(156, 165, 196, 0.95)'))
    ))
    fig_scatter.update_layout(title='Ingreso Mensual vs Monto Solicitado', xaxis_title='Ingreso Mensual (COP)', yaxis_title='Monto Solicitado')
    st.plotly_chart(fig_scatter)
    
    # Botón para volver a la página principal
    if st.button("Volver a la página principal"):
        st.session_state['page'] = 'pagina_principal'

# Función principal
def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = 'pagina_principal'

    if st.session_state['page'] == 'pagina_principal':
        pagina_principal()
    elif st.session_state['page'] == 'segunda_pagina':
        segunda_pagina()
