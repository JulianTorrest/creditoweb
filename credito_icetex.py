import streamlit as st
import pandas as pd

# Título de la página
st.title("Solicitud de Crédito Educativo - ICETEX")

# Descripción
st.write("""
Por favor, completa el siguiente formulario para solicitar un crédito educativo con ICETEX.
""")

# Formulario de solicitud de crédito
with st.form(key='credito_form'):
    # Campo 1: Valor solicitado por periodo académico
    valor_solicitado = st.number_input("¿Cuál es el valor solicitado por periodo académico?", min_value=0, step=100000)
    
    # Campo 2: Cantidad de periodos a financiar
    cantidad_periodos = st.number_input("Cantidad de periodos a financiar:", min_value=1, max_value=10, step=1)
    
    # Campo 3: Cuánto puedes pagar mensualmente mientras estudias
    pago_mensual = st.number_input("¿Cuánto puedes pagar mensualmente mientras estudias?", min_value=0, step=10000)
    
    # Botón de enviar
    submit_button = st.form_submit_button(label='Enviar Solicitud')

# Al enviar el formulario
if submit_button:
    st.success(f"Solicitud enviada exitosamente. Valor solicitado: ${valor_solicitado:,}. "
               f"Periodos a financiar: {cantidad_periodos}. Pago mensual: ${pago_mensual:,}.")

# Botón para simular el plan de pagos
if st.button("Simular Plan de Pagos"):
    # Ejemplo de cálculo simplificado
    meses_estudio = cantidad_periodos * 6  # Suponiendo que cada periodo dura 6 meses
    meses_post_estudio = 24  # Ejemplo de 2 años de pago después de estudiar
    tasa_interes = 0.01  # 1% mensual como ejemplo
    
    # Mientras estudias
    data_estudio = []
    saldo = valor_solicitado * cantidad_periodos
    for mes in range(1, meses_estudio + 1):
        interes = saldo * tasa_interes
        abono_capital = max(0, pago_mensual - interes)
        saldo -= abono_capital
        data_estudio.append([mes, pago_mensual, abono_capital, interes, saldo])
    
    df_estudio = pd.DataFrame(data_estudio, columns=["Mes", "Cuota Mensual", "Abono Capital", "Abono Intereses", "Saldo"])
    
    # Finalizado estudios
    data_post_estudio = []
    cuota_post_estudio = saldo / meses_post_estudio
    for mes in range(1, meses_post_estudio + 1):
        interes = saldo * tasa_interes
        abono_capital = cuota_post_estudio - interes
        saldo -= abono_capital
        data_post_estudio.append([mes, cuota_post_estudio, abono_capital, interes, saldo])
    
    df_post_estudio = pd.DataFrame(data_post_estudio, columns=["Mes", "Cuota Mensual", "Abono Capital", "Abono Intereses", "Saldo"])

    # Mostrar tablas
    st.write("### Mientras Estudias")
    st.table(df_estudio)
    
    st.write("### Finalizado Estudios")
    st.table(df_post_estudio)

# Botón para abrir el formulario de datos personales
if st.button("Ingresar Datos del Solicitante"):
    # Formulario de datos personales
    with st.form(key='datos_personales_form'):
        # Campos de datos personales
        nombre = st.text_input("Nombre")
        apellido = st.text_input("Apellido")
        correo = st.text_input("Correo Electrónico")
        direccion = st.text_input("Dirección")
        ciudad = st.text_input("Ciudad")
        departamento = st.text_input("Departamento")
        pais = st.text_input("País")
        ingresos = st.selectbox("Rango de Ingresos Mensuales",
                                ["Menos de 1 millón", "1-2 millones", "2-3 millones", "3-4 millones",
                                 "4-5 millones", "5-6 millones", "6-7 millones", "7-8 millones",
                                 "8-9 millones", "9-10 millones", "10-15 millones", "15-20 millones",
                                 "Más de 20 millones"])

        # Botón de enviar datos personales
        submit_datos_personales = st.form_submit_button(label='Enviar Datos Personales')

    # Al enviar el formulario de datos personales
    if submit_datos_personales:
        st.success(f"Datos personales enviados exitosamente. Nombre: {nombre} {apellido}. "
                   f"Correo: {correo}. Dirección: {direccion}, {ciudad}, {departamento}, {pais}. "
                   f"Ingresos: {ingresos}.")

