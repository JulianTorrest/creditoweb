import streamlit as st
import pandas as pd
import random
import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from datetime import datetime,timedelta  # Importación directa de datetime
import seaborn as sns
from fpdf import FPDF
import io
from io import BytesIO
import xlsxwriter
import base64
import tempfile
import csv

# Crear una función para generar datos ficticios
def generar_datos_ficticios(n):
    nombres = [f"Nombre_{i}" for i in range(n)]
    estados_credito = ["Ninguno", "Castigado", "En mora y castigado"]
    listas_sarlaft = ["No está en ninguna lista", "Vinculantes", "Restrictivas", "Informativas"]
    
    datos = []
    for nombre in nombres:
        # Generar una fecha aleatoria en los últimos 10 años
        fecha_random = datetime.now() - timedelta(days=random.randint(0, 3650))
        # Extraer año y mes
        año = fecha_random.year
        mes = fecha_random.month
        # Determinar periodo
        periodo = "1er Semestre" if mes <= 6 else "2do Semestre"
        
        datos.append({
            "Nombre": nombre,
            "Edad": random.randint(18, 65),
            "Estado Crédito": random.choice(estados_credito),
            "Lista SARLAFT": random.choice(listas_sarlaft),
            "Score Crediticio": random.randint(150, 900),
            "Capacidad de Pago (COP)": random.randint(1500000, 20000000),
            "Límite de Endeudamiento (COP)": random.randint(1500000, 20000000),
            "Fecha": fecha_random.strftime("%Y-%m-%d"),  # Convertir la fecha a formato de cadena
            "Año": año,
            "Mes": mes,
            "Periodo": periodo
        })
    return datos


    
# Inicializar datos
beneficiarios_data = generar_datos_ficticios(500)
if "ofertas_enviadas" not in st.session_state:
    st.session_state.ofertas_enviadas = []
if "ofertas_en_proceso" not in st.session_state:
    st.session_state.ofertas_en_proceso = []

# Función para validar un deudor
def validar_deudor(deudor):
    # Asignar valor por defecto si el Estado de Crédito está vacío
    if 'Estado Crédito' not in deudor or not deudor['Estado Crédito']:
        deudor['Estado Crédito'] = 'Ninguno'  # Asignar 'Ninguno' si falta
    
    # Validar edad
    if deudor['Edad'] >= 65:
        return False, "Es mayor de 65 años"

    # Validar Estado de Crédito
    if deudor['Estado Crédito'] != 'Ninguno':
        return False, "Estado Crédito debe ser Ninguno"
    
    return True, ""  # Si pasa todas las validaciones

def validar_sarlaft(deudor):
    if deudor['Lista SARLAFT'] in ['Vinculantes', 'Restrictivas', 'Informativas']:
        return False, f"Listas SARLAFT: {deudor['Lista SARLAFT']}"
    return True, ""

def validar_antecedentes(deudor, fecha_antecedentes):
    if (datetime.now() - fecha_antecedentes).days < 90:
        return False, "Antecedentes menores a 90 días"
    return True, ""

def realizar_validaciones(deudor):
    errores = []
    
    # Verificar y asignar Estado de Crédito
    if 'Estado Crédito' not in deudor or not deudor['Estado Crédito']:
        deudor['Estado Crédito'] = 'Ninguno'  # Asegúrate de asignarlo aquí también

    # Validar score crediticio
    if deudor["Score Crediticio"] < 610:
        errores.append("El score crediticio debe ser de mínimo 610 puntos.")
    
    # Validar capacidad de pago
    if deudor["Capacidad de Pago (COP)"] < 3000000:
        errores.append("Capacidad de pago insuficiente.")
    
    return errores

# Procesar validaciones y estadísticas
def procesar_validaciones(beneficiarios):
    validaciones = {
        "Validación 1": {"Aprobados": 0, "No Aprobados": 0, "Motivo No Aprobación": []},
        "Validación 2": {"Aprobados": 0, "No Aprobados": 0},
        "Validación 3": {"Aprobados": 0, "No Aprobados": 0, "Motivo No Aprobación": []},
    }

    for deudor in beneficiarios.to_dict(orient='records'):
        # Verificar y asignar Estado de Crédito
        if 'Estado Crédito' not in deudor or not deudor['Estado Crédito']:
            deudor['Estado Crédito'] = 'Ninguno'  # Asegúrate de asignarlo aquí también

        # Validación 1
        valido1, motivo1 = validar_deudor(deudor)
        if valido1 and valido_nacionalidad:
            validaciones["Validación 1"]["Aprobados"] += 1
        else:
            validaciones["Validación 1"]["No Aprobados"] += 1
            validaciones["Validación 1"]["Motivo No Aprobación"].append(motivo1)

        # Validación 2
        valido2, motivo2 = validar_sarlaft(deudor)
        if valido2:
            validaciones["Validación 2"]["Aprobados"] += 1
        else:
            validaciones["Validación 2"]["No Aprobados"] += 1

        # Validación 3
        fecha_antecedentes = datetime.now() - pd.DateOffset(days=random.randint(1, 100))
        valido3, motivo3 = validar_antecedentes(deudor, fecha_antecedentes)
        if valido3:
            validaciones["Validación 3"]["Aprobados"] += 1
        else:
            validaciones["Validación 3"]["No Aprobados"] += 1
            # Añadir motivo a la lista de motivos de no aprobación
            validaciones["Validación 3"]["Motivo No Aprobación"].append(motivo3)

        # Realizar validaciones adicionales
        errores = realizar_validaciones(deudor)
        if errores:
            validaciones["Validación 1"]["No Aprobados"] += 1
            validaciones["Validación 1"]["Motivo No Aprobación"].extend(errores)
    
    return validaciones


# Funciones de la aplicación
def firma_garantias(oferta):
    st.write(f"Firmando garantías para {oferta['Nombre']}...")

# Página de captura de datos
def generar_datos_ficticios(n):
    nombres = [f"Nombre_{i}" for i in range(n)]
    nacionalidades = ["Colombiano", "Otro"]
    estados_credito = ["Ninguno", "Castigado", "En mora y castigado"]
    listas_sarlaft = ["No está en ninguna lista", "Vinculantes", "Restrictivas", "Informativas"]
    
    datos = []
    for nombre in nombres:
        fecha_random = datetime.now() - timedelta(days=random.randint(0, 3650))
        año = fecha_random.year
        mes = fecha_random.month
        periodo = "1er Semestre" if mes <= 6 else "2do Semestre"
        # Generar periodicidad aleatoria
        periodicidad = random.choice(['Anual', 'Semestral'])

        
        datos.append({
            "Nombre": nombre,
            "Nacionalidad": random.choice(nacionalidades),
            "Edad": random.randint(18, 65),
            "Estado Crédito": random.choice(estados_credito),
            "Lista SARLAFT": random.choice(listas_sarlaft),
            "Score Crediticio": random.randint(150, 900),
            "Capacidad de Pago (COP)": random.randint(1500000, 20000000),
            "Límite de Endeudamiento (COP)": random.randint(1500000, 20000000),
            "Fecha": fecha_random.strftime("%Y-%m-%d"),
            "Año": año,
            "Mes": mes,
            "Periodo": periodo,
            "Periodicidad": periodicidad  # Nuevo campo Periodicidad
        })
    return datos

