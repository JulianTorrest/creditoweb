import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from fpdf import FPDF
import io

# Título de la página
st.title("Formulario de Crédito Educativo")

# Formulario combinado
with st.form(key='credito_y_simulacion_form'):
    valor_solicitado = st.number_input("¿Cuál es el valor solicitado por periodo académico?", min_value=0, step=100000)
    cantidad_periodos = st.number_input("Cantidad de periodos a financiar:", min_value=1, max_value=10, step=1)
    ingresos_mensuales = st.number_input("¿Cuánto puedes pagar mensualmente mientras estudias?", min_value=0, step=10000)
    tasa_interes = st.number_input("Tasa de interés mensual (en porcentaje):", min_value=0.0, max_value=100.0, step=0.01) / 100
    submit_button = st.form_submit_button(label='Enviar Solicitud y Simulación')
    clear_button = st.form_submit_button(label='Limpiar Datos', help="Haz clic aquí para limpiar todos los datos del formulario")

# Validación de Entrada de Datos
def validar_datos(valor_solicitado, cantidad_periodos, ingresos_mensuales, tasa_interes):
    errores = []
    if valor_solicitado <= 0:
        errores.append("El valor solicitado debe ser mayor que 0.")
    if cantidad_periodos <= 0:
        errores.append("La cantidad de periodos debe ser mayor que 0.")
    if ingresos_mensuales <= 0:
        errores.append("Los ingresos mensuales deben ser mayores que 0.")
    if tasa_interes < 0 or tasa_interes > 1:
        errores.append("La tasa de interés debe estar entre 0% y 100%.")

    return errores

# Función para calcular la viabilidad del crédito
def calcular_viabilidad(ingresos, total_cuotas, total_meses):
    if ingresos == 0:
        return False, 0  # Previene división por cero
    promedio_cuota = total_cuotas / total_meses  # Promedio de las cuotas mensuales
    return promedio_cuota <= ingresos, promedio_cuota

# Función para generar el PDF
def generar_pdf(valor_solicitado, cantidad_periodos, ingresos_mensuales, promedio_cuota, viable, df_mientras_estudias, df_finalizado_estudios, cuota_ideal):
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
        pdf.cell(200, 10, txt="La solicitud no es viable con los ingresos actuales. La simulación se muestra para tu referencia.", ln=True)
    
    pdf.ln(10)

    # Agregar tablas al PDF
    pdf.set_font("Arial", size=10)
    
    def add_table(df, title):
        pdf.cell(200, 10, txt=title, ln=True)
        pdf.ln(5)
        for col in df.columns:
            pdf.cell(40, 10, txt=col, border=1, align='C')
        pdf.ln()
        for i in range(len(df)):
            for col in df.columns:
                pdf.cell(40, 10, txt=str(df[col][i]), border=1, align='C')
            pdf.ln()
        pdf.ln(5)

    add_table(df_mientras_estudias, "Resumen de pagos durante los estudios")
    add_table(df_finalizado_estudios, "Resumen de pagos después de finalizar los estudios")

    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Cuota Mensual Ideal: ${cuota_ideal:,.2f}", ln=True)

    pdf_output = io.BytesIO()
    pdf.output(pdf_output, 'F')  # Guardar PDF en BytesIO
    pdf_output.seek(0)
    
    return pdf_output

