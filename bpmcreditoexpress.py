import streamlit as st
import pandas as pd
import random

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
if "ofertas_en_proceso" not in st.session_state:
    st.session_state.ofertas_en_proceso = []

# Funciones de la aplicación
def realizar_validaciones(beneficiario):
    errores = []
    if beneficiario["Score Crediticio"] < 200:
        errores.append("Score crediticio muy bajo.")
    if beneficiario["Capacidad de Pago (COP)"] < 3000000:
        errores.append("Capacidad de pago insuficiente.")
    return errores

def firma_garantias(oferta):
    st.write(f"Firmando garantías para {oferta['Nombre']}...")

# Página de captura de datos
def captura_datos():
    st.title("Formulario de Búsqueda de Captura de Datos para ICETEX")
    
    nombre = st.text_input("Nombre completo")
    nacionalidad = st.multiselect("Nacionalidad", ["Colombiano", "Otro"])
    edad = st.slider("Edad", min_value=10, max_value=65, value=(10, 65), step=1)
    estado_credito = st.multiselect("Estado del crédito anterior", ["Ninguno", "Castigado", "En mora y castigado"])
    lista_sarlaft = st.multiselect("Lista SARLAFT", ["No está en ninguna lista", "Vinculantes", "Restrictivas", "Informativas"])
    score_credito = st.slider("Score crediticio", min_value=150, max_value=900, value=(150, 900), step=1)
    capacidad_pago = st.slider("Capacidad de pago (en COP)", min_value=1500000, max_value=20000000, value=(1500000, 20000000), step=10000)
    limite_endeudamiento = st.slider("Límite de endeudamiento (en COP)", min_value=1500000, max_value=20000000, value=(1500000, 20000000), step=10000)
    
    if st.button("Mostrar datos de beneficiarios"):
        df_beneficiarios = pd.DataFrame(beneficiarios_data)
        
        if nacionalidad:
            df_beneficiarios = df_beneficiarios[df_beneficiarios["Nacionalidad"].isin(nacionalidad)]
        if estado_credito:
            df_beneficiarios = df_beneficiarios[df_beneficiarios["Estado Crédito"].isin(estado_credito)]
        if lista_sarlaft:
            df_beneficiarios = df_beneficiarios[df_beneficiarios["Lista SARLAFT"].isin(lista_sarlaft)]
        if edad:
            df_beneficiarios = df_beneficiarios[df_beneficiarios["Edad"].between(edad[0], edad[1])]
        if score_credito:
            df_beneficiarios = df_beneficiarios[df_beneficiarios["Score Crediticio"].between(score_credito[0], score_credito[1])]
        if capacidad_pago:
            df_beneficiarios = df_beneficiarios[df_beneficiarios["Capacidad de Pago (COP)"].between(capacidad_pago[0], capacidad_pago[1])]
        if limite_endeudamiento:
            df_beneficiarios = df_beneficiarios[df_beneficiarios["Límite de Endeudamiento (COP)"].between(limite_endeudamiento[0], limite_endeudamiento[1])]
        
        st.dataframe(df_beneficiarios)

# Página de validación de beneficiarios
def validacion_beneficiarios():
    st.title("Validaciones de Elegibilidad para ICETEX")
    
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
        else:
            st.success(f"Beneficiario {beneficiario['Nombre']} pasó todas las validaciones.")
            st.write(f"Ofrecer crédito educativo.")

# Página para enviar la oferta al beneficiario
def enviar_oferta():
    st.title("Enviar Oferta al Beneficiario")
    
    if not beneficiarios_data:
        st.warning("No hay datos de beneficiarios disponibles.")
        return
    
    for i, beneficiario in enumerate(beneficiarios_data):
        st.subheader(f"Beneficiario {i+1}: {beneficiario['Nombre']}")
        if st.button(f"Enviar oferta a {beneficiario['Nombre']}"):
            st.session_state.ofertas_enviadas.append(beneficiario.copy())
            st.session_state.ofertas_en_proceso.append({
                "Nombre": beneficiario["Nombre"],
                "Estado": "Enviada"
            })
            st.success(f"Oferta enviada a {beneficiario['Nombre']}.")