# Inicializar datos
beneficiarios_data = generar_datos_ficticios(500)
if "ofertas_enviadas" not in st.session_state:
    st.session_state.ofertas_enviadas = []
if "ofertas_en_proceso" not in st.session_state:
    st.session_state.ofertas_en_proceso = []

# Procesar y mostrar gráficos
def mostrar_graficos(df_beneficiarios):
    # Gráfico 2: Distribución del estado de crédito
    fig, ax = plt.subplots()
    df_beneficiarios['Estado Crédito'].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90, colors=['gold', 'lightcoral', 'lightskyblue'])
    ax.set_title('Distribución del Estado de Crédito')
    st.pyplot(fig)

    # Gráfico 3: Relación entre Score Crediticio y Capacidad de Pago
    fig, ax = plt.subplots()
    ax.scatter(df_beneficiarios['Score Crediticio'], df_beneficiarios['Capacidad de Pago (COP)'], alpha=0.5)
    ax.set_title('Relación entre Score Crediticio y Capacidad de Pago')
    ax.set_xlabel('Score Crediticio')
    ax.set_ylabel('Capacidad de Pago (COP)')
    # Configurar para mostrar valores en el eje Y como enteros
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    # Asegurar que el eje X solo muestre valores enteros
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    # Mostrar el gráfico
    st.pyplot(fig)

    # Gráfico 4: Distribución de las Edades
    fig, ax = plt.subplots()
    ax.hist(df_beneficiarios['Edad'], bins=10, color='lightblue', edgecolor='black')
    ax.set_title('Distribución de las Edades')
    ax.set_xlabel('Edad')
    ax.set_ylabel('Frecuencia')
    st.pyplot(fig)

    # Gráfico 5: Relación entre Capacidad de Pago y Límite de Endeudamiento
    fig, ax = plt.subplots()
    ax.scatter(df_beneficiarios['Capacidad de Pago (COP)'], df_beneficiarios['Límite de Endeudamiento (COP)'], alpha=0.5, color='purple')
    ax.set_title('Relación entre Capacidad de Pago y Límite de Endeudamiento')
    ax.set_xlabel('Capacidad de Pago (COP)')
    ax.set_ylabel('Límite de Endeudamiento (COP)')
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    st.pyplot(fig)

    # Gráfico 6: Beneficiarios por Periodo (Semestre)
    fig, ax = plt.subplots()
    df_beneficiarios['Periodo'].value_counts().plot(kind='bar', ax=ax, color='orange')
    ax.set_title('Número de Beneficiarios por Periodo')
    ax.set_ylabel('Cantidad')
    ax.set_xlabel('Periodo')
    st.pyplot(fig)

    # Gráfico 7: Distribución del Estado de Crédito
    fig, ax = plt.subplots()
    df_beneficiarios['Estado Crédito'].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%', startangle=90, colors=['lightcoral', 'lightgreen', 'skyblue'])
    ax.set_title('Distribución del Estado de Crédito')
    ax.axis('equal')  # Para asegurar que el gráfico sea circular
    st.pyplot(fig)

    # Gráfico 8: Beneficiarios por Lista SARLAFT
    fig, ax = plt.subplots()
    df_beneficiarios['Lista SARLAFT'].value_counts().plot(kind='bar', ax=ax, color='plum')
    ax.set_title('Número de Beneficiarios por Lista SARLAFT')
    ax.set_ylabel('Cantidad')
    ax.set_xlabel('Lista SARLAFT')
    st.pyplot(fig)

    # Gráfico 9: Relación entre Edad y Score Crediticio
    fig, ax = plt.subplots()
    ax.scatter(df_beneficiarios['Edad'], df_beneficiarios['Score Crediticio'], alpha=0.5, color='darkblue')
    ax.set_title('Relación entre Edad y Score Crediticio')
    ax.set_xlabel('Edad')
    ax.set_ylabel('Score Crediticio')
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    st.pyplot(fig)

    # Gráfico 10: Distribución del Score Crediticio por Estado de Crédito
    fig, ax = plt.subplots()
    df_beneficiarios.boxplot(column='Score Crediticio', by='Estado Crédito', ax=ax, grid=False, notch=True)
    ax.set_title('Distribución del Score Crediticio por Estado de Crédito')
    ax.set_ylabel('Score Crediticio')
    plt.suptitle('')  # Para eliminar el título automático del boxplot
    st.pyplot(fig)
 
    # Filtrar solo las columnas numéricas
    df_numerico = df_beneficiarios.select_dtypes(include=['number'])

    # Crear el heatmap de correlación
    fig, ax = plt.subplots()
    sns.heatmap(df_numerico.corr(), annot=True, cmap='coolwarm', ax=ax)
    ax.set_title('Matriz de Correlación')
    st.pyplot(fig)

    # Gráfico 12: Evolución de la Capacidad de Pago Promedio por Año
    fig, ax = plt.subplots()
    df_beneficiarios.groupby('Año')['Capacidad de Pago (COP)'].mean().plot(kind='line', ax=ax, marker='o', color='green')
    ax.set_title('Evolución de la Capacidad de Pago Promedio por Año')
    ax.set_ylabel('Capacidad de Pago (COP)')
    ax.set_xlabel('Año')
    st.pyplot(fig)

    # Gráfico 13: Estado de Crédito por Grupo de Edad
    df_beneficiarios['Grupo Edad'] = pd.cut(df_beneficiarios['Edad'], bins=[18, 30, 40, 50, 65], labels=["18-30", "31-40", "41-50", "51-65"])

    fig, ax = plt.subplots()
    df_grouped = df_beneficiarios.groupby(['Grupo Edad', 'Estado Crédito']).size().unstack().fillna(0)
    df_grouped.plot(kind='bar', stacked=True, ax=ax, color=['skyblue', 'orange', 'lightgreen'])
    ax.set_title('Distribución del Estado de Crédito por Grupo de Edad')
    ax.set_ylabel('Cantidad')
    st.pyplot(fig)

    # Gráfico 15: Comparación del Score Crediticio Promedio entre Semestres
    fig, ax = plt.subplots()
    df_beneficiarios.groupby('Periodo')['Score Crediticio'].mean().plot(kind='line', ax=ax, marker='o', color='blue')
    ax.set_title('Comparación del Score Crediticio Promedio entre Semestres')
    ax.set_ylabel('Score Crediticio Promedio')
    ax.set_xlabel('Periodo')
    st.pyplot(fig)

    # Gráfico 16: Límite de Endeudamiento Promedio por Estado de Crédito
    fig, ax = plt.subplots()
    df_beneficiarios.groupby('Estado Crédito')['Límite de Endeudamiento (COP)'].mean().plot(kind='bar', ax=ax, color='lightblue')
    ax.set_title('Límite de Endeudamiento Promedio por Estado de Crédito')
    ax.set_ylabel('Límite de Endeudamiento (COP)')
    ax.set_xlabel('Estado Crédito')
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    st.pyplot(fig)

    # Gráfico 17: Relación entre Límite de Endeudamiento y Capacidad de Pago
    fig, ax = plt.subplots()
    ax.scatter(df_beneficiarios['Límite de Endeudamiento (COP)'], df_beneficiarios['Capacidad de Pago (COP)'], alpha=0.5, color='purple')
    ax.set_title('Relación entre Límite de Endeudamiento y Capacidad de Pago')
    ax.set_xlabel('Límite de Endeudamiento (COP)')
    ax.set_ylabel('Capacidad de Pago (COP)')
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    st.pyplot(fig)

    # Gráfico 18: Distribución del Score Crediticio
    fig, ax = plt.subplots()
    ax.hist(df_beneficiarios['Score Crediticio'], bins=30, color='teal', edgecolor='black')
    ax.set_title('Distribución del Score Crediticio')
    ax.set_xlabel('Score Crediticio')
    ax.set_ylabel('Frecuencia')
    st.pyplot(fig)

    # Gráfico 19: Evolución del Score Crediticio Promedio por Año
    fig, ax = plt.subplots()
    df_beneficiarios.groupby('Año')['Score Crediticio'].mean().plot(kind='line', ax=ax, marker='o', color='navy')
    ax.set_title('Evolución del Score Crediticio Promedio por Año')
    ax.set_ylabel('Score Crediticio Promedio')
    ax.set_xlabel('Año')
    st.pyplot(fig)

    # Gráfico 20: Edad Promedio por Lista SARLAFT
    fig, ax = plt.subplots()
    df_beneficiarios.groupby('Lista SARLAFT')['Edad'].mean().plot(kind='bar', ax=ax, color='orange')
    ax.set_title('Edad Promedio por Lista SARLAFT')
    ax.set_ylabel('Edad Promedio')
    st.pyplot(fig)

    # Gráfico 21: Capacidad de Pago por Lista SARLAFT (Boxplot)
    fig, ax = plt.subplots()
    sns.boxplot(x='Lista SARLAFT', y='Capacidad de Pago (COP)', data=df_beneficiarios, ax=ax, palette='coolwarm')
    ax.set_title('Distribución de la Capacidad de Pago por Lista SARLAFT')
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    st.pyplot(fig)

    # Gráfico 22: Estado de Crédito por Periodo
    fig, ax = plt.subplots()
    df_grouped = df_beneficiarios.groupby(['Periodo', 'Estado Crédito']).size().unstack().fillna(0)
    df_grouped.plot(kind='bar', stacked=True, ax=ax, color=['gold', 'lightcoral', 'lightskyblue'])
    ax.set_title('Distribución del Estado de Crédito por Periodo')
    ax.set_ylabel('Cantidad')
    st.pyplot(fig)

    # Gráfico 23: Relación entre Score Crediticio y Límite de Endeudamiento
    fig, ax = plt.subplots()
    ax.scatter(df_beneficiarios['Score Crediticio'], df_beneficiarios['Límite de Endeudamiento (COP)'], alpha=0.5, color='darkred')
    ax.set_title('Relación entre Score Crediticio y Límite de Endeudamiento')
    ax.set_xlabel('Score Crediticio')
    ax.set_ylabel('Límite de Endeudamiento (COP)')
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    st.pyplot(fig)

