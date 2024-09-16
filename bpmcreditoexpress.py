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

# Generar datos ficticios
beneficiarios_data = generar_datos_ficticios(500)

# Página de captura de datos
def captura_datos():
    st.title("Formulario de Búsqueda de Captura de Datos para ICETEX")
    
    # Entradas del formulario
    nombre = st.text_input("Nombre completo")
    nacionalidad = st.multiselect("Nacionalidad", ["Colombiano", "Otro"])
    edad = st.slider("Edad", min_value=10, max_value=65, value=(10, 65), step=1)
    estado_credito = st.multiselect("Estado del crédito anterior", ["Ninguno", "Castigado", "En mora y castigado"])
    lista_sarlaft = st.multiselect("Lista SARLAFT", ["No está en ninguna lista", "Vinculantes", "Restrictivas", "Informativas"])
    score_credito = st.slider("Score crediticio", min_value=150, max_value=900, value=(150, 900), step=1)
    capacidad_pago = st.slider("Capacidad de pago (en COP)", min_value=1500000, max_value=20000000, value=(1500000, 20000000), step=10000)
    limite_endeudamiento = st.slider("Límite de endeudamiento (en COP)", min_value=1500000, max_value=20000000, value=(1500000, 20000000), step=10000)
    
    if st.button("Mostrar datos de beneficiarios"):
        # Crear un DataFrame con los datos de beneficiarios
        df_beneficiarios = pd.DataFrame(beneficiarios_data)
        
        # Aplicar filtros basados en los valores del formulario
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
        
        # Mostrar el DataFrame filtrado
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
            # Aquí se debería enviar el correo, en este caso se simula la acción
            ofertas_enviadas.append(beneficiario)
            st.success(f"Oferta enviada a {beneficiario['Nombre']}.")

# Página de gestión comercial de ofertas
def gestion_comercial():
    st.title("Gestión Comercial de Ofertas Enviadas")
    
    if not ofertas_enviadas:
        st.warning("No hay ofertas enviadas para gestionar.")
        return
    
    for i, oferta in enumerate(ofertas_enviadas):
        st.subheader(f"Oferta {i+1}: {oferta['Nombre']}")
        
        interesado = st.selectbox("¿Está interesado el potencial beneficiario?", ["Sí", "No", "Sí, pero después"])
        
        if interesado == "Sí":
            st.write("Generando marca positiva...")
            # Proceder con la firma de garantías
            firma_garantias(oferta)
        elif interesado == "No":
            st.write("Actualizando registros y finalizando el flujo.")
            ofertas_enviadas.remove(oferta)
            st.success("Registros actualizados y flujo finalizado.")
        elif interesado == "Sí, pero después":
            st.write("Generando marca 'Sí, pero después'...")
            # Aquí se podría gestionar el seguimiento futuro
            st.write("Realizando seguimiento periódico para retomar contacto.")
            
            # Pregunta sobre la garantía
            garantia_firmada = st.checkbox("Garantía firmada recibida")
            
            if garantia_firmada:
                convenio = st.selectbox("¿La IES tiene convenio con ICETEX?", ["Sí", "No"])
                
                if convenio == "Sí":
                    st.write("Realizando liquidación automática del desembolso...")
                    st.write("Generando instrucción de giro...")
                    st.write("Realizando control presupuestal...")
                    st.write("Comprobación digital por el ordenador del gasto...")
                    
                elif convenio == "No":
                    st.write("Solicitando información para giro...")
                    nombre_banco = st.text_input("Nombre del banco")
                    tipo_cuenta = st.selectbox("Tipo de cuenta", ["Ahorros", "Corriente"])
                    numero_cuenta = st.text_input("Número de cuenta")
                    
                    if st.button("Validar información para giro"):
                        st.write("Validando información para giro...")
                        st.write("Realizando liquidación automática del desembolso...")
                        st.write("Generando instrucción de giro...")
                        st.write("Realizando control presupuestal...")
                        st.write("Comprobación digital por el ordenador del gasto...")
                        st.write("Proceso finalizado.")
                
                st.write("Generando módulo de herramientas de aprobación...")
                st.write("Seguimiento de solicitudes y presupuesto.")
                
                # Gestión de interés de potencial beneficiarios
                interesado_nuevo = st.selectbox("¿El potencial beneficiario está interesado después del seguimiento?", ["Sí", "No"])
                
                if interesado_nuevo == "Sí":
                    st.write("Generando marca positiva...")
                    firma_garantias(oferta)
                else:
                    st.write("Actualizando registros y finalizando el flujo.")
                    ofertas_enviadas.remove(oferta)
                    st.success("Registros actualizados y flujo finalizado.")

# Crear usuario y validación de identidad
def crear_usuario(oferta):
    st.title(f"Creación de Usuario para {oferta['Nombre']}")
    
    # Validación de identidad
    st.subheader("Validación de Identidad")
    otp = st.text_input("Ingrese OTP")
    rostro_vivo = st.checkbox("Validación de Rostro Vivo")
    biometrico = st.checkbox("Validación Biométrica")
    preguntas_reto = st.text_input("Responda Preguntas de Reto")
    
    if st.button("Validar Identidad"):
        if otp and rostro_vivo and biometrico and preguntas_reto:
            st.write("Validación de identidad exitosa.")
            
            # Simulador y formulario
            st.write("Accediendo al simulador...")
            monto_sugerido = st.number_input("Monto sugerido", min_value=0)
            limite_inferior = st.number_input("Límite inferior", min_value=0)
            monto_solicitado = st.number_input("Monto solicitado", min_value=0)
            
            st.write("Formulario completado.")
            
            # Decisión de aceptación
            acepta = st.radio("¿Acepta el monto solicitado?", ["Sí", "No"])
            
            if acepta == "Sí":
                st.write("Generando marca positiva...")
                st.write("Procediendo a la firma de garantías...")
                firma_garantias(oferta)
            else:
                st.write("Activando campaña OCM...")
                campaña_ocm = st.selectbox("¿El potencial beneficiario aceptará después de la campaña OCM?", ["Sí", "No"])
                
                if campaña_ocm == "Sí":
                    st.write("Volviendo a la firma de garantías...")
                    firma_garantias(oferta)
                else:
                    st.write("Conociendo causal de no aceptación...")
                    causal = st.text_input("Diligencie la causal de no aceptación")
                    valor_cuota = st.number_input("Valor de la cuota")
                    plazo = st.number_input("Plazo")
                    tasa = st.number_input("Tasa")
                    otra = st.text_input("Otra razón")
                    st.write("Generando marca negativa...")
                    st.success("Proceso finalizado.")
        else:
            st.error("Faltan datos para completar la validación de identidad.")

# Crear las pestañas en la aplicación de Streamlit
st.sidebar.title("Navegación")
page = st.sidebar.selectbox("Selecciona una página:", ["Captura de Datos", "Validación de Beneficiarios", "Enviar Oferta", "Gestión Comercial", "Crear Usuario"])

if page == "Captura de Datos":
    captura_datos()
elif page == "Validación de Beneficiarios":
    validacion_beneficiarios()
elif page == "Enviar Oferta":
    enviar_oferta()
elif page == "Gestión Comercial":
    gestion_comercial()
elif page == "Crear Usuario":
    if ofertas_enviadas:
        for oferta in ofertas_enviadas:
            crear_usuario(oferta)
    else:
        st.warning("No hay ofertas enviadas para crear usuario.")

