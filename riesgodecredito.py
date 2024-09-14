import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
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

# Descripción básica
st.subheader('Descripción Básica de Datos')
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
    'SVM': SVC(probability=True, random_state=42),
    'KNN': KNeighborsClassifier()
}

# Entrenamiento y evaluación
st.subheader('Evaluación de Modelos')
for nombre, modelo in modelos.items():
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    st.write(f"Modelo: {nombre}")
    st.write("Matriz de Confusión:\n", confusion_matrix(y_test, y_pred))
    st.write("Reporte de Clasificación:\n", classification_report(y_test, y_pred))

    # Curva ROC
    if nombre == 'Regresión Logística' or nombre == 'SVM':
        y_prob = modelo.predict_proba(X_test)[:,1] if nombre == 'Regresión Logística' else modelo.decision_function(X_test)
        fpr, tpr, _ = roc_curve(y_test, y_prob, pos_label='Alto')
        roc_auc = auc(fpr, tpr)

        fig_roc = plt.figure(figsize=(10, 6))
        plt.plot(fpr, tpr, color='darkorange', lw=2, label='Curva ROC (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('Tasa de Falsos Positivos')
        plt.ylabel('Tasa de Verdaderos Positivos')
        plt.title('Curva ROC')
        plt.legend(loc="lower right")
        st.pyplot(fig_roc)

# Optimización de hiperparámetros para RandomForestClassifier
param_grid = {
    'n_estimators': [50, 100, 150],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10]
}
grid_search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)
st.write("Mejores parámetros para RandomForestClassifier:", grid_search.best_params_)

# Clusterización
st.subheader('Clusterización con K-Means')
n_clusters = 3
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
datos_credito['Cluster'] = kmeans.fit_predict(X_scaled)

# Gráfico interactivo de la clusterización
fig_clusterizacion = px.scatter(datos_credito, x='Monto_Solicitado', y='Monto_Desembolsado', color='Cluster', title='Clusterización de Datos de Crédito')
st.plotly_chart(fig_clusterizacion)

# Análisis de importancia de características para RandomForestClassifier
importancias = modelos['Bosque Aleatorio'].feature_importances_
caracteristicas = X.columns
importancias_df = pd.DataFrame({'Característica': caracteristicas, 'Importancia': importancias})
importancias_df = importancias_df.sort_values(by='Importancia', ascending=False)

fig_importancia = plt.figure(figsize=(12, 8))
sns.barplot(x='Importancia', y='Característica', data=importancias_df)
plt.title('Importancia de Características')
st.pyplot(fig_importancia)

# Evaluación de modelos con validación cruzada
scores = cross_val_score(LogisticRegression(max_iter=1000), X_scaled, y, cv=5)
st.write("Puntuaciones de validación cruzada para Regresión Logística:", scores)
st.write("Media de puntuaciones:", scores.mean())

# Análisis de datos perturbados
datos_credito_perturbado = shuffle(datos_credito)
X_perturbado = datos_credito_perturbado.drop('Riesgo_Credito', axis=1)
y_perturbado = datos_credito_perturbado['Riesgo_Credito']

X_perturbado_scaled = scaler.transform(X_perturbado)
y_pred_perturbado = modelos['Regresión Logística'].predict(X_perturbado_scaled)
st.write("Reporte de Clasificación con Datos Perturbados:")
st.write(classification_report(y_perturbado, y_pred_perturbado))