# Funciones de la aplicación
def firma_garantias(oferta):
    st.write(f"Firmando garantías para {oferta['Nombre']}...")

# Página de captura de datos
def captura_datos():
    st.title("Consulta Postulantes")

    # Filtros de Año y Periodo
    st.subheader("Filtros de búsqueda")
    year = st.selectbox("Selecciona el año", options=[2024])
    periodo = st.selectbox("Selecciona el periodo", options=["Todos", "1er Semestre", "2do Semestre"])
    tipo_solicitud = st.selectbox("Tipo de Solicitud", options=["Todos", "Adjudicación", "Renovación"])        

    st.subheader("Filtrar por Fecha")
    fecha_inicio = st.date_input("Fecha de Inicio", value=datetime.today())
    fecha_fin = st.date_input("Fecha de Fin", value=datetime.today())

    # Formulario actual de captura de datos
    st.subheader("Datos del Postulante")
    id_solicitud = st.text_input("ID Solicitud")
    nombre = st.text_input("Nombre")
    apellido = st.text_input("Apellido")
    tipo_documento = st.selectbox("Tipo de Documento", ["Tarjeta de Identidad", "Cédula de Ciudadanía"])
    numero_documento = st.text_input("Número de Documento")
    fecha_solicitud = st.date_input("Fecha de Solicitud", value=datetime.today())
    estado_solicitud = st.selectbox("Estado de Solicitud", ["Pendiente", "Aprobada", "Rechazada"])

    # Campos adicionales
    if st.checkbox("Mostrar campos adicionales"):
        nacionalidad = st.multiselect("Nacionalidad", ["Colombiano", "Otro"])
        edad = st.slider("Edad", min_value=18, max_value=65, value=(18, 65), step=1)
        estado_credito = st.multiselect("Estado del crédito anterior (en caso de tener alguno)", ["Ninguno", "Castigado", "En mora y castigado"])
        lista_sarlaft = st.multiselect("Lista SARLAFT", ["No está en ninguna lista", "Vinculantes", "Restrictivas", "Informativas"])
        score_credito = st.slider("Score crediticio", min_value=150, max_value=900, value=(150, 900), step=1)
        capacidad_pago = st.slider("Capacidad de pago (en COP)", min_value=1500000, max_value=20000000, value=(1500000, 20000000), step=10000)

    if st.button("Mostrar datos de postulantes"):
        df_beneficiarios = pd.DataFrame(beneficiarios_data)

        # Aplicar filtros
        if nacionalidad:
            df_beneficiarios = df_beneficiarios[df_beneficiarios["Nacionalidad"].isin(nacionalidad)]
        if estado_credito:
            df_beneficiarios = df_beneficiarios[df_beneficiarios["Estado Crédito"].isin(estado_credito)]
        if lista_sarlaft:
            df_beneficiarios = df_beneficiarios[df_beneficiarios["Lista SARLAFT"].isin(lista_sarlaft)]
        if year:
            df_beneficiarios = df_beneficiarios[df_beneficiarios["Año"] == year]
        if periodo:
            df_beneficiarios = df_beneficiarios[df_beneficiarios["Periodo"] == periodo]

        # Eliminar la columna de "Nacionalidad"
        df_beneficiarios = df_beneficiarios.drop(columns=["Nacionalidad"], errors='ignore')

        if df_beneficiarios.empty:
            st.warning("No se encontraron beneficiarios que cumplan con los filtros.")
        else:
            st.write("Solicitudes encontradas:")
            st.dataframe(df_beneficiarios)

            # Mostrar gráficos
            mostrar_graficos(df_beneficiarios)

    # Botón para ejecutar validación de beneficiarios
    if st.button("Ejecutar Validación de Postulantes"):
        # Mostrar un spinner mientras se ejecuta el proceso
        with st.spinner("Validando postulantes, por favor espera..."):
            # Simular una ejecución oculta
            beneficiarios_validados = []
            beneficiarios_con_errores = []

            for beneficiario in beneficiarios_data:
                errores = realizar_validaciones(beneficiario)
                if errores:
                    beneficiarios_con_errores.append(beneficiario)
                else:
                    beneficiarios_validados.append(beneficiario)

            # Guardar las listas en el estado de sesión
            st.session_state['beneficiarios_validados'] = beneficiarios_validados
            st.session_state['beneficiarios_con_errores'] = beneficiarios_con_errores

        # Mostrar el resultado final de la validación
        st.success("Validación de beneficiarios ejecutada correctamente.")

        # Mostrar un resumen del resultado
        total_validados = len(beneficiarios_validados)
        total_errores = len(beneficiarios_con_errores)

        st.write(f"✅ Postulantes validados: {total_validados}")
        st.write(f"❌ Postulantes con errores: {total_errores}")

        # Agregar un botón opcional para revisar detalles
        if st.button("Revisar Detalles"):
            st.subheader("Postulantes Validados")
            if beneficiarios_validados:
                st.write(beneficiarios_validados)
            else:
                st.write("No hay postulantes validados.")

            st.subheader("Postulantes con Errores")
            if beneficiarios_con_errores:
                st.write(beneficiarios_con_errores)
            else:
                st.write("No hay postulantes con errores.")