# Función para simular el plan de pagos
def simular_plan_pagos(valor_solicitado, cantidad_periodos, ingresos_mensuales, tasa_interes):
    meses_gracia = 6
    tiempo_credito_maximo = cantidad_periodos * 2
    num_cuotas_finales = tiempo_credito_maximo * 6
    tasa_interes_mensual = tasa_interes

    saldo_periodo = 0
    cuota_fija = ingresos_mensuales
    afim_total = valor_solicitado * 0.02
    cuota_afim_mensual = afim_total / (cantidad_periodos * meses_gracia)

    data_mientras_estudias = []

    for semestre in range(cantidad_periodos):
        for mes in range(meses_gracia):
            if mes == 0:
                saldo_periodo += valor_solicitado

            intereses = saldo_periodo * tasa_interes_mensual
            abono_capital = cuota_fija - intereses - cuota_afim_mensual
            if abono_capital < 0:
                abono_capital = 0
                cuota_fija = intereses + cuota_afim_mensual

            saldo_periodo -= abono_capital
            saldo_periodo = max(saldo_periodo, 0)

            data_mientras_estudias.append({
                "Semestre": f"Semestre {semestre+1}",
                "Mes": mes + 1 + semestre * meses_gracia,
                "Cuota Mensual": cuota_fija,
                "Abono Capital": abono_capital,
                "Abono Intereses": intereses,
                "AFIM": cuota_afim_mensual,
                "Saldo": saldo_periodo
            })

    saldo_final = saldo_periodo
    data_finalizado_estudios = []
    saldo_inicial_post_estudios = saldo_final

    if saldo_inicial_post_estudios > 0:
        cuota_ideal = saldo_inicial_post_estudios * tasa_interes_mensual / (1 - (1 + tasa_interes_mensual)**-num_cuotas_finales)

        for mes in range(num_cuotas_finales):
            if saldo_inicial_post_estudios <= 0:
                break
            intereses = saldo_inicial_post_estudios * tasa_interes_mensual
            abono_capital = cuota_ideal - intereses
            saldo_inicial_post_estudios -= abono_capital
            saldo_inicial_post_estudios = max(saldo_inicial_post_estudios, 0)

            data_finalizado_estudios.append({
                "Mes": mes + 1,
                "Cuota Mensual": cuota_ideal,
                "Abono Capital": abono_capital,
                "Abono Intereses": intereses,
                "Saldo": saldo_inicial_post_estudios
            })
    else:
        cuota_ideal = 0

    df_mientras_estudias = pd.DataFrame(data_mientras_estudias)
    df_finalizado_estudios = pd.DataFrame(data_finalizado_estudios)

    return df_mientras_estudias, df_finalizado_estudios, saldo_final, cuota_ideal

# Gráfico del saldo durante los estudios
def graficar_saldo_mientras_estudias(df_mientras_estudias):
    fig, ax = plt.subplots()
    ax.plot(df_mientras_estudias["Mes"], df_mientras_estudias["Saldo"], marker='o', color='blue', label="Saldo")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Saldo")
    ax.set_title("Evolución del Saldo durante los Estudios")
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    st.pyplot(fig)

# Gráfico del saldo después de los estudios
def graficar_saldo_despues_estudios(df_finalizado_estudios):
    fig, ax = plt.subplots()
    ax.plot(df_finalizado_estudios["Mes"], df_finalizado_estudios["Saldo"], marker='o', color='red', label="Saldo")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Saldo")
    ax.set_title("Evolución del Saldo después de los Estudios")
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    st.pyplot(fig)

# Gráfico de distribución de pagos de intereses y capital
def graficar_distribucion_pagos(df_finalizado_estudios):
    fig, ax = plt.subplots()
    
    ax.bar(df_finalizado_estudios["Mes"], df_finalizado_estudios["Abono Intereses"], color='orange', label="Intereses")
    ax.bar(df_finalizado_estudios["Mes"], df_finalizado_estudios["Abono Capital"], color='green', bottom=df_finalizado_estudios["Abono Intereses"], label="Capital")
    
    ax.set_xlabel("Mes")
    ax.set_ylabel("Monto")
    ax.set_title("Distribución de Pagos de Intereses y Capital")
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    
    ax.legend()
    st.pyplot(fig)

# Lógica del formulario
if submit_button:
    errores = validar_datos(valor_solicitado, cantidad_periodos, ingresos_mensuales, tasa_interes)
    
    if errores:
        st.error("Por favor, corrige los siguientes errores:")
        for error in errores:
            st.error(f"- {error}")
    else:
        df_mientras_estudias, df_finalizado_estudios, saldo_final, cuota_ideal = simular_plan_pagos(valor_solicitado, cantidad_periodos, ingresos_mensuales, tasa_interes)
        
        viable, promedio_cuota = calcular_viabilidad(ingresos_mensuales, df_finalizado_estudios["Cuota Mensual"].sum(), cantidad_periodos * 6)
        
        st.write(f"Total de pagos mientras estudias: ${df_mientras_estudias['Cuota Mensual'].sum():,.2f}")
        st.write(f"Total de pagos después de finalizar los estudios: ${df_finalizado_estudios['Cuota Mensual'].sum():,.2f}")
        
        graficar_saldo_mientras_estudias(df_mientras_estudias)
        graficar_saldo_despues_estudios(df_finalizado_estudios)
        graficar_distribucion_pagos(df_finalizado_estudios)

        pdf_output = generar_pdf(valor_solicitado, cantidad_periodos, ingresos_mensuales, promedio_cuota, viable, df_mientras_estudias, df_finalizado_estudios, cuota_ideal)
        
        st.download_button(
            label="Descargar Resumen en PDF",
            data=pdf_output,
            file_name="resumen_credito_educativo.pdf",
            mime="application/pdf"
        )
