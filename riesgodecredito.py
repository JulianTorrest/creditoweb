import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import classification_report, confusion_matrix
import streamlit as st

# Configurar la semilla para reproducibilidad
np.random.seed(42)
random.seed(42)

# Crear un DataFrame sintético
def generar_datos_credito(n=1000):
    data = pd.DataFrame({
        'Cantidad_Postulantes': np.random.randint(1, 100, n),
        'Cantidad_Aprobados': np.random.randint(0, 100, n),
        'Cantidad_Legalizados': np.random.randint(0, 100, n),
        'Cantidad_Desembolsos': np.random.randint(0, 100, n),
        'Monto_Solicitado': np.random.uniform(1000, 50000, n),
        'Monto_Aprobado': np.random.uniform(1000, 50000, n),
        'Monto_Legalizado': np.random.uniform(1000, 50000, n),
        'Monto_Desembolsado': np.random.uniform(1000, 50000, n),
        'Estrato_Socioeconomico': np.random.choice(['1', '2', '3', '4', '5'], n),
        'Sexo_Biologico': np.random.choice(['Masculino', 'Femenino'], n),
        'Rango_Edad': np.random.choice(['18-25', '26-35', '36-45', '46-55', '56+'], n),
        'Ubicacion_Residencia': np.random.choice(['Rural', 'Urbano'], n),
        'Ano_Finalizacion_Pregrado': np.random.randint(2000, 2024, n),
        'Area_Conocimiento_Pregrado': np.random.choice(['Ciencias Sociales', 'Ingeniería', 'Ciencias de la Salud', 'Artes', 'Ciencias Naturales'], n),
        'Areas_Conocimiento_Programas': np.random.choice(['Ingeniería', 'Ciencias Sociales', 'Ciencias de la Salud', 'Artes', 'Ciencias Naturales'], n),
        'Empleo_Status': np.random.choice(['Empleado', 'Desempleado', 'Independiente'], n),
        'Antiguedad_Ultimo_Empleo': np.random.randint(0, 20, n),
        'Ingreso_Mensual': np.random.uniform(500, 5000, n),
        'Estado_Civil': np.random.choice(['Soltero', 'Casado', 'Divorciado', 'Viudo'], n),
        'Patrimonio': np.random.choice(['Bajo', 'Medio', 'Alto'], n),
        'Cantidad_Desembolsos_Requeridos': np.random.randint(1, 10, n),
        'Modalidad_IES': np.random.choice(['Presencial', 'Virtual', 'A Distancia'], n),
        'Nivel_Estudios_IES': np.random.choice(['Especialización', 'Maestría', 'Doctorado', 'Especialidades Médicas'], n),
        'Nombre_IES': np.random.choice(['Universidad Nacional de Colombia', 'Universidad de los Andes', 'Universidad de Antioquia'], n),
        'IES_Publica_Privada': np.random.choice(['Pública', 'Privada'], n),
        'Renovaciones_Realizadas': np.random.randint(0, 50, n),
        'Renovaciones_Requeridas': np.random.randint(0, 50, n),
        'Total_Renovaciones_Desembolsadas': np.random.randint(0, 50, n),
        'Deserciones': np.random.randint(0, 20, n),
        'Suspensiones': np.random.randint(0, 20, n),
        'Riesgo_Credito': np.random.choice(['Alto', 'Medio', 'Bajo'], n)  # Variable objetivo
    })
    return data

datos_credito = generar_datos_credito()

# Configuración de Streamlit
st.title('Análisis de Riesgo de Crédito Educativo')

# Mostrar información básica
st.subheader('Descripción de los Datos')
st.write(datos_credito.describe())
st.write(datos_credito.info())

# Histograma de montos solicitados
st.subheader('Distribución de Monto Solicitado')
fig_histograma = plt.figure(figsize=(10, 6))
sns.histplot(datos_credito['Monto_Solicitado'], bins=30, kde=True)
plt.title('Distribución de Monto Solicitado')
plt.xlabel('Monto Solicitado')
plt.ylabel('Frecuencia')
st.pyplot(fig_histograma)

