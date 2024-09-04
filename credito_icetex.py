import streamlit as st
import pandas as pd
from fpdf import FPDF

# Título de la página
st.title("Solicitud de Crédito Educativo - ICETEX")

# Descripción
st.write("""
Por favor, completa el siguiente formulario para solicitar un crédito educativo con ICETEX.
""")

# Formulario de solicitud de crédito
with st.form(key='credito_form'):
    valor_solicitado = st.number_input("¿Cuál es el valor solicitado por periodo académico?", min_value=0, step=100000)
    cantidad_periodos = st.number_input("Cantidad de periodos a financiar:", min_value=1, max_value=10, step=1)
    pago_mensual = st.number_input("¿Cuánto puedes pagar mensualmente mientras estudias?", min_value=0, step=10000)
    
    submit_button = st.form_submit_button(label='Enviar Solicitud')

# Función para calcular la viabilidad del crédito
def calcular_viabilidad(ingresos, valor_solicitado, cantidad_periodos):
    cuota_maxima = ingresos * 0.3  # 30% de los ingresos como cuota máxima sugerida
    cuota_calculada = valor_solicitado / (cantidad_periodos * 12)  # Cuota mensual estimada
    if cuota_calculada <= cuota_maxima:
        return True, cuota_calculada
    else:
        return False, cuota_calculada

# Función para generar el PDF
def generar_pdf(valor_solicitado, cantidad_periodos, pago_mensual, cuota_calculada):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Resumen de Solicitud de Crédito Educativo - ICETEX", ln=True, align='C')
    pdf.ln(10)
    
    pdf.cell(200, 10, txt=f"Valor solicitado por periodo académico: ${valor_solicitado:,}", ln=True)
    pdf.cell(200, 10, txt=f"Cantidad de periodos a financiar: {cantidad_periodos}", ln=True)
    pdf.cell(200, 10, txt=f"Cuota mensual estimada: ${cuota_calculada:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Pago mensual mientras estudias: ${pago_mensual:,}", ln=True)
    
    pdf.output("resumen_credito.pdf")
    st.success("PDF generado exitosamente.")

# Función para simular diferentes escenarios de pago
def simular_pago(valor_solicitado, tasa_interes, plazo):
    tasa_mensual = tasa_interes / 12 / 100
    n = plazo * 12
    cuota_mensual = valor_solicitado * (tasa_mensual * (1 + tasa_mensual) ** n) / ((1 + tasa_mensual) ** n - 1)
    return cuota_mensual

# Función para precalificación
def precalificar(ingresos, valor_solicitado, cantidad_periodos):
    ratio_ingresos = valor_solicitado / (ingresos * cantidad_periodos)
    if ratio_ingresos < 3:  # Regla arbitraria para precalificación
        return True
    else:
        return False

# Función para calcular desembolso total
def calcular_desembolso_total(valor_solicitado, cantidad_periodos):
    return valor_solicitado * cantidad_periodos

# Función para calcular el capital a cobro
def calcular_capital_a_cobro(desembolso_total, afim):
    return desembolso_total * (1 + afim)

# Función para calcular el interés a cobro
def calcular_interes_a_cobro(capital_a_cobro, tasa_nominal, meses):
    return capital_a_cobro * tasa_nominal * meses / 12

# Función para calcular el interés durante el periodo de gracia
def calcular_interes_periodo_gracia(capital_a_cobro, tasa_nominal, meses_gracia):
    return capital_a_cobro * tasa_nominal * meses_gracia / 12

# Función para calcular el total a cobro
def calcular_total_a_cobro(capital_a_cobro, interes_a_cobro, interes_periodo_gracia):
    return capital_a_cobro + interes_a_cobro + interes_periodo_gracia

# Función para calcular la cuota mensual al terminar estudios
def calcular_cuota_final(total_a_cobro, num_cuotas):
    return total_a_cobro / num_cuotas

