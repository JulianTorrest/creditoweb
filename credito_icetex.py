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
    ingresos_mensuales = st.number_input("¿Cuánto puedes pagar mensualmente mientras estudias?", min_value=0, step=10000)
    opcion_pago = st.selectbox("Opción de pago durante estudios:", ["0%", "20%"])
    submit_button = st.form_submit_button(label='Enviar Solicitud')

# Función para calcular la viabilidad del crédito
def calcular_viabilidad(ingresos, valor_solicitado, cantidad_periodos):
    if ingresos == 0:
        return False, 0  # Previene división por cero
    cuota_maxima = ingresos * 0.3  # 30% de los ingresos como cuota máxima sugerida
    cuota_calculada = valor_solicitado / (cantidad_periodos * 6)  # Cuota mensual estimada (6 meses por periodo)
    return cuota_calculada <= cuota_maxima, cuota_calculada

# Función para generar el PDF
def generar_pdf(valor_solicitado, cantidad_periodos, ingresos_mensuales, cuota_calculada):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Resumen de Solicitud de Crédito Educativo - ICETEX", ln=True, align='C')
    pdf.ln(10)
    
    pdf.cell(200, 10, txt=f"Valor solicitado por periodo académico: ${valor_solicitado:,}", ln=True)
    pdf.cell(200, 10, txt=f"Cantidad de periodos a financiar: {cantidad_periodos}", ln=True)
    pdf.cell(200, 10, txt=f"Cuota mensual estimada: ${cuota_calculada:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Pago mensual mientras estudias: ${ingresos_mensuales:,}", ln=True)
    
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
    if ingresos == 0:
        return False  # Previene división por cero
    ratio_ingresos = valor_solicitado / (ingresos * cantidad_periodos * 6)  # Total a financiar / total ingresos durante el período
    return ratio_ingresos < 3  # Regla arbitraria para precalificación

# Función para calcular desembolso total
def calcular_desembolso_total(valor_solicitado, cantidad_periodos):
    return valor_solicitado * cantidad_periodos

# Función para calcular el capital a cobro
def calcular_capital_a_cobro(desembolso_total, afim):
    return desembolso_total * (1 + afim / 100)

# Función para calcular el interés a cobro
def calcular_interes_a_cobro(capital_a_cobro, tasa_nominal, meses):
    return capital_a_cobro * tasa_nominal / 100 * meses / 12

# Función para calcular el interés durante el periodo de gracia
def calcular_interes_periodo_gracia(capital_a_cobro, tasa_nominal, meses_gracia):
    return capital_a_cobro * tasa_nominal / 100 * meses_gracia / 12

# Función para calcular el total a cobro
def calcular_total_a_cobro(capital_a_cobro, interes_a_cobro, interes_periodo_gracia):
    return capital_a_cobro + interes_a_cobro + interes_periodo_gracia

# Función para calcular la cuota mensual al terminar estudios
def calcular_cuota_final(total_a_cobro, num_cuotas):
    return total_a_cobro / num_cuotas

# Función para simular el plan de pagos
def simular_plan_pagos(valor_solicitado, cantidad_periodos, ingresos_mensuales, opcion_pago):
    # Variables base
    meses_gracia = 6  # Ejemplo de meses de periodo de gracia
    num_cuotas_finales = cantidad_periodos * 2 * 6  # Máximo doble de semestres de estudio
    afim = 10.0  # Ejemplo de AFIM en porcentaje
    
    # Cálculos
    desembolso_total = calcular_desembolso_total(valor_solicitado, cantidad_periodos)
    capital_a_cobro = calcular_capital_a_cobro(desembolso_total, afim)
    interes_a_cobro = calcular_interes_a_cobro(capital_a_cobro, 0, cantidad_periodos * 6)  # Tasa de interés 0 durante estudios
    interes_periodo_gracia = calcular_interes_periodo_gracia(capital_a_cobro, 0, meses_gracia)  # Tasa de interés 0 durante gracia
    total_a_cobro = calcular_total_a_cobro(capital_a_cobro, interes_a_cobro, interes_periodo_gracia)
    valor_cuota_final = calcular_cuota_final(total_a_cobro, num_cuotas_finales)
    
    # Simulación de tablas
    data_mientras_estudias = {
        "Semestre": [f"Semestre {i+1}" for i in range(cantidad_periodos) for _ in range(6)],
        "Mes": [i+1 + 6 * (s) for s in range(cantidad_periodos) for i in range(6)],
        "Cuota Mensual": [ingresos_mensuales] * (cantidad_periodos * 6),
        "Abono Capital": [ingresos_mensuales * (0 if opcion_pago == "0%" else 0.2)] * (cantidad_periodos * 6),
        "Abono Intereses": [ingresos_mensuales * (1 if opcion_pago == "0%" else 0.8)] * (cantidad_periodos * 6),
        "AFIM": [afim] * (cantidad_periodos * 6),
        "Saldo": [desembolso_total - (ingresos_mensuales * (0.2 if opcion_pago == "20%" else 0)) * i for i in range(cantidad_periodos * 6)]
    }
    
    data_finalizado_estudios = {
        "Mes": [i+1 for i in range(num_cuotas_finales)],
        "Cuota Mensual": [valor_cuota_final] * num_cuotas_finales,
        "Abono Capital": [valor_cuota_final * 0.7] * num_cuotas_finales,
        "Abono Intereses": [valor_cuota_final * 0.3] * num_cuotas_finales,
        "AFIM": [afim] * num_cuotas_finales,
        "Saldo": [total_a_cobro - (valor_cuota_final * i) for i in range(num_cuotas_finales)]
    }
    
    return pd.DataFrame(data_mientras_estudias), pd.DataFrame(data_finalizado_estudios), total_a_cobro

# Función de prefactibilidad
def prefactibilidad():
    st.header("Módulo de Prefactibilidad")
    
    cantidad_anos = st.number_input("Cantidad de años del crédito:", min_value=1, step=1)
    valor_solicitado = st.number_input("Valor solicitado:", min_value=0, step=100000)
    
    # Tasa nominal de ejemplo
    tasa_nominal = 13.19  # Ejemplo de tasa nominal
    num_cuotas = cantidad_anos * 12  # Asumiendo cuotas mensuales
    
    cuota_mensual = simular_pago(valor_solicitado, tasa_nominal, cantidad_anos)
    
    st.write(f"Cuota mensual aproximada: ${cuota_mensual:.2f}")

if submit_button:
    viabilidad, cuota_calculada = calcular_viabilidad(ingresos_mensuales, valor_solicitado, cantidad_periodos)
    
    if viabilidad:
        st.success("Tu solicitud es viable. Calculando simulación...")
        data_mientras_estudias, data_finalizado_estudios, total_a_cobro = simular_plan_pagos(
            valor_solicitado, cantidad_periodos, ingresos_mensuales, opcion_pago)
        
        st.write("**Simulación mientras estudias:**")
        st.dataframe(data_mientras_estudias)
        
        st.write("**Simulación después de finalizar estudios:**")
        st.dataframe(data_finalizado_estudios)
        
        st.write(f"**Total a pagar al final del período de gracia:** ${total_a_cobro:,.2f}")
        
        generar_pdf(valor_solicitado, cantidad_periodos, ingresos_mensuales, cuota_calculada)
    else:
        st.error("La solicitud no es viable con los ingresos actuales.")
