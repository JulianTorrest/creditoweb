import streamlit as st
import pandas as pd
from fpdf import FPDF

# Título de la página
st.title("Solicitud de Crédito Educativo - ICETEX")

# Formulario combinado
with st.form(key='credito_y_simulacion_form'):
    valor_solicitado = st.number_input("¿Cuál es el valor solicitado por periodo académico?", min_value=0, step=100000)
    cantidad_periodos = st.number_input("Cantidad de periodos a financiar:", min_value=1, max_value=10, step=1)
    ingresos_mensuales = st.number_input("¿Cuánto puedes pagar mensualmente mientras estudias?", min_value=0, step=10000)
    opcion_pago = st.selectbox("Opción de pago durante estudios:", ["0%", "20%"])
    submit_button = st.form_submit_button(label='Enviar Solicitud y Simulación')
    clear_button = st.form_submit_button(label='Limpiar Datos', help="Haz clic aquí para limpiar todos los datos del formulario")

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
        minimo_necesario = calcular_pago_minimo(valor_solicitado, cantidad_periodos)
        pdf.cell(200, 10, txt=f"Para que la solicitud sea viable, necesitas poder pagar al menos ${minimo_necesario:,.2f} por mes.", ln=True)
    
    pdf.output("resumen_credito.pdf")

# Función para calcular el pago mínimo necesario
def calcular_pago_minimo(valor_solicitado, cantidad_periodos):
    cuota_maxima = ingresos_mensuales * 0.3
    cuota_minima = valor_solicitado / (cantidad_periodos * 6)  # Cuota mensual mínima requerida
    if cuota_minima > cuota_maxima:
        return cuota_minima
    else:
        return cuota_maxima

# Función para simular el plan de pagos
def simular_plan_pagos(valor_solicitado, cantidad_periodos, ingresos_mensuales, opcion_pago):
    # Variables base
    meses_gracia = 6  # Ejemplo de meses de periodo de gracia
    tiempo_credito_maximo = cantidad_periodos * 2  # Tiempo máximo del crédito es el doble del periodo de estudio
    num_cuotas_finales = tiempo_credito_maximo * 6  # Máximo doble de semestres de estudio
    afim = 10.0  # Ejemplo de AFIM en porcentaje

    # Cálculos
    desembolso_total = valor_solicitado * cantidad_periodos
    capital_a_cobro = desembolso_total * (1 + afim / 100)
    interes_a_cobro = capital_a_cobro * 0 / 100 * cantidad_periodos * 6  # Tasa de interés 0 durante estudios
    interes_periodo_gracia = capital_a_cobro * 0 / 100 * meses_gracia  # Tasa de interés 0 durante gracia
    total_a_cobro = capital_a_cobro + interes_a_cobro + interes_periodo_gracia
    
    # Cuota mensual al final de los estudios
    valor_cuota_final = total_a_cobro / num_cuotas_finales
    
    # Simulación de tablas
    saldo = desembolso_total
    data_mientras_estudias = {
        "Semestre": [f"Semestre {i+1}" for i in range(cantidad_periodos) for _ in range(6)],
        "Mes": [i+1 + 6 * (s) for s in range(cantidad_periodos) for i in range(6)],
        "Cuota Mensual": [ingresos_mensuales] * (cantidad_periodos * 6),
        "Abono Capital": [ingresos_mensuales * (0 if opcion_pago == "0%" else 0.2)] * (cantidad_periodos * 6),
        "Abono Intereses": [ingresos_mensuales * (1 if opcion_pago == "0%" else 0.8)] * (cantidad_periodos * 6),
        "AFIM": [afim] * (cantidad_periodos * 6),
        "Saldo": [saldo - (ingresos_mensuales * (0.2 if opcion_pago == "20%" else 0)) * i for i in range(cantidad_periodos * 6)]
    }
    
    saldo_final = saldo - (ingresos_mensuales * (0.2 if opcion_pago == "20%" else 0)) * (cantidad_periodos * 6)
    
    data_finalizado_estudios = {
        "Mes": [i+1 for i in range(num_cuotas_finales)],
        "Cuota Mensual": [valor_cuota_final] * num_cuotas_finales,
        "Abono Capital": [valor_cuota_final * 0.7] * num_cuotas_finales,
        "Abono Intereses": [valor_cuota_final * 0.3] * num_cuotas_finales,
        "AFIM": [afim] * num_cuotas_finales,
        "Saldo": [total_a_cobro - (valor_cuota_final * i) for i in range(num_cuotas_finales)]
    }
    
    return pd.DataFrame(data_mientras_estudias), pd.DataFrame(data_finalizado_estudios), total_a_cobro, saldo_final

# Lógica para ejecutar y mostrar resultados
if submit_button:
    viable, cuota_calculada = calcular_viabilidad(ingresos_mensuales, valor_solicitado, cantidad_periodos)
    
    if viable:
        st.success("La solicitud es viable con los ingresos actuales.")
        saldo_final = 0
    else:
        st.error("La solicitud no es viable con los ingresos actuales. La simulación aún se muestra para tu referencia.")
        minimo_necesario = calcular_pago_minimo(valor_solicitado, cantidad_periodos)
        st.write(f"Para que la solicitud sea viable, necesitas poder pagar al menos ${minimo_necesario:,.2f} por mes.")
        saldo_final = None  # Indicar que el saldo final no será 0 en este caso
    
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
    
    # Simular el plan de pagos
    st.header("Simulación de Plan de Pagos")
    df_mientras_estudias, df_finalizado_estudios, total_a_cobro, saldo_final = simular_plan_pagos(
        valor_solicitado,
        cantidad_periodos,
        ingresos_mensuales,
        opcion_pago
    )
    
    st.write(f"El total a pagar al finalizar el crédito es ${total_a_cobro:.2f}.")
    if saldo_final == 0:
        st.write("Tu saldo final es 0, lo que significa que has cubierto todos los pagos durante el periodo de gracia.")
    else:
        st.write(f"Tu saldo final es ${saldo_final:.2f}.")
    
    st.subheader("Durante los estudios")
    st.dataframe(df_mientras_estudias)
    
    st.subheader("Después de finalizar los estudios")
    st.dataframe(df_finalizado_estudios)

# Manejo del botón de limpiar
if clear_button:
    st.experimental_rerun()
