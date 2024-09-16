import streamlit as st
import pandas as pd
import random
import numpy as np

# Crear una función para generar datos ficticios
def generar_datos_ficticios(n):
    nombres = [f"Nombre_{i}" for i in range(n)]
    nacionalidades = ["Colombiano", "Otro"]
    estados_credito = ["Ninguno", "Castigado", "En mora y castigado"]
    listas_sarlaft = ["No está en ninguna lista", "Vinculantes", "Restrictivas", "Informativas"]
    
    datos = []
    for nombre in nombres:
        datos.append({
            "Nombre": nombre,
            "Nacionalidad": random.choice(nacionalidades),
            "Edad": random.randint(18, 65),
            "Estado Crédito": random.choice(estados_credito),
            "Lista SARLAFT": random.choice(listas_sarlaft),
            "Score Crediticio": random.randint(150, 900),
            "Capacidad de Pago (COP)": random.randint(1500000, 20000000),
            "Límite de Endeudamiento (COP)": random.randint(1500000, 20000000)
        })
    return datos

# Inicializar datos
beneficiarios_data = generar_datos_ficticios(500)
if "ofertas_enviadas" not in st.session_state:
    st.session_state.ofertas_enviadas = []

# Variables globales para el presupuesto
presupuesto_total = 500000000  # 500 millones COP
if "presupuesto_disponible" not in st.session_state:
    st.session_state.presupuesto_disponible = presupuesto_total

# Funciones de la aplicación
def captura_datos():
    st.title("Captura de Datos de Beneficiarios")
    # Aquí puedes agregar el formulario para capturar los datos del beneficiario
    nombre = st.text_input("Nombre del Beneficiario")
    edad = st.number_input("Edad", min_value=18, max_value=100)
    estado_credito = st.selectbox("Estado de Crédito", ["Ninguno", "Castigado", "En mora y castigado"])
    lista_sarlaft = st.selectbox("Lista SARLAFT", ["No está en ninguna lista", "Vinculantes", "Restrictivas", "Informativas"])
    score_crediticio = st.number_input("Score Crediticio", min_value=150, max_value=900)
    capacidad_pago = st.number_input("Capacidad de Pago (COP)", min_value=1500000)
    limite_endeudamiento = st.number_input("Límite de Endeudamiento (COP)", min_value=1500000)
    
    if st.button("Agregar Beneficiario"):
        nuevo_beneficiario = {
            "Nombre": nombre,
            "Edad": edad,
            "Estado Crédito": estado_credito,
            "Lista SARLAFT": lista_sarlaft,
            "Score Crediticio": score_crediticio,
            "Capacidad de Pago (COP)": capacidad_pago,
            "Límite de Endeudamiento (COP)": limite_endeudamiento
        }
        st.session_state.ofertas_enviadas.append(nuevo_beneficiario)
        st.success("Beneficiario agregado con éxito.")

def validacion_beneficiarios():
    st.title("Validación de Beneficiarios")
    
    for i, beneficiario in enumerate(st.session_state.ofertas_enviadas):
        st.subheader(f"Beneficiario {i+1}: {beneficiario['Nombre']}")
        
        errores = realizar_validaciones(beneficiario)
        if errores:
            for error in errores:
                st.error(f"Error: {error}")
        else:
            st.success("Beneficiario validado correctamente.")

def enviar_oferta():
    st.title("Enviar Oferta")
    st.write("Aquí puedes agregar la lógica para enviar ofertas a los beneficiarios.")

def firma_garantias(oferta):
    st.write(f"Firmando garantías para {oferta['Nombre']}...")

# Función para mostrar semáforo de valores
def mostrar_semaforo(valor, limites, etiquetas):
    color = ""
    if valor < limites[0]:
        color = '🟢'  # Verde
    elif limites[0] <= valor < limites[1]:
        color = '🟡'  # Amarillo
    else:
        color = '🔴'  # Rojo
    st.write(f"{etiquetas}: {valor:,} {color}")

