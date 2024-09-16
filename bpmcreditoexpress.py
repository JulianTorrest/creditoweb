import streamlit as st
import pandas as pd

# Simulaciones de bases de datos
beneficiarios_data = []
ofertas_enviadas = []
potenciales_beneficiarios = []
base_referidos = []

# Función para simular validaciones
def realizar_validaciones(datos_beneficiario):
    errores = []
    
    # Validación 1: Nacionalidad y edad
    if datos_beneficiario["nacionalidad"] != "Colombiano":
        errores.append("El beneficiario no es colombiano.")
    if datos_beneficiario["edad"] >= 65:
        errores.append("El beneficiario es mayor de 65 años.")
    
    # Validación 2: Estado de crédito
    if datos_beneficiario["estado_credito"] == "castigado":
        errores.append("El beneficiario tiene un crédito castigado.")
    elif datos_beneficiario["estado_credito"] == "en mora y castigado":
        errores.append("El beneficiario tiene un crédito en mora y está castigado.")
    
    # Validación 3: SARLAFT
    if datos_beneficiario["lista_sarlaft"] == "Vinculantes":
        errores.append("El beneficiario está en lista SARLAFT vinculante.")
    
    # Validación 4: Score crediticio
    if datos_beneficiario["score_credito"] == "":
        errores.append("El beneficiario no tiene score crediticio.")
    elif datos_beneficiario["score_credito"] < 500:
        errores.append("El score es bajo. Se requiere codeudor.")
    
    # Validación 5: Modelo de pre-aprobación
    if datos_beneficiario["capacidad_pago"] < datos_beneficiario["limite_endeudamiento"]:
        errores.append("El beneficiario no tiene suficiente capacidad de pago.")
    
    return errores

# Página de captura de datos
def captura_datos():
    st.title("Formulario de Captura de Datos para ICETEX")
    
    nombre = st.text_input("Nombre completo")
    nacionalidad = st.selectbox("Nacionalidad", ["Colombiano", "Otro"])
    edad = st.number_input("Edad", min_value=18, max_value=80, step=1)
    estado_credito = st.selectbox("Estado del crédito anterior", ["Ninguno", "castigado", "en mora y castigado"])
    lista_sarlaft = st.selectbox("Lista SARLAFT", ["No está en ninguna lista", "Vinculantes", "Restrictivas", "Informativas"])
    score_credito = st.number_input("Score crediticio", min_value=0, max_value=850, step=1)
    capacidad_pago = st.number_input("Capacidad de pago (en COP)")
    limite_endeudamiento = st.number_input("Límite de endeudamiento (en COP)")
    
    if st.button("Enviar formulario"):
        datos_beneficiario = {
            "nombre": nombre,
            "nacionalidad": nacionalidad,
            "edad": edad,
            "estado_credito": estado_credito,
            "lista_sarlaft": lista_sarlaft,
            "score_credito": score_credito,
            "capacidad_pago": capacidad_pago,
            "limite_endeudamiento": limite_endeudamiento
        }
        beneficiarios_data.append(datos_beneficiario)
        st.success(f"Datos del beneficiario {nombre} capturados exitosamente.")

# Página de validación de beneficiarios
def validacion_beneficiarios():
    st.title("Validaciones de Elegibilidad para ICETEX")
    
    if not beneficiarios_data:
        st.warning("No hay datos de beneficiarios disponibles.")
        return
    
    for i, beneficiario in enumerate(beneficiarios_data):
        st.subheader(f"Beneficiario {i+1}: {beneficiario['nombre']}")
        
        errores = realizar_validaciones(beneficiario)
        if errores:
            st.error(f"Errores encontrados para {beneficiario['nombre']}:")
            for error in errores:
                st.write(f"- {error}")
        else:
            st.success(f"Beneficiario {beneficiario['nombre']} pasó todas las validaciones.")
            st.write(f"Ofrecer crédito educativo.")

# Página para enviar la oferta al beneficiario
def enviar_oferta():
    st.title("Enviar Oferta al Beneficiario")
    
    if not beneficiarios_data:
        st.warning("No hay datos de beneficiarios disponibles.")
        return
    
    for i, beneficiario in enumerate(beneficiarios_data):
        st.subheader(f"Beneficiario {i+1}: {beneficiario['nombre']}")
        if st.button(f"Enviar oferta a {beneficiario['nombre']}"):
            # Aquí se debería enviar el correo, en este caso se simula la acción
            ofertas_enviadas.append(beneficiario)
            st.success(f"Oferta enviada a {beneficiario['nombre']}.")

# Página de gestión comercial de ofertas
def gestion_comercial():
    st.title("Gestión Comercial de Ofertas Enviadas")
    
    if not ofertas_enviadas:
        st.warning("No hay ofertas enviadas para gestionar.")
        return
    
    for i, oferta in enumerate(ofertas_enviadas):
        st.subheader(f"Oferta {i+1}: {oferta['nombre']}")
        
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
            interesado = st.selectbox("¿El potencial beneficiario está interesado?", ["Sí", "No"])
            
            if interesado == "Sí":
                seguimiento_periodico(oferta)
            else:
                st.write("Actualizando registros y finalizando el flujo.")
                ofertas_enviadas.remove(oferta)
                st.success("Registros actualizados y flujo finalizado.")
                
