import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score, learning_curve
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, roc_auc_score, precision_recall_fscore_support, ConfusionMatrixDisplay
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
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
st.write("Descripción Básica de Datos")
st.write(datos_credito.describe())
st.write(datos_credito.info())

# Histograma de montos solicitados
st.write("Distribución de Monto Solicitado")
fig = plt.figure(figsize=(10, 6))
sns.histplot(datos_credito['Monto_Solicitado'], bins=30, kde=True)
plt.title('Distribución de Monto Solicitado')
plt.xlabel('Monto Solicitado')
plt.ylabel('Frecuencia')
st.pyplot(fig)

# Gráfico de dispersión de Monto Solicitado vs Monto Desembolsado
st.write("Monto Solicitado vs Monto Desembolsado")
fig = plt.figure(figsize=(10, 6))
sns.scatterplot(x='Monto_Solicitado', y='Monto_Desembolsado', data=datos_credito)
plt.title('Monto Solicitado vs Monto Desembolsado')
plt.xlabel('Monto Solicitado')
plt.ylabel('Monto Desembolsado')
st.pyplot(fig)

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
    'SVM': SVC(probability=True, random_state=42)  # Agregado SVM
}

# Entrenamiento y evaluación
for nombre, modelo in modelos.items():
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    y_prob = modelo.predict_proba(X_test)[:, 1] if nombre == 'Regresión Logística' else None
    
    st.write(f"Modelo: {nombre}")
    st.write("Matriz de Confusión:\n", confusion_matrix(y_test, y_pred))
    st.write("Reporte de Clasificación:\n", classification_report(y_test, y_pred))
    
    if nombre == 'Regresión Logística':
        # Curva ROC
        fpr, tpr, _ = roc_curve(y_test, y_prob, pos_label='Alto')
        auc = roc_auc_score(y_test, y_prob)
        fig = plt.figure(figsize=(10, 6))
        plt.plot(fpr, tpr, marker='.')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'Curva ROC (AUC = {auc:.2f})')
        st.pyplot(fig)

# Importancia de características para Random Forest
st.write("Importancia de Características del Modelo de Bosque Aleatorio")
rf_model = modelos['Bosque Aleatorio']
importancia = rf_model.feature_importances_
caracteristicas = X.columns
importancia_df = pd.DataFrame({'Característica': caracteristicas, 'Importancia': importancia})
importancia_df = importancia_df.sort_values(by='Importancia', ascending=False)

fig = plt.figure(figsize=(10, 6))
sns.barplot(x='Importancia', y='Característica', data=importancia_df)
plt.title('Importancia de Características en el Modelo de Bosque Aleatorio')
st.pyplot(fig)

# Optimización de Hiperparámetros con GridSearchCV
st.write("Optimización de Hiperparámetros con GridSearchCV")
param_grid = {
    'n_estimators': [50, 100, 150],
    'max_depth': [None, 10, 20, 30]
}
grid_search = GridSearchCV(estimator=RandomForestClassifier(random_state=42), param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)
st.write("Mejores parámetros para Random Forest:", grid_search.best_params_)

# Validación Cruzada
st.write("Validación Cruzada")
cv_scores = cross_val_score(LogisticRegression(max_iter=1000), X_scaled, y, cv=5)
st.write(f"Cross-Validation Scores (Regresión Logística): {cv_scores}")
st.write(f"Mean CV Score: {cv_scores.mean()}")

# Curva de Aprendizaje
st.write("Curva de Aprendizaje")
train_sizes, train_scores, test_scores = learning_curve(LogisticRegression(max_iter=1000), X_scaled, y, cv=5, n_jobs=-1, train_sizes=np.linspace(0.1, 1.0, 10))

fig, ax = plt.subplots()
ax.plot(train_sizes, np.mean(train_scores, axis=1), 'o-', color='r', label='Train Score')
ax.plot(train_sizes, np.mean(test_scores, axis=1), 'o-', color='g', label='Test Score')
ax.set_xlabel('Training Size')
ax.set_ylabel('Score')
ax.set_title('Curva de Aprendizaje')
ax.legend(loc='best')
st.pyplot(fig)

# Matriz de Confusión Normalizada
st.write("Matriz de Confusión Normalizada (Regresión Logística)")
cm = confusion_matrix(y_test, y_pred, normalize='true')
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=modelos['Regresión Logística'].classes_)
fig, ax = plt.subplots(figsize=(10, 6))
disp.plot(ax=ax, cmap=plt.cm.Blues)
plt.title('Matriz de Confusión Normalizada (Regresión Logística)')
st.pyplot(fig)

# Evaluación Adicional con Métricas de Clasificación
st.write("Evaluación Adicional (Regresión Logística)")
precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average='weighted')
st.write(f"Precisión Promedio: {precision}")
st.write(f"Recall Promedio: {recall}")
st.write(f"Puntuación F1 Promedio: {f1}")

# Análisis de Residuos (Solo si se usa regresión)
# residuos = y_test - y_pred
# fig = plt.figure(figsize=(10, 6))
# sns.histplot(residuos, bins=30, kde=True)
# plt.title('Distribución de Residuos')
# st.pyplot(fig)

# PCA
st.write("Análisis de Componentes Principales (PCA)")
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

fig = plt.figure(figsize=(10, 6))
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=y, palette='viridis')
plt.title('Análisis de Componentes Principales (PCA)')
st.pyplot(fig)

# Segmentación de Datos y Análisis de Clústeres
st.write("Segmentación de Datos con K-Means")
kmeans = KMeans(n_clusters=3, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

fig = plt.figure(figsize=(10, 6))
sns.scatterplot(x=X_scaled[:, 0], y=X_scaled[:, 1], hue=clusters, palette='viridis')
plt.title('Segmentación de Datos con K-Means')
st.pyplot(fig)