# Función para simular el plan de pagos
def simular_plan_pagos(valor_solicitado, cantidad_periodos, pago_mensual, opcion_pago, tasa_nominal):
    # Variables base
    meses_gracia = 6  # Ejemplo de meses de periodo de gracia
    num_cuotas_finales = 60  # Ejemplo de cuotas al finalizar estudios
    
    # Cálculos
    desembolso_total = calcular_desembolso_total(valor_solicitado, cantidad_periodos)
    capital_a_cobro = calcular_capital_a_cobro(desembolso_total, afim)
    interes_a_cobro = calcular_interes_a_cobro(capital_a_cobro, tasa_nominal, cantidad_periodos * 6)
    interes_periodo_gracia = calcular_interes_periodo_gracia(capital_a_cobro, tasa_nominal, meses_gracia)
    total_a_cobro = calcular_total_a_cobro(capital_a_cobro, interes_a_cobro, interes_periodo_gracia)
    valor_cuota_final = calcular_cuota_final(total_a_cobro, num_cuotas_finales)
    
    # Simulación de tablas
    data_mientras_estudias = {
        "Semestre": [f"Semestre {i+1}" for i in range(cantidad_periodos)],
        "Mes": [i+1 for i in range(cantidad_periodos * 6)],
        "Cuota Mensual": [pago_mensual] * (cantidad_periodos * 6),
        "Abono Capital": [pago_mensual * (0 if opcion_pago == "0%" else 0.2)] * (cantidad_periodos * 6),
        "Abono Intereses": [pago_mensual * (1 if opcion_pago == "0%" else 0.8)] * (cantidad_periodos * 6),
        "AFIM": [afim * desembolso_total / (cantidad_periodos * 6)] * (cantidad_periodos * 6),
        "Saldo": [desembolso_total - (pago_mensual * (0.2 if opcion_pago == "20%" else 0)) * i for i in range(cantidad_periodos * 6)]
    }
    
    data_finalizado_estudios = {
        "Mes": [i+1 for i in range(num_cuotas_finales)],
        "Cuota Mensual": [valor_cuota_final] * num_cuotas_finales,
        "Abono Capital": [valor_cuota_final * 0.7] * num_cuotas_finales,
        "Abono Intereses": [valor_cuota_final * 0.3] * num_cuotas_finales,
        "AFIM": [afim * total_a_cobro / num_cuotas_finales] * num_cuotas_finales,
        "Saldo": [total_a_cobro - (valor_cuota_final * i) for i in range(num_cuotas_finales)]
    }
    
    return pd.DataFrame(data_mientras_estudias), pd.DataFrame(data_finalizado_estudios), total_a_cobro

# Al enviar el formulario
if submit_button:
    st.success(f"Solicitud enviada exitosamente. Valor solicitado: ${valor_solicitado:,}. "
               f"Periodos a financiar: {cantidad_periodos}. Pago mensual: ${pago_mensual:,}.")
    
    # Sección de viabilidad del crédito
    st.header("Cálculo de Viabilidad del Crédito")
    ingresos = st.number_input("Ingresos mensuales:", min_value=0, step=100000)
    es_viable, cuota_calculada = calcular_viabilidad(ingresos, valor_solicitado, cantidad_periodos)
    
    if es_viable:
        st.success(f"El crédito es viable. Cuota mensual estimada: ${cuota_calculada:,.2f}")
    else:
        st.error(f"El crédito no es viable con los ingresos actuales. Cuota mensual estimada: ${cuota_calculada:,.2f}")
    
    # Simulación de diferentes escenarios de pago
    st.header("Simulación de Diferentes Escenarios de Pago")
    tasa_interes = st.slider("Tasa de interés anual (%):", 1.0, 20.0, 5.0)
    plazo = st.slider("Plazo (años):", 1, 15, 5)
    cuota_simulada = simular_pago(valor_solicitado, tasa_interes, plazo)
    st.write(f"Con una tasa de interés de {tasa_interes}% y un plazo de {plazo} años, la cuota mensual sería: ${cuota_simulada:,.2f}")
    
    # Precalificación automática
    st.header("Precalificación Automática")
    precalificado = precalificar(ingresos, valor_solicitado, cantidad_periodos)
    
    if precalificado:
        st.success("Precalificación aprobada.")
    else:
        st.error("Precalificación no aprobada.")
    
    # Comparador de créditos
    st.header("Comparador de Créditos")
    comparacion_creditos = {
        "Entidad": ["Banco A", "Banco B", "ICETEX"],
        "Tasa de Interés (%)": [8.5, 9.0, 7.5],
        "Cuota Mensual Estimada ($)": [
            simular_pago(valor_solicitado, 8.5, plazo),
            simular_pago(valor_solicitado, 9.0, plazo),
            simular_pago(valor_solicitado, 7.5, plazo)
        ]
    }
    df_comparacion = pd.DataFrame(comparacion_creditos)
    st.write("Comparación de Opciones de Crédito:")
    st.dataframe(df_comparacion)
    
    # Simulación de plan de pagos
    st.header("Simulación del Plan de Pagos")
    opcion_pago = st.selectbox("Opción de Pago durante los estudios:", ["0%", "20%"])
    afim = st.slider("AFIM (%):", 0.0, 10.0, 0.0)
    
    data_mientras_estudias, data_finalizado_estudios, total_a_cobro = simular_plan_pagos(
        valor_solicitado, cantidad_periodos, pago_mensual, opcion_pago, tasa_interes)
    
    st.write("Simulación durante los estudios:")
    st.dataframe(data_mientras_estudias)
    st.write("Simulación después de los estudios:")
    st.dataframe(data_finalizado_estudios)
    
    st.write(f"Total a cobrar al finalizar los estudios: ${total_a_cobro:,.2f}")
    
    # Botón para generar PDF
    if st.button("Generar PDF"):
        generar_pdf(valor_solicitado, cantidad_periodos, pago_mensual, cuota_calculada)


