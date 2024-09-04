import streamlit as st
import pandas as pd
from fpdf import FPDF

# Título de la página
st.title("Solicitud de Crédito Educativo - ICETEX")

# Descripción
st.write("""
Por favor, completa el siguiente formulario para solicitar un crédito educativo con ICETEX.
""")

# Formulario principal
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
def generar_pdf(valor_solicitado, cantidad_periodos, ingresos_mensuales, cuota_calculada, viable):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Resumen de Solicitud de Crédito Educativo - ICETEX", ln=True, align='C')
    pdf.ln(10)
    
    pdf.cell(200, 10, txt=f"Valor solicitado por periodo académico: ${valor_solicitado:,}", ln=True)
    pdf.cell(200, 10, txt=f"Cantidad de periodos a financiar: {cantidad_periodos}", ln=True)
    pdf.cell(200, 10, txt=f"Cuota mensual estimada: ${cuota_calculada:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Pago mensual mientras estudias: ${ingresos_mensuales:,}", ln=True)
    
    if viable:
        pdf.cell(200, 10, txt="La solicitud es viable con los ingresos actuales.", ln=True)
    else:
        pdf.cell(200, 10, txt="La solicitud no es viable con los ingresos actuales. La simulación aún se muestra para tu referencia.", ln=True)
    
    pdf.output("resumen_credito.pdf")

# Función para calcular el pago mínimo necesario
def calcular_pago_minimo(valor_solicitado, cantidad_periodos):
    cuota_maxima = ingresos_mensuales * 0.3
    cuota_minima = valor_solicitado / (cantidad_periodos * 6)  # Cuota mensual mínima requerida
    if cuota_minima > cuota_maxima:
        return cuota_minima
    else:
        return cuota_maxima

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
    tiempo_credito_maximo = cantidad_periodos * 2  # Tiempo máximo del crédito es el doble del periodo de estudio
    num_cuotas_finales = tiempo_credito_maximo * 6  # Máximo doble de semestres de estudio
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
    
    valor_solicitado = st.number_input("Valor solicitado:", min_value=0)
    tasa_interes = st.number_input("Tasa de interés anual (%):", min_value=0.0, step=0.1)
    plazo = st.number_input("Plazo en años:", min_value=1, max_value=20, step=1)
    
    if st.button("Simular"):
        cuota_mensual = simular_pago(valor_solicitado, tasa_interes, plazo)
        st.write(f"La cuota mensual para un valor solicitado de ${valor_solicitado} a una tasa de interés de {tasa_interes}% y un plazo de {plazo} años es ${cuota_mensual:.2f}.")

# Ejecutar la lógica del formulario
if submit_button:
    viable, cuota_calculada = calcular_viabilidad(ingresos_mensuales, valor_solicitado, cantidad_periodos)
    
    if viable:
        st.success("La solicitud es viable con los ingresos actuales.")
    else:
        st.error("La solicitud no es viable con los ingresos actuales. La simulación aún se muestra para tu referencia.")
        
        # Calcular mínimo necesario
        minimo_necesario = calcular_pago_minimo(valor_solicitado, cantidad_periodos)
        st.write(f"Para que la solicitud sea viable, necesitas poder pagar al menos ${minimo_necesario:,.2f} por mes.")
    
    # Generar PDF
    generar_pdf(valor_solicitado, cantidad_periodos, ingresos_mensuales, cuota_calculada, viable)
    
    # Mostrar opción de descarga de PDF
    st.write("Haz clic en el siguiente enlace para descargar el PDF:")
    with open("resumen_credito.pdf", "rb") as pdf_file:
        st.download_button(
            label="Descargar PDF",
            data=pdf_file,
            file_name="resumen_credito.pdf",
            mime="application/pdf"
        )

# Agregar simulación de plan de pagos
st.header("Simulación de Plan de Pagos")
form = st.form(key='simulacion_form')
form.valor_solicitado = form.number_input("Valor solicitado por periodo académico:", min_value=0, step=100000)
form.cantidad_periodos = form.number_input("Cantidad de periodos a financiar:", min_value=1, max_value=10, step=1)
form.ingresos_mensuales = form.number_input("Pago mensual mientras estudias:", min_value=0, step=10000)
form.opcion_pago = form.selectbox("Opción de pago durante estudios:", ["0%", "20%"])
submit_simulacion = form.form_submit_button("Simular")

if submit_simulacion:
    df_mientras_estudias, df_finalizado_estudios, total_a_cobro = simular_plan_pagos(
        form.valor_solicitado,
        form.cantidad_periodos,
        form.ingresos_mensuales,
        form.opcion_pago
    )
    
    st.write(f"El total a pagar al finalizar el crédito es ${total_a_cobro:.2f}.")
    st.write("Simulación mientras estudias:")
    st.write(df_mientras_estudias)
    st.write("Simulación al finalizar estudios:")
    st.write(df_finalizado_estudios)

    # Agregar simulación de prefactibilidad
    prefactibilidad()


