import streamlit as st
import pandas as pd

# Simulaciones de bases de datos
beneficiarios_data = []

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

# 1. Página de captura de datos
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

# 2. Validación de datos
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

# 3. Enviar oferta por correo
def enviar_oferta():
    st.title("Enviar Oferta al Beneficiario")
    
    if not beneficiarios_data:
        st.warning("No hay datos de beneficiarios disponibles.")
        return
    
    for i, beneficiario in enumerate(beneficiarios_data):
        st.subheader(f"Beneficiario {i+1}: {beneficiario['nombre']}")
