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
    cuota_mensual_post_estudios = st.number_input("¿Cuánto puedes pagar mensualmente después de finalizar los estudios?", min_value=0, step=10000)
    submit_button = st.form_submit_button(label='Enviar Solicitud y Simulación')
    clear_button = st.form_submit_button(label='Limpiar Datos', help="Haz clic aquí para limpiar todos los datos del formulario")

# Función para calcular la viabilidad del crédito
def calcular_viabilidad(ingresos, valor_solicitado, cantidad_periodos, cuota_mensual_post_estudios, total_cuotas):
    if ingresos == 0:
        return False, 0  # Previene división por cero
    promedio_cuota = total_cuotas / (cantidad_periodos * 6 + (total_cuotas / 6))  # Promedio de las cuotas mensuales
    return promedio_cuota <= ingresos, promedio_cuota

# Función para generar el PDF
def generar_pdf(valor_solicitado, cantidad_periodos, ingresos_mensuales, promedio_cuota, viable):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Resumen de Solicitud de Crédito Educativo - ICETEX", ln=True, align='C')
    pdf.ln(10)
    
    pdf.cell(200, 10, txt=f"Valor solicitado por periodo académico: ${valor_solicitado:,}", ln=True)
    pdf.cell(200, 10, txt=f"Cantidad de periodos a financiar: {cantidad_periodos}", ln=True)
    pdf.cell(200, 10, txt=f"Pago mensual promedio: ${promedio_cuota:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Pago mensual mientras estudias: ${ingresos_mensuales:,}", ln=True)
    
    if viable:
        pdf.cell(200, 10, txt="La solicitud es viable con los ingresos actuales.", ln=True)
    else:
        pdf.cell(200, 10, txt="La solicitud no es viable con los ingresos actuales. La simulación aún se muestra para tu referencia.", ln=True)
    
    pdf.output("resumen_credito.pdf")

# Función para simular el plan de pagos
def simular_plan_pagos(valor_solicitado, cantidad_periodos, ingresos_mensuales, cuota_mensual_post_estudios):
    meses_gracia = 6  # Ejemplo de meses de periodo de gracia
    tiempo_credito_maximo = cantidad_periodos * 2  # Tiempo máximo del crédito es el doble del periodo de estudio
    num_cuotas_finales = tiempo_credito_maximo * 6  # Máximo doble de semestres de estudio
    tasa_interes_mensual = 0.0116  # Tasa mensual (1.16%)

    # Inicialización
    saldo_periodo = valor_solicitado

    # Dataframe durante los estudios
    data_mientras_estudias = []
    for semestre in range(cantidad_periodos):
        for mes in range(6):  # 6 meses por semestre
            if ingresos_mensuales > 0:
                intereses = saldo_periodo * tasa_interes_mensual  # Intereses mensuales
                abono_capital = max(0, ingresos_mensuales - intereses)  # El abono a capital es la cuota mensual menos los intereses
                saldo_periodo = saldo_periodo - abono_capital + intereses  # Ajuste del saldo
            else:
                intereses = 0
                abono_capital = 0
                saldo_periodo += intereses  # Solo se acumulan intereses sin abono de capital

            if mes == 5:  # En el último mes de cada semestre, añadir nuevo saldo
                saldo_periodo += valor_solicitado

            data_mientras_estudias.append({
                "Semestre": f"Semestre {semestre+1}",
                "Mes": mes + 1 + semestre * 6,
                "Cuota Mensual": ingresos_mensuales,
                "Abono Capital": abono_capital,
                "Abono Intereses": intereses,
                "Saldo": saldo_periodo
            })

    # Saldo final después de estudios
    saldo_final = saldo_periodo
    data_finalizado_estudios = []
    for mes in range(num_cuotas_finales):
        if saldo_final <= 0:
            break
        intereses = saldo_final * tasa_interes_mensual  # Intereses mensuales N.A.M.V
        cuota_pago_final = min(cuota_mensual_post_estudios, saldo_final + intereses)
        abono_capital = cuota_pago_final - intereses
        saldo_final -= abono_capital

        data_finalizado_estudios.append({
            "Mes": mes + 1,
            "Cuota Mensual": cuota_pago_final,
            "Abono Capital": abono_capital,
            "Abono Intereses": intereses,
            "Saldo": saldo_final
        })

    # Si queda saldo remanente, distribuirlo entre las últimas cuotas
    if saldo_final > 0:
        ajuste = saldo_final / len(data_finalizado_estudios)  # Distribuir el saldo restante equitativamente
        for entry in data_finalizado_estudios:
            entry["Cuota Mensual"] += ajuste
            entry["Saldo"] = max(0, entry["Saldo"] - ajuste)

    return pd.DataFrame(data_mientras_estudias), pd.DataFrame(data_finalizado_estudios), saldo_final

# Lógica para ejecutar y mostrar resultados
if submit_button:
    # Simular el plan de pagos
    df_mientras_estudias, df_finalizado_estudios, saldo_final = simular_plan_pagos(
        valor_solicitado,
        cantidad_periodos,
        ingresos_mensuales,
        cuota_mensual_post_estudios
    )

    # Calcular la suma de todas las cuotas y su promedio
    total_cuotas = df_mientras_estudias["Cuota Mensual"].sum() + df_finalizado_estudios["Cuota Mensual"].sum()
    viable, promedio_cuota = calcular_viabilidad(ingresos_mensuales, valor_solicitado, cantidad_periodos, cuota_mensual_post_estudios, total_cuotas)

    if viable:
        st.success("La solicitud es viable con los ingresos actuales.")
    else:
        st.error("La solicitud no es viable con los ingresos actuales.")
        st.warning(f"Para que la solicitud sea viable, necesitas poder pagar al menos ${promedio_cuota:,.2f} mensualmente.")

    # Generar PDF
    generar_pdf(valor_solicitado, cantidad_periodos, ingresos_mensuales, promedio_cuota, viable)

    # Mostrar opción de descarga de PDF
    st.write("Haz clic en el siguiente enlace para descargar el PDF:")
    with open("resumen_credito.pdf", "rb") as pdf_file:
        st.download_button(
            label="Descargar PDF",
            data=pdf_file,
            file_name="resumen_credito.pdf",
            mime="application/pdf"
        )

    # Mostrar las tablas
    st.header("Simulación de Plan de Pagos")

    st.subheader("Durante los estudios")
    st.dataframe(df_mientras_estudias)

    st.subheader("Después de finalizar los estudios")
    st.dataframe(df_finalizado_estudios)

# Manejo del botón de limpiar
if clear_button:
    st.experimental_rerun()
