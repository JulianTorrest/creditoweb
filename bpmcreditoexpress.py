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
            st.success(f"Oferta enviada a {beneficiario['Nombre']}.")

# Página de gestión comercial de ofertas
def gestion_comercial():
    st.title("Gestión Comercial de Ofertas Enviadas")
    
    if not st.session_state.ofertas_enviadas:
        st.warning("No hay ofertas enviadas para gestionar.")
        return
    
    for i, oferta in enumerate(st.session_state.ofertas_enviadas):
        st.subheader(f"Oferta {i+1}: {oferta['Nombre']}")
        
        interesado = st.selectbox("¿Está interesado el potencial beneficiario?", ["Sí", "No", "Sí, pero después"], key=f"interesado_{i}")
        
        if interesado == "Sí, pero después":
            st.write("Generando marca 'Sí, pero después'...")
            firma_garantias(oferta)
        elif interesado == "No":
            st.write("Actualizando registros y finalizando el flujo.")
            st.session_state.ofertas_enviadas.remove(oferta)
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
                
                interesado_nuevo = st.selectbox("¿El potencial beneficiario está interesado después del seguimiento?", ["Sí", "No"], key=f"interesado_nuevo_{i}")
                if interesado_nuevo == "Sí":
                    st.success(f"Beneficiario {oferta['Nombre']} está listo para proceder con la oferta.")
                else:
                    st.warning(f"Beneficiario {oferta['Nombre']} decidió no proceder.")

# Página de gestión para el ordenador del gasto
def gestion_ordenador_gasto():
    st.title("Gestión para el Ordenador del Gasto")

    # Información de la liquidación automática del desembolso
    st.header("Liquidación Automática del Desembolso")
    st.write("Generando liquidación automática del desembolso...")
    # Muestra detalles de la liquidación
    st.write("Detalles del desembolso...")
    # Aquí puedes agregar información más específica o datos de ejemplo

    # Generación automática de la instrucción de giro
    st.header("Generación Automática de Instrucción de Giro")
    st.write("Generando instrucción de giro...")
    # Muestra detalles de la instrucción de giro
    st.write("Detalles de la instrucción de giro...")
    # Agrega información adicional si es necesario

    # Control presupuestal
    st.header("Control Presupuestal")
    presupuesto_disponible = st.number_input("Presupuesto disponible (en COP)", min_value=0, step=1000)
    monto_solicitado = st.number_input("Monto solicitado (en COP)", min_value=0, step=1000)

    if monto_solicitado > presupuesto_disponible:
        st.error("El monto solicitado excede el presupuesto disponible.")
    else:
        st.success("Presupuesto dentro de los límites permitidos.")

    st.write("Alertas de cumplimiento del presupuesto:")
    if monto_solicitado > presupuesto_disponible * 0.8:
        st.warning("El monto solicitado se acerca al límite del presupuesto.")

    # Aprobación digital
    st.header("Aprobación Digital por Ordenador del Gasto")
    aprobado = st.checkbox("Aprobar desembolso")
    if aprobado:
        st.success("Desembolso aprobado.")
    else:
        st.warning("Desembolso no aprobado.")

    # Seguimiento de solicitudes y presupuesto disponible
    st.header("Seguimiento de Solicitudes y Presupuesto")
    if aprobado:
        st.write("Realizando seguimiento de las solicitudes aprobadas...")
        st.write(f"Presupuesto disponible restante: {presupuesto_disponible - monto_solicitado} COP")
        st.write("Proceso finalizado.")
    else:
        st.write("No se ha realizado seguimiento ya que el desembolso no fue aprobado.")

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