# Página de gestión comercial de ofertas
def gestion_comercial():
    st.title("Gestión Comercial de Ofertas Enviadas")
    
    if not st.session_state.ofertas_en_proceso:
        st.warning("No hay ofertas en proceso para gestionar.")
        return
    
    for i, oferta in enumerate(st.session_state.ofertas_en_proceso):
        st.subheader(f"Oferta {i+1}: {oferta['Nombre']}")
        
        interesado = st.selectbox("¿Está interesado el potencial beneficiario?", ["Sí", "No", "Sí, pero después"], key=f"interesado_{i}")
        
        if interesado == "Sí, pero después":
            st.write("Generando marca 'Sí, pero después'...")
            firma_garantias(oferta)
            st.session_state.ofertas_en_proceso[i]["Estado"] = "Marca Sí, pero después"
        elif interesado == "No":
            st.write("Actualizando registros y finalizando el flujo.")
            st.session_state.ofertas_en_proceso[i]["Estado"] = "Finalizada"
            st.session_state.ofertas_en_proceso.remove(oferta)
            st.success("Registros actualizados y flujo finalizado.")
        elif interesado == "Sí":
            st.write("Generando marca positiva...")
            st.write("Realizando seguimiento periódico para retomar contacto.")
            
            garantia_firmada = st.checkbox("Garantía firmada recibida", key=f"garantia_firmada_{i}")
            
            if garantia_firmada:
                convenio = st.selectbox("¿La IES tiene convenio con ICETEX?", ["Sí", "No"], key=f"convenio_{i}")
                
                if convenio == "Sí":
                    st.write("Realizando liquidación automática del desembolso...")
                    st.write("Generando instrucción de giro...")
                    st.write("Realizando control presupuestal...")
                    st.write("Comprobación digital por el ordenador del gasto...")
                    st.session_state.ofertas_en_proceso[i]["Estado"] = "En Proceso"
                    
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
                        st.session_state.ofertas_en_proceso[i]["Estado"] = "En Proceso"
                        
                    st.write("Generando módulo de herramientas de aprobación...")
                    st.write("Seguimiento de solicitudes y presupuesto.")
                    
                    if st.button("Finalizar proceso", key=f"finalizar_proceso_{i}"):
                        st.session_state.ofertas_en_proceso[i]["Estado"] = "Finalizada"
                        st.success("Proceso finalizado y oferta gestionada.")

# Página de gestión del ordenador del gasto
def gestion_ordenador_gasto():
    st.title("Gestión Ordenador del Gasto")
    
    if not st.session_state.ofertas_en_proceso:
        st.warning("No hay ofertas en proceso para gestionar.")
        return
    
    for i, oferta in enumerate(st.session_state.ofertas_en_proceso):
        st.subheader(f"Oferta {i+1}: {oferta['Nombre']}")
        
        if oferta["Estado"] == "En Proceso":
            st.write(f"Estado actual de la oferta: {oferta['Estado']}")
            st.write("Detalles del proceso en curso:")
            st.write("Realizando liquidación automática del desembolso...")
            st.write("Generando instrucción de giro...")
            st.write("Realizando control presupuestal...")
            st.write("Comprobación digital por el ordenador del gasto...")
            st.write("Generando módulo de herramientas de aprobación...")
            st.write("Seguimiento de solicitudes y presupuesto.")
            
            aprobado = st.checkbox(f"Aprobar oferta {i+1}", key=f"aprobar_oferta_{i}")
            if aprobado:
                st.success(f"Oferta {i+1} aprobada.")
                st.session_state.ofertas_en_proceso[i]["Estado"] = "Aprobada"
            else:
                st.warning(f"Oferta {i+1} no aprobada.")
                st.session_state.ofertas_en_proceso[i]["Estado"] = "No Aprobada"

# Configurar el menú de la aplicación
menu = st.sidebar.selectbox(
    "Selecciona una página",
    ["Captura de Datos", "Validación de Beneficiarios", "Enviar Oferta", "Gestión Comercial", "Gestión Ordenador del Gasto"]
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
elif menu == "Gestión Ordenador del Gasto":
    gestion_ordenador_gasto()