# Página de validación de beneficiarios
def validacion_beneficiarios():
    st.title("Validaciones de Elegibilidad para ICETEX")

    # Paso 1: Listas para almacenar beneficiarios
    beneficiarios_validados = []
    beneficiarios_con_errores = []

    if not beneficiarios_data:
        st.warning("No hay datos de beneficiarios disponibles.")
        return
    
    for i, beneficiario in enumerate(beneficiarios_data):
        st.subheader(f"Beneficiario {i+1}: {beneficiario['Nombre']}")
        
        errores = realizar_validaciones(beneficiario)
        if errores:
            st.error(f"Errores encontrados para {beneficiario['Nombre']}:")
            for error in errores:
                st.write(f"- {error}")
            # Agregar a la lista de beneficiarios con errores
            beneficiarios_con_errores.append(beneficiario)
        else:
            st.success(f"Beneficiario {beneficiario['Nombre']} pasó todas las validaciones.")
            st.write(f"Ofrecer crédito educativo.")
            # Agregar a la lista de beneficiarios validados
            beneficiarios_validados.append(beneficiario)

    # Guardar las listas en el estado para usarlas en otras páginas
    st.session_state['beneficiarios_validados'] = beneficiarios_validados
    st.session_state['beneficiarios_con_errores'] = beneficiarios_con_errores

     # Mensaje visible al completar la validación
    st.success("Se realizó la validación automática de postulantes.")


# Función para realizar las validaciones
def realizar_validaciones(beneficiario):
    errores = []
    
    # Verificar que existan las claves necesarias en los datos del beneficiario
    required_keys = ['Estado Crédito', 'Score Crediticio', 'Capacidad de Pago (COP)']
    for key in required_keys:
        if key not in beneficiario:
            errores.append(f"Falta el campo: {key}.")
        elif beneficiario[key] is None or beneficiario[key] == "":
            errores.append(f"El campo '{key}' no puede estar vacío.")
    
    # Si hay errores en los campos requeridos, salir de la función
    if errores:
        return errores
    
    # Condiciones de validación
    if beneficiario.get('Estado Crédito') in ['Castigado', 'En Mora y Castigado']:
        errores.append("Estado de Crédito no aprobado.")
    if beneficiario.get('Score Crediticio', 0) < 610:
        errores.append("El score crediticio debe ser de mínimo 610 puntos.")
    if beneficiario.get('Capacidad de Pago (COP)', 0) < 3000000:
        errores.append("Capacidad de pago insuficiente.")
    
    return errores