# Gráfico de dispersión de Monto Solicitado vs Monto Desembolsado
st.subheader('Monto Solicitado vs Monto Desembolsado')
fig_dispersion = plt.figure(figsize=(10, 6))
sns.scatterplot(x='Monto_Solicitado', y='Monto_Desembolsado', data=datos_credito)
plt.title('Monto Solicitado vs Monto Desembolsado')
plt.xlabel('Monto Solicitado')
plt.ylabel('Monto Desembolsado')
st.pyplot(fig_dispersion)

# Codificación de variables categóricas
label_encoders = {}
categorical_columns = ['Estrato_Socioeconomico', 'Sexo_Biologico', 'Rango_Edad', 'Ubicacion_Residencia',
                       'Area_Conocimiento_Pregrado', 'Areas_Conocimiento_Programas', 'Empleo_Status',
                       'Estado_Civil', 'Patrimonio', 'Modalidad_IES', 'Nivel_Estudios_IES', 'Nombre_IES', 'IES_Publica_Privada']

for col in categorical_columns:
    le = LabelEncoder()
    datos_credito[col] = le.fit_transform(datos_credito[col])
    label_encoders[col] = le

# Separar características y variable objetivo
X = datos_credito.drop('Riesgo_Credito', axis=1)
y = datos_credito['Riesgo_Credito']

# Normalización de datos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Dividir en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# Modelos
modelos = {
    'Regresión Logística': LogisticRegression(max_iter=1000),
    'Bosque Aleatorio': RandomForestClassifier(n_estimators=100, random_state=42),
    'SVM': SVC(),
    'KNN': KNeighborsClassifier()
}

# Entrenamiento y evaluación
st.subheader('Evaluación de Modelos')
for nombre, modelo in modelos.items():
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    st.write(f"Modelo: {nombre}")
    st.write("Matriz de Confusión:")
    st.write(confusion_matrix(y_test, y_pred))
    st.write("Reporte de Clasificación:")
    st.write(classification_report(y_test, y_pred))

# Pronóstico con Regresión Logística
st.subheader('Pronóstico de Riesgo de Crédito')
modelo_regresion_logistica = LogisticRegression(max_iter=1000)
modelo_regresion_logistica.fit(X_train, y_train)
y_pred_logistica = modelo_regresion_logistica.predict(X_test)
st.write("Pronósticos del Modelo de Regresión Logística:")
st.write(pd.DataFrame({'Actual': y_test, 'Predicción': y_pred_logistica}))

# Clusterización con K-Means
st.subheader('Clusterización con K-Means')
n_clusters = st.slider('Selecciona el número de clusters:', 2, 10, 3)
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
datos_credito_clusterizado = datos_credito.copy()
datos_credito_clusterizado['Cluster'] = kmeans.fit_predict(X_scaled)

# Gráfico interactivo de clusters
fig_clusters = px.scatter(datos_credito_clusterizado, x='Monto_Solicitado', y='Monto_Desembolsado', color='Cluster', title='Clusters de Riesgo de Crédito')
st.plotly_chart(fig_clusters)

# Gráfico interactivo del riesgo de crédito
st.subheader('Monto Solicitado por Riesgo de Crédito')
fig_histograma_interactivo = px.histogram(datos_credito, x='Monto_Solicitado', color='Riesgo_Credito', title='Monto Solicitado por Riesgo de Crédito')
st.plotly_chart(fig_histograma_interactivo)

# Gráfico interactivo de la distribución del riesgo de crédito por estrato socioeconómico
st.subheader('Monto Solicitado por Estrato Socioeconómico')
fig_estrato_socioeconomico = px.box(datos_credito, x='Estrato_Socioeconomico', y='Monto_Solicitado', color='Riesgo_Credito', title='Monto Solicitado por Estrato Socioeconómico')
st.plotly_chart(fig_estrato_socioeconomico)