# Página de gestión comercial de ofertas con semáforo de valores, estadísticas financieras y presupuesto
def gestion_comercial():
    st.title("Gestión Comercial de Ofertas Enviadas")
    
    if not st.session_state.ofertas_enviadas:
        st.warning("No hay ofertas enviadas para gestionar.")
        return
    
    # Mostrar el presupuesto disponible
    st.subheader(f"Presupuesto disponible: COP {st.session_state.presupuesto_disponible:,}")
    
    for i, oferta in enumerate(st.session_state.ofertas_enviadas):
        st.subheader(f"Oferta {i+1}: {oferta['Nombre']}")
        
        # Mostrar semáforo de valores financieros
        mostrar_semaforo(oferta["Capacidad de Pago (COP)"], [5000000, 10000000], "Capacidad de Pago (COP)")
        mostrar_semaforo(oferta["Score Crediticio"], [400, 600], "Score Crediticio")
        mostrar_semaforo(oferta["Límite de Endeudamiento (COP)"], [5000000, 10000000], "Límite de Endeudamiento (COP)")
        
        interesado = st.selectbox("¿Está interesado el potencial beneficiario?", ["Sí", "No", "Sí, pero después"], key=f"interesado_{i}")
        
        if interesado == "Sí":
            st.write("Generando marca positiva...")
            firma_garantias(oferta)
            convenio = st.selectbox("¿La IES tiene convenio con ICETEX?", ["Sí", "No"], key=f"convenio_{i}")
            
            if convenio == "Sí":
                st.write("Realizando liquidación automática del desembolso...")
                monto_oferta = random.randint(10000000, 50000000)  # Simular el monto de la oferta en COP
                st.write(f"Monto otorgado: COP {monto_oferta:,}")
                
                if st.session_state.presupuesto_disponible >= monto_oferta:
                    st.session_state.presupuesto_disponible -= monto_oferta
                    st.success(f"Presupuesto restante: COP {st.session_state.presupuesto_disponible:,}")
                else:
                    st.error("Presupuesto insuficiente para otorgar la oferta.")
                    
            elif convenio == "No":
                st.write("Solicitando información para giro...")
                nombre_banco = st.text_input("Nombre del banco", key=f"nombre_banco_{i}")
                tipo_cuenta = st.selectbox("Tipo de cuenta", ["Ahorros", "Corriente"], key=f"tipo_cuenta_{i}")
                numero_cuenta = st.text_input("Número de cuenta", key=f"numero_cuenta_{i}")
                
                if st.button("Validar información para giro", key=f"validar_info_{i}"):
                    st.write("Validando información para giro...")
                    st.write("Realizando liquidación automática del desembolso...")
                    st.write("Generando instrucción de giro...")
                    st.write("Realizando control presupuestal...")
                    st.write("Comprobación digital por el ordenador del gasto...")
                    st.write("Proceso finalizado.")
                    
            st.write("Generando módulo de herramientas de aprobación...")
            st.write("Seguimiento de solicitudes y presupuesto.")
            
        elif interesado == "No":
            st.write("Actualizando registros y finalizando el flujo.")
            st.session_state.ofertas_enviadas.remove(oferta)
            st.success("Registros actualizados y flujo finalizado.")
        elif interesado == "Sí, pero después":
            st.write("Generando marca 'Sí, pero después'...")
            st.write("Realizando seguimiento periódico para retomar contacto.")

# Estadísticas financieras
def mostrar_estadisticas_financieras():
    st.title("Estadísticas Financieras de Beneficiarios")
    
    df_beneficiarios = pd.DataFrame(beneficiarios_data)
    
    st.subheader("Estadísticas Generales")
    st.write(f"Capacidad de Pago Promedio: COP {df_beneficiarios['Capacidad de Pago (COP)'].mean():,.2f}")
    st.write(f"Límite de Endeudamiento Promedio: COP {df_beneficiarios['Límite de Endeudamiento (COP)'].mean():,.2f}")
    st.write(f"Score Crediticio Promedio: {df_beneficiarios['Score Crediticio'].mean():.2f}")
    
    st.subheader("Estadísticas Descriptivas")
    st.dataframe(df_beneficiarios[["Capacidad de Pago (COP)", "Límite de Endeudamiento (COP)", "Score Crediticio"]].describe())

# Configurar el menú de la aplicación
menu = st.sidebar.selectbox(
    "Selecciona una página",
    ["Captura de Datos", "Validación de Beneficiarios", "Enviar Oferta", "Gestión Comercial", "Estadísticas Financieras"]
)

# Ejecutar la página seleccionada
if menu == "Captura de Datos":
    captura_datos()
elif menu == "Validación de Beneficiarios":
    validacion_beneficiarios()
elif menu == "Enviar Oferta":
    enviar_oferta()
elif menu == "Gestión Comercial":
    gestion_comercial()
elif menu == "Estadísticas Financieras":
    mostrar_estadisticas_financieras()