# Página para enviar la oferta al beneficiario
def enviar_oferta():
    st.title("Enviar Oferta a los Postulantes")

    # Verificar y establecer las variables de estado necesarias
    if 'beneficiarios_validados' not in st.session_state:
        st.warning("No se ha realizado la validación de Postulantes.")
        return

    if 'ofertas_en_proceso' not in st.session_state:
        st.session_state['ofertas_en_proceso'] = []

    if 'beneficiarios_con_errores' not in st.session_state:
        st.session_state['beneficiarios_con_errores'] = []  # Inicializa la lista si no existe

    beneficiarios_validados = st.session_state['beneficiarios_validados']
    beneficiarios_con_errores = st.session_state['beneficiarios_con_errores']

    st.subheader(f"{len(beneficiarios_validados)} postulantes pasaron todas las validaciones")

    # Filtros de año y periodo
    anio_actual = datetime.now().year
    anos = list(range(2021, anio_actual + 1))
    año_seleccionado = st.selectbox("Seleccione un año:", anos)
    periodo_seleccionado = st.selectbox("Seleccione un periodo:", ["1 semestre", "2 semestre"])

    if st.button("Enviar oferta a todos los postulantes validados"):
        for beneficiario in beneficiarios_validados:
            oferta = beneficiario.copy()
            oferta["Interesado"] = random.choice(["Sí", "No", "Sí, pero después"])  # Asignar interés aleatorio
            oferta["GarantiaFirmada"] = random.choice([True, False])  # Asignar garantía aleatoria
            oferta["Valor"] = random.randint(3000000, beneficiario["Capacidad de Pago (COP)"])
            oferta["Año"] = año_seleccionado
            oferta["Periodo"] = periodo_seleccionado
            st.session_state['ofertas_en_proceso'].append(oferta)

        st.success("Ofertas enviadas a todos los beneficiarios que pasaron las validaciones.")

    # Crear un DataFrame con los beneficiarios aprobados
    df_aprobados = pd.DataFrame(beneficiarios_validados)
    df_aprobados['Año'] = año_seleccionado
    df_aprobados['Periodo'] = periodo_seleccionado

    # Botón para descargar ofertas aprobadas
    if st.button("Descargar Excel con ofertas aprobadas"):
        # Crear el archivo Excel
        try:
            st.download_button(
                label="Descargar Excel",
                data=df_aprobados.to_csv(index=False).encode('utf-8'),
                file_name="ofertas_aprobadas.csv",
                mime="text/csv"
            )
            st.success("Archivo Excel listo para descargar.")
        except Exception as e:
            st.error(f"Ocurrió un error al descargar el archivo: {e}")

    # Mostrar cuántos postulantes tienen errores
    st.subheader(f"{len(beneficiarios_con_errores)} postulantes no aprobaron todas las validaciones")  # Aquí está la verificación

    if len(beneficiarios_con_errores) > 0:
        st.info("No se enviarán ofertas a los postulantes que no aprobaron todas las validaciones.")

        # Generación de datos para el gráfico tipo embudo
        validacion1_fallos = 0
        validacion2_fallos = 0
        validacion3_fallos = 0

        for beneficiario in beneficiarios_con_errores:
            errores = realizar_validaciones(beneficiario)
            if "El score crediticio debe ser de mínimo 610 puntos." in errores:
                validacion1_fallos += 1
            if "Capacidad de pago insuficiente." in errores:
                validacion2_fallos += 1
            if "Antecedentes menores a 90 días" in errores:
                validacion3_fallos += 1

        # Generar datos para el gráfico
        fallos_validaciones = [validacion1_fallos, validacion2_fallos, validacion3_fallos]
        etapas = ['Validación Score Crediticio', 'Validación Capacidad de Pago', 'Validación Antecedentes Crediticios']

    # Mostrar gráficos adicionales

    # Gráfico 1: Cantidad de beneficiarios aprobados por semestre/año
    st.subheader("Cantidad de beneficiarios aprobados por semestre/año")
    if not df_aprobados.empty:
        aprobados_por_periodo = df_aprobados.groupby(['Año', 'Periodo']).size().unstack(fill_value=0)
        fig1, ax1 = plt.subplots()
        aprobados_por_periodo.plot(kind='bar', stacked=True, ax=ax1)
        ax1.set_xlabel('Año')
        ax1.set_ylabel('Cantidad de Aprobados')
        ax1.set_title('Cantidad de Beneficiarios Aprobados por Año y Periodo')
        st.pyplot(fig1)

    # Gráfico 2: Cantidad de beneficiarios con errores
    st.subheader("Cantidad de beneficiarios con errores por tipo de error")
    errores_count = {
        "Score Crediticio": 0,
        "Capacidad de Pago": 0,
        "Estado Crédito": 0
    }
    
    for beneficiario in beneficiarios_con_errores:
        errores = realizar_validaciones(beneficiario)
        if "El score crediticio debe ser de mínimo 610 puntos." in errores:
            errores_count["Score Crediticio"] += 1
        if "Capacidad de pago insuficiente." in errores:
            errores_count["Capacidad de Pago"] += 1
        if "Estado de Crédito no aprobado." in errores:
            errores_count["Estado Crédito"] += 1

    fig2, ax2 = plt.subplots()
    ax2.bar(errores_count.keys(), errores_count.values(), color='skyblue')
    ax2.set_ylabel('Número de Beneficiarios')
    ax2.set_title('Cantidad de Beneficiarios con Errores por Tipo')
    st.pyplot(fig2)