# Seguimiento periódico y validaciones adicionales
def seguimiento_periodico(oferta):
    st.title(f"Seguimiento Periódico para {oferta['nombre']}")
    
    st.write("Realizando seguimiento periódico...")
    # Verificación de antecedentes crediticios
    antecedentes_dias = st.number_input("Días desde el último antecedente crediticio", min_value=0, max_value=365)
    
    if antecedentes_dias > 90:
        st.write("Antecedentes crediticios mayores a 90 días, añadiendo a la base de referidos...")
        base_referidos.append(oferta)
        st.write("Seleccionando nuevos potenciales beneficiarios...")
        return
    
    if antecedentes_dias <= 30:
        st.write("Creando usuario...")
        crear_usuario(oferta)
    else:
        st.write("Consultando SARLAFT...")
        consulta_sarlaft = st.selectbox("Consulta SARLAFT aprobada?", ["Sí", "No"])
        
        if consulta_sarlaft == "Sí":
            st.write("Creando usuario...")
            crear_usuario(oferta)
        else:
            st.write("Notificando y actualizando base...")
            # Lógica para notificar y actualizar base
            st.success("Base actualizada y flujo finalizado.")

# Crear usuario y validación de identidad
def crear_usuario(oferta):
    st.title(f"Creación de Usuario para {oferta['nombre']}")
    
    # Validación de identidad
    st.subheader("Validación de Identidad")
    otp = st.text_input("Ingrese OTP")
    rostro_vivo = st.checkbox("Validación de Rostro Vivo")
    biometrico = st.checkbox("Validación Biométrica")
    preguntas_reto = st.text_input("Responda Preguntas de Reto")
    
    if st.button("Validar Identidad"):
        if otp and rostro_vivo and biometrico and preguntas_reto:
            st.success("Identidad validada exitosamente.")
            st.write("Entrando al simulador...")
            simulador(oferta)
        else:
            st.error("No se completaron todos los métodos de validación.")

# Simulador para el monto a pagar
def simulador(oferta):
    st.title("Simulador de Monto a Pagar")
    
    monto_sugerido = st.number_input("Monto sugerido para pagar mensualmente", min_value=0)
    limite_inferior = st.number_input("Límite inferior del parámetro establecido", min_value=0)
    monto_solicitado = st.number_input("Monto solicitado", min_value=0)
    
    if st.button("Aceptar monto"):
        st.write("Generando marca positiva...")
        firma_garantias(oferta)
    else:
        st.write("Activando campaña OCM para incentivar al potencial beneficiario...")
        # Simulación de campaña OCM
        interes_despues_OCM = st.selectbox("¿El potencial beneficiario está interesado después de la campaña OCM?", ["Sí", "No"])
        
        if interes_despues_OCM == "Sí":
            st.write("Generando marca positiva...")
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

# Firma de garantías
def firma_garantias(oferta):
    st.title("Firma de Garantías")
    
    firma_recibida = st.checkbox("Firma de garantías recibida")
    
    if firma_recibida:
        st.write("Conectando con el ICETEX para verificar convenio...")
        # Aquí se integraría la lógica para verificar el convenio con ICETEX
        convenio = st.selectbox("¿La IES tiene convenio con ICETEX?", ["Sí", "No"])
        
        if convenio == "Sí":
            st.success("Proceso completado exitosamente.")
        else:
            st.write("Reiniciando proceso de firma de garantías...")
            # Aquí se debería reiniciar el proceso o manejar la falta de convenio.
            st.write("Proceso finalizado.")
    else:
        st.write("Activando campaña OCM para firma de garantías...")
        # Simulación de campaña OCM para firma de garantías
        firma_despues_OCM = st.selectbox("¿Firma de garantías después de campaña OCM?", ["Sí", "No"])
        
        if firma_despues_OCM == "Sí":
            st.write("Conectando con ICETEX para verificar convenio...")
            convenio = st.selectbox("¿La IES tiene convenio con ICETEX?", ["Sí", "No"])
            if convenio == "Sí":
                st.success("Proceso completado exitosamente.")
            else:
                st.write("Proceso finalizado.")
        else:
            st.success("Proceso finalizado.")

# Crear las pestañas en la aplicación de Streamlit
st.sidebar.title("Navegación")
page = st.sidebar.selectbox("Selecciona una página:", ["Captura de Datos", "Validación de Beneficiarios", "Enviar Oferta", "Gestión Comercial"])

if page == "Captura de Datos":
    captura_datos()
elif page == "Validación de Beneficiarios":
    validacion_beneficiarios()
elif page == "Enviar Oferta":
    enviar_oferta()
elif page == "Gestión Comercial":
    gestion_comercial()