# Página de gestión comercial de ofertas
def gestion_comercial():
    st.title("Gestión Comercial de Ofertas Enviadas")
    st.image(url_gestion_comercial, caption="Gestión Comercial", use_container_width=True)

    # Verificar si hay ofertas enviadas
    if 'ofertas_en_proceso' not in st.session_state or not st.session_state.ofertas_en_proceso:
        st.warning("No hay ofertas enviadas para gestionar.")
        return

    # Inicializar DataFrame de ofertas
    df_ofertas = pd.DataFrame(st.session_state.ofertas_en_proceso)

    # Seleccionar año
    anio_actual = datetime.now().year
    anio_seleccionado = st.selectbox("Selecciona el año", list(range(2024, anio_actual + 1)))

    # Seleccionar periodo (semestre)
    periodo_seleccionado = st.selectbox("Selecciona el periodo", ["1er Semestre", "2do Semestre"])

    # Filtros para seleccionar el estado de las ofertas
    estado_filtrado = st.selectbox("Respuesta a oferta de pre-aprobación enviada", ["Todos", "Sí", "No", "Sí, pero después"])

    # Inicializar la variable para el estado de garantías
    estado_garantia_filtrado = None

    # Mostrar filtro de Estado de Garantías solo si se selecciona "Sí"
    if estado_filtrado == "Sí":
        estado_garantia_filtrado = st.selectbox("Estado de Garantías", ["Todas", "Garantías Firmadas", "Garantías No Firmadas"])

    # Buscador de Ofertas
    buscador = st.text_input("Buscar oferta por nombre:")
    if buscador:
        df_ofertas = df_ofertas[df_ofertas['Nombre'].str.contains(buscador, case=False, na=False)]

    # Filtrar por año y semestre
    if 'Fecha' in df_ofertas.columns:
        df_ofertas['Fecha'] = pd.to_datetime(df_ofertas['Fecha'])
        if periodo_seleccionado == "1er Semestre":
            df_ofertas = df_ofertas[(df_ofertas['Fecha'].dt.month >= 1) & (df_ofertas['Fecha'].dt.month <= 6)]
        else:
            df_ofertas = df_ofertas[(df_ofertas['Fecha'].dt.month >= 7) & (df_ofertas['Fecha'].dt.month <= 12)]
    else:
        st.error("La columna 'Fecha' no se encuentra en los datos.")
        return

    # Filtrar por estado
    if estado_filtrado != "Todos":
        df_ofertas = df_ofertas[df_ofertas['Interesado'] == estado_filtrado]

    # Filtrar por estado de garantías si se seleccionó "Sí"
    if estado_filtrado == "Sí" and estado_garantia_filtrado != "Todas":
        if estado_garantia_filtrado == "Garantías Firmadas":
            df_ofertas = df_ofertas[df_ofertas['GarantiaFirmada'] == True]
        elif estado_garantia_filtrado == "Garantías No Firmadas":
            df_ofertas = df_ofertas[df_ofertas['GarantiaFirmada'] == False]

    # Informe de seguimiento
    st.subheader("Informe de Seguimiento")
    
    # Contar interesados y garantías
    total_interesados = df_ofertas[df_ofertas['Interesado'] == "Sí"].shape[0]
    total_no_interesados = df_ofertas[df_ofertas['Interesado'] == "No"].shape[0]
    total_si_pero_despues = df_ofertas[df_ofertas['Interesado'] == "Sí, pero después"].shape[0]
    total_garantias_firmadas = df_ofertas[(df_ofertas['Interesado'] == "Sí") & (df_ofertas['GarantiaFirmada'] == True)].shape[0]
    total_garantias_no_firmadas = total_interesados - total_garantias_firmadas if total_interesados > 0 else 0

    # Mostrar informe
    st.write(f"Total ofertas de beneficiarios interesados: {total_interesados}")
    st.write(f"Total ofertas de beneficiarios no interesados: {total_no_interesados}")
    st.write(f"Total ofertas de beneficiarios 'sí, pero después': {total_si_pero_despues}")
    st.write(f"Total garantías firmadas: {total_garantias_firmadas}")
    st.write(f"Total garantías no firmadas: {total_garantias_no_firmadas}")

    # Gráfico de distribución de interesados
    st.subheader("Distribución de Interesados")
    labels_interesados = ['Interesados', 'No Interesados', 'Sí, pero después']
    sizes_interesados = [total_interesados, total_no_interesados, total_si_pero_despues]
    
    plt.figure(figsize=(10, 6))
    plt.pie(sizes_interesados, labels=labels_interesados, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    st.pyplot(plt)

    # Gráfico de garantías firmadas
    st.subheader("Estado de Garantías")
    labels_garantias = ['Garantías Firmadas', 'Garantías No Firmadas']
    sizes_garantias = [total_garantias_firmadas, total_garantias_no_firmadas]

    plt.figure(figsize=(10, 6))
    plt.bar(labels_garantias, sizes_garantias, color=['green', 'red'])
    plt.ylabel('Número de Garantías')
    plt.title('Estado de Garantías Firmadas y No Firmadas')
    st.pyplot(plt)

    # Notificaciones y Alertas (ejemplo simple)
    if total_no_interesados > 0:
        st.warning(f"Existen {total_no_interesados} ofertas no interesadas.")

    # Nuevo: Selección de Oferta
    st.subheader("Seleccionar Oferta")
    oferta_seleccionada = st.selectbox("Selecciona una oferta:", [f"Oferta {i + 1}: {oferta['Nombre']}" for i, oferta in enumerate(st.session_state.ofertas_en_proceso)])

    if st.button("Buscar Oferta"):
        # Filtrar la oferta seleccionada
        nombre_oferta = oferta_seleccionada.split(": ")[1]
        oferta_info = df_ofertas[df_ofertas['Nombre'] == nombre_oferta]
        
        if not oferta_info.empty:
            st.subheader(f"Detalles de {nombre_oferta}")
            for index, row in oferta_info.iterrows():
                st.write(f"Interesado: {row['Interesado']}")
                st.write(f"Estado: {'Garantía Firmada' if row['GarantiaFirmada'] else 'Esperando Confirmación'}")

                # Comentarios y Feedback
                comentarios = st.text_area(f"Comentarios sobre la oferta {row['Nombre']}", value="", key=f"comentario_{index}")
                if st.button(f"Enviar Comentario para {row['Nombre']}", key=f"boton_comentario_{index}"):
                    # Aquí podrías guardar los comentarios en la base de datos o en el estado de sesión
                    st.success("Comentario enviado.")

    # Botones de descarga (después del informe)
    if st.button("Descargar en Excel"):
        # Exportación Personalizada
        columnas_seleccionadas = st.multiselect("Selecciona las columnas para exportar:", df_ofertas.columns.tolist())
        if not columnas_seleccionadas:
            columnas_seleccionadas = df_ofertas.columns.tolist()  # Usar todas las columnas si no se selecciona ninguna

        excel_buffer = io.BytesIO()
        df_ofertas[columnas_seleccionadas].to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)
        st.download_button("Descargar Excel", data=excel_buffer, file_name="ofertas.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    if st.button("Descargar en PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Agregar contenido al PDF
        for i, oferta in enumerate(df_ofertas.to_dict('records')):
            pdf.cell(200, 10, txt=f"Oferta {i + 1}: {oferta['Nombre']}", ln=True)
            pdf.cell(200, 10, txt=f"Interesado: {oferta['Interesado']}", ln=True)
            pdf.cell(200, 10, txt=f"Estado: {estado}", ln=True)
            pdf.cell(200, 10, ln=True)  # Nueva línea

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            pdf.output(temp_pdf.name, 'F')
            temp_pdf.seek(0)

        with open(temp_pdf.name, 'rb') as f:
            pdf_output = f.read()

        st.download_button("Descargar PDF", data=pdf_output, file_name="ofertas.pdf", mime="application/pdf")
	    
# Generación aleatoria de información bancaria
def generar_info_bancaria():
    try:
        # Generar información bancaria aleatoria para la IES
        return {
            "NIT": random.randint(100000000, 999999999),
            "Nombre": f"IES {random.choice(['A', 'B', 'C', 'D'])}",
            "Tipo Cuenta": random.choice(['Corriente', 'Ahorros']),
            "Numero Cuenta": random.randint(10000000, 99999999),
            "Nombre Banco": random.choice(['Banco A', 'Banco B', 'Banco C']),
            "Numero Factura": random.randint(1000, 9999),
            "Valor": random.randint(100000, 35000000)  # Asegúrate de agregar el valor aquí
        }
    except Exception as e:
        st.error(f"Error al generar información bancaria: {str(e)}")
        return None

def gestion_ordenador_gasto():
    st.title("Gestión Ordenador del Gasto")
    st.image(url_gestion_presupuestal, caption="Gestión Presupuestal", use_container_width=True)


    # Inicialización de sesión
    if "ofertas_en_proceso" not in st.session_state or not st.session_state.ofertas_en_proceso:
        st.warning("No hay ofertas en proceso para gestionar.")
        return

    # Inicializar historial de solicitudes en estado de sesión
    if "historial_solicitudes" not in st.session_state:
        st.session_state.historial_solicitudes = []

    # Filtrar ofertas
    df_ofertas = pd.DataFrame(st.session_state.ofertas_en_proceso)

    # Validación de columnas
    if 'GarantiaFirmada' not in df_ofertas.columns:
        st.error("La columna 'GarantiaFirmada' no existe en el DataFrame. Verifica la generación de las ofertas.")
        return

    # Filtrar ofertas con garantía firmada
    df_ofertas = df_ofertas[df_ofertas['GarantiaFirmada'] == True]

    if df_ofertas.empty:
        st.warning("No hay ofertas con garantías firmadas para gestionar.")
        return

    # Adicionar la columna 'tiene_convenio'
    if 'tiene_convenio' not in df_ofertas.columns:
        df_ofertas['tiene_convenio'] = [random.choice(["Sí", "No"]) for _ in range(len(df_ofertas))]
        st.session_state.ofertas_en_proceso = df_ofertas.to_dict('records')

    umbral_presupuesto = st.number_input(
        "Define el umbral de advertencia para el presupuesto (millones de pesos):", min_value=0, key="umbral_presupuesto"
    )

    # Inicializar presupuesto en estado de sesión si no está definido
    if "presupuesto_disponible" not in st.session_state:
        st.session_state.presupuesto_disponible = st.number_input(
            "Define el Presupuesto Disponible (millones de pesos)", min_value=0, value=10000, key="presupuesto_disponible"
        )
    else:
        st.write(f"Presupuesto Disponible: {st.session_state.presupuesto_disponible} millones de pesos")

    # Verificar si el presupuesto disponible está por debajo del umbral
    if st.session_state.presupuesto_disponible < umbral_presupuesto:
        st.warning("Advertencia: El presupuesto disponible está por debajo del umbral definido.")

    # Presupuesto comprometido
    presupuesto_comprometido = st.number_input(
        "Define el Presupuesto Comprometido (millones de pesos)", min_value=0, value=1500, key="presupuesto_comprometido"
    )
    st.write(f"Presupuesto Comprometido: {presupuesto_comprometido} millones de pesos")

    # Control presupuestal
    control_presupuestal = pd.DataFrame({
        "Concepto": ["Presupuesto Disponible", "Presupuesto Comprometido", "Presupuesto Disponible"],
        "Monto (Millones)": [
            st.session_state.presupuesto_disponible,
            presupuesto_comprometido,
            st.session_state.presupuesto_disponible - presupuesto_comprometido
        ]
    })

    st.write("Control Presupuestal:")
    st.dataframe(control_presupuestal)

    st.subheader("Control Presupuestal")
    st.dataframe(control_presupuestal)

    # Tabla de indicadores
    cantidad_ofertas = df_ofertas.shape[0]
    ofertas_convenio = df_ofertas[df_ofertas['tiene_convenio'] == "Sí"]
    ofertas_sin_convenio = df_ofertas[df_ofertas['tiene_convenio'] == "No"]

    cantidad_convenio = ofertas_convenio.shape[0]
    cantidad_sin_convenio = ofertas_sin_convenio.shape[0]

    total_solicitado = df_ofertas['Valor'].sum()
    total_convenio = ofertas_convenio['Valor'].sum()
    total_sin_convenio = ofertas_sin_convenio['Valor'].sum()

    # Crear tablas de indicadores
    indicadores_cantidad = pd.DataFrame({
        "Indicador": [
            "Cantidad de Ofertas con Garantías Firmadas",
            "Cantidad de Ofertas de IES con Convenio",
            "Cantidad de Ofertas de IES sin Convenio",
        ],
        "Valor": [
            cantidad_ofertas,
            cantidad_convenio,
            cantidad_sin_convenio,
        ]
    })

    indicadores_valor = pd.DataFrame({
        "Indicador": [
            "Total Solicitado por IES",
            "Total Solicitado por IES con Convenio",
            "Total Solicitado por IES sin Convenio"
        ],
        "Valor": [
            total_solicitado,
            total_convenio,
            total_sin_convenio
        ]
    })

    st.subheader("Tabla de Indicadores - Cantidades")
    st.dataframe(indicadores_cantidad)

    st.subheader("Tabla de Indicadores - Valores")
    st.dataframe(indicadores_valor)

    # Gráficos de indicadores
    st.subheader("Gráficos de Indicadores")
    
    # Gráfico de Cantidades
    plt.figure(figsize=(8, 4))
    plt.bar(indicadores_cantidad['Indicador'], indicadores_cantidad['Valor'], color=['blue', 'orange', 'green'])
    plt.title("Indicadores de Cantidades")
    plt.xticks(rotation=45)
    plt.ylabel("Cantidad")
    st.pyplot(plt)

    # Gráfico de Valores
    plt.figure(figsize=(8, 4))
    plt.bar(indicadores_valor['Indicador'], indicadores_valor['Valor'], color=['blue', 'orange', 'green'])
    plt.title("Indicadores de Valores")
    plt.xticks(rotation=45)
    plt.ylabel("Valor (millones de pesos)")
    ax = plt.gca()
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    st.pyplot(plt)
	
	# Visualización de datos
    st.subheader("Distribución de IES por Convenio")
    st.bar_chart(df_ofertas['tiene_convenio'].value_counts())


    # Mostrar detalles
    if 'mostrar_detalles' not in st.session_state:
        st.session_state.mostrar_detalles = False

    if st.button("Mostrar Detalles" if not st.session_state.mostrar_detalles else "Ocultar Detalles"):
        st.session_state.mostrar_detalles = not st.session_state.mostrar_detalles

    # Procesar cada beneficiario
    if st.session_state.mostrar_detalles:
        for index, beneficiario in enumerate(df_ofertas.to_dict('records')):
            st.subheader(f"Gestión para {beneficiario.get('Nombre', 'Beneficiario Desconocido')}")
            st.write(f"Valor Solicitado: {beneficiario['Valor']} millones de pesos")
            st.write(f"Tiene Convenio: {beneficiario['tiene_convenio']}")

            if beneficiario['tiene_convenio'] == "No":
                if st.button(f"Solicitar información financiera para IES {beneficiario.get('Nombre', 'IES Desconocida')}", key=f"solicitar_{index}"):
                    info_bancaria = generar_info_bancaria()
                    st.write("Información bancaria generada:")
                    st.write(f"NIT: {info_bancaria['NIT']}")
                    st.write(f"Nombre IES: {info_bancaria['Nombre']}")
                    st.write(f"Tipo de Cuenta: {info_bancaria['Tipo Cuenta']}")
                    st.write(f"Número de Cuenta: {info_bancaria['Numero Cuenta']}")
                    st.write(f"Nombre del Banco: {info_bancaria['Nombre Banco']}")
                    st.write(f"Número de Factura de Matrícula: {info_bancaria['Numero Factura']}")

                    if st.button(f"Confirmar información para giro de {beneficiario.get('Nombre', 'IES Desconocida')}", key=f"confirmar_{index}"):
                        validacion_info = random.choice(["Sí", "No"])
                        if validacion_info == "Sí":
                            st.success("Validación exitosa. Procediendo a giro...")
                            presupuesto_disponible -= beneficiario['Valor']
                            st.session_state.presupuesto_disponible = presupuesto_disponible
                            if presupuesto_disponible < limite_presupuesto:
                                st.warning("¡Urgente! Se recomienda solicitar mayor presupuesto.")
                            if st.button(f"Giro Exitoso para {beneficiario.get('Nombre')}", key=f"giro_exitoso_{index}"):
                                st.success(f"Giro a {beneficiario.get('Nombre')} completado exitosamente.")
                            else:
                                st.error(f"El giro a {beneficiario.get('Nombre')} falló. Por favor reintente.")
                        else:
                            st.warning("La validación de la información ha fallado. Por favor, intente nuevamente.")
            
            elif beneficiario['tiene_convenio'] == "Sí":
                st.success("Iniciando liquidación automática del desembolso...")
                instruccion_giro = f"Instrucción de giro generada para {beneficiario.get('Nombre', 'Beneficiario Desconocido')}."
                st.write(instruccion_giro)
                
                if st.button(f"Aprobar liquidación de IES {beneficiario.get('Nombre')} con convenio", key=f"aprobar_convenio_{index}"):
                    st.success(f"Liquidación aprobada para IES {beneficiario.get('Nombre')}. Procediendo con el desembolso.")
                    # Descontar del presupuesto disponible
                    presupuesto_disponible -= beneficiario['Valor']
                    st.session_state.presupuesto_disponible = presupuesto_disponible
                    if presupuesto_disponible < limite_presupuesto:
                        st.warning("¡Urgente! Se recomienda solicitar mayor presupuesto.")


    # Inicializar historial de solicitudes en estado de sesión
    if "historial_solicitudes" not in st.session_state:
        st.session_state.historial_solicitudes = []

    st.subheader("Aprobar IES")

    # Filtrar las IES según convenio
    tipo_convenio = st.selectbox("Seleccionar tipo de IES", ["Con Convenio", "Sin Convenio"])
    ies_seleccionadas = None

    # Filtro de valor
    min_valor, max_valor = st.slider("Selecciona un rango de valores", 
                                       min_value=0, 
                                       max_value=int(df_ofertas['Valor'].max()), 
                                       value=(0, int(df_ofertas['Valor'].max())))

    if tipo_convenio == "Con Convenio":
        ies_convenio = df_ofertas[df_ofertas['tiene_convenio'] == "Sí"]
        if not ies_convenio.empty:
            ies_seleccionadas = st.multiselect("Selecciona las IES con Convenio", options=ies_convenio['Nombre'].tolist())
        else:
            st.warning("No hay IES con convenio para aprobar.")
    else:
        ies_sin_convenio = df_ofertas[df_ofertas['tiene_convenio'] == "No"]
        if not ies_sin_convenio.empty:
            ies_seleccionadas = st.multiselect("Selecciona las IES sin Convenio", options=ies_sin_convenio['Nombre'].tolist())
                    # Botón para solicitar información financiera
            if ies_seleccionadas and st.button("Solicitar información financiera de las IES sin convenio"):
                for ies in ies_seleccionadas:
                    st.write(f"Solicitud de información financiera enviada para: {ies}")
        else:
            st.warning("No hay IES sin convenio disponibles.")


# Botón para procesar y aprobar desembolso
    if ies_seleccionadas and st.button("Procesar Aprobación"):
        total_aprobado = df_ofertas[df_ofertas['Nombre'].isin(ies_seleccionadas)]['Valor'].sum()
        st.success(f"Se ha aprobado el desembolso de {total_aprobado} millones de pesos para las IES seleccionadas.")

        for ies in ies_seleccionadas:
            valor_ies = df_ofertas[df_ofertas['Nombre'] == ies]['Valor'].values[0]
            st.write(f"IES: {ies}, Valor aprobado: {valor_ies} millones de pesos.")
            st.info(f"Se inició el proceso financiero para la IES: {ies}")

        # Confirmación de aprobación final
        if st.button("Confirmar Aprobación Final"):
            st.success("Desembolso aprobado para las IES seleccionadas.")

    # Mostrar historial de solicitudes
    st.subheader("Historial de Solicitudes")
    for solicitud in st.session_state.historial_solicitudes:
        st.write(solicitud)

# Exportar a CSV
    if st.button("Exportar a CSV"):
        with open('ies_aprobadas.csv', 'w', newline='') as csvfile:
            fieldnames = ['Nombre', 'Valor']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for ies in ies_seleccionadas:
                valor_ies = df_ofertas[df_ofertas['Nombre'] == ies]['Valor'].values[0]
                writer.writerow({'Nombre': ies, 'Valor': valor_ies})
        st.success("Archivo CSV generado con éxito.")


# URL de la imagen del logo
url_logo = "https://raw.githubusercontent.com/JulianTorrest/creditoweb/main/Imagenes/Logo%20ICETEX%20definitivo-2024.png"
url_portada = "https://raw.githubusercontent.com/JulianTorrest/creditoweb/main/portada%20(1).png"
url_gestion_comercial = "https://raw.githubusercontent.com/JulianTorrest/creditoweb/main/Imagenes/gestion%20comercial.jpg"
url_gestion_presupuestal = "https://raw.githubusercontent.com/JulianTorrest/creditoweb/main/Imagenes/gestion%20presupuestal.jpeg"


# Logo en la esquina superior izquierda
col1, col2 = st.columns([1, 8])
with col1:
    st.image(url_logo, width=100)
with col2:
    st.markdown("<h1 style='text-align: center; color: #4B72FA;'>Sistema de Gestión ICETEX</h1>", unsafe_allow_html=True)

# Imagen de portada al inicio
st.image(url_portada, caption="Sistema de Gestión", use_container_width=True)

if 'selected_page' not in st.session_state:
    st.session_state.selected_page = "Consulta de Solicitudes"

# Crear menú de navegación
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    if st.button("Consulta de Solicitudes"):
        st.session_state.selected_page = "Consulta de Solicitudes"
with col2:
    if st.button("Enviar Oferta"):
        st.session_state.selected_page = "Enviar Oferta"
with col3:
    if st.button("Gestión Comercial"):
        st.session_state.selected_page = "Gestión Comercial"
with col4:
    if st.button("Gestión Presupuestal"):
        st.session_state.selected_page = "Gestión Presupuestal"
with col5:  # Nueva opción para los gráficos
    if st.button("Gráficos de Beneficiarios"):
        st.session_state.selected_page = "Gráficos de Beneficiarios"

# Ejecutar la función de la página seleccionada
if st.session_state.selected_page == "Consulta de Solicitudes":
    captura_datos()  # Asegúrate de que esta función esté definida
elif st.session_state.selected_page == "Enviar Oferta":
    enviar_oferta()  # Asegúrate de que esta función esté definida
elif st.session_state.selected_page == "Gestión Comercial":
    gestion_comercial()  # Asegúrate de que esta función esté definida
elif st.session_state.selected_page == "Gestión Presupuestal":
    gestion_ordenador_gasto()  # Asegúrate de que esta función esté definida
elif st.session_state.selected_page == "Gráficos de Beneficiarios":
    if 'df_beneficiarios' in locals() or 'df_beneficiarios' in globals():
        mostrar_graficos(df_beneficiarios)
    else:
        st.error("El DataFrame de beneficiarios no está disponible.")

# Footer personalizado
st.markdown("<footer style='text-align: center; color: gray;'>© 2024 ICETEX - Todos los derechos reservados.</footer>", unsafe_allow_html=True)
