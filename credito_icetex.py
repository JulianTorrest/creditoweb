import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from fpdf import FPDF
import tempfile
import io
import os

# Colores institucionales del ICETEX
COLOR_ICETEX_PRIMARY = "#003D7C"
COLOR_ICETEX_SECONDARY = "#E9E9E9"

# Título de la página
st.title("Formulario de Crédito Educativo")

# Tasas de interés para otras entidades financieras (en porcentaje mensual)
tasas_competencia = {
    "Bancolombia": 0.0171,
    "BBVA": 0.0213,
    "Davivienda": 0.0166,
    "Banco de Bogota": 0.0174,
    "Serfinanza": 0.0179
}

# Formulario combinado
with st.form(key='credito_y_simulacion_form'):
    valor_solicitado = st.number_input("¿Cuál es el valor solicitado por periodo académico?", min_value=0, step=100000)
    cantidad_periodos = st.number_input("Cantidad de periodos a financiar:", min_value=1, max_value=10, step=1)
    ingresos_mensuales = st.number_input("¿Cuánto puedes pagar mensualmente mientras estudias?", min_value=0, step=10000)
    submit_button = st.form_submit_button(label='Enviar Solicitud y Simulación')
    clear_button = st.form_submit_button(label='Limpiar Datos', help="Haz clic aquí para limpiar todos los datos del formulario")

# Función para calcular la viabilidad del crédito
def calcular_viabilidad(ingresos, total_cuotas, total_meses):
    if ingresos == 0:
        return False, 0  # Previene división por cero
    promedio_cuota = total_cuotas / total_meses  # Promedio de las cuotas mensuales
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
    
    # Guardar el PDF en un archivo temporal
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        pdf.output(temp_file.name)
        temp_file.seek(0)
        pdf_bytes = temp_file.read()
        temp_file.close()
        os.remove(temp_file.name)
    
    return pdf_bytes

# Función para simular el plan de pagos
def simular_plan_pagos(valor_solicitado, cantidad_periodos, ingresos_mensuales, tasa_interes_mensual):
    meses_gracia = 6  # Ejemplo de meses de periodo de gracia
    tiempo_credito_maximo = cantidad_periodos * 2  # Tiempo máximo del crédito es el doble del periodo de estudio
    num_cuotas_finales = tiempo_credito_maximo * 6  # Máximo doble de semestres de estudio

    # Inicialización
    saldo_periodo = 0
    cuota_fija = ingresos_mensuales
    afim_total = valor_solicitado * 0.02  # 2% del valor solicitado
    cuota_afim_mensual = afim_total / (cantidad_periodos * meses_gracia)  # Distribuir AFIM en todos los meses

    # Dataframe durante los estudios
    data_mientras_estudias = []

    for semestre in range(cantidad_periodos):
        for mes in range(meses_gracia):
            if mes == 0:
                saldo_periodo += valor_solicitado  # Sumar el valor solicitado en el primer mes de cada semestre

            intereses = saldo_periodo * tasa_interes_mensual
            abono_capital = cuota_fija - intereses - cuota_afim_mensual
            if abono_capital < 0:
                abono_capital = 0
                cuota_fija = intereses + cuota_afim_mensual

            saldo_periodo -= abono_capital

            # Asegurarse de que el saldo no sea negativo
            saldo_periodo = max(saldo_periodo, 0)

            # Actualizar la tabla
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

    # Calcular la cuota ideal que asegure que el saldo se pague completamente en num_cuotas_finales
    if saldo_inicial_post_estudios > 0:
        cuota_ideal = saldo_inicial_post_estudios * tasa_interes_mensual / (1 - (1 + tasa_interes_mensual)**-num_cuotas_finales)

        for mes in range(num_cuotas_finales):
            if saldo_inicial_post_estudios <= 0:
                break
            intereses = saldo_inicial_post_estudios * tasa_interes_mensual
            abono_capital = cuota_ideal - intereses
            saldo_inicial_post_estudios -= abono_capital

            # Asegurarse de que el saldo no sea negativo
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

    # Convertir las listas en DataFrames
    df_mientras_estudias = pd.DataFrame(data_mientras_estudias)
    df_finalizado_estudios = pd.DataFrame(data_finalizado_estudios)

    return df_mientras_estudias, df_finalizado_estudios, saldo_final, cuota_ideal

# Función para calcular el costo total del crédito
def calcular_costo_total(valor_solicitado, tasa_interes_mensual, cantidad_periodos, meses_gracia):
    # Simular el plan de pagos con la tasa dada
    df_mientras_estudias, df_finalizado_estudios, saldo_final, cuota_ideal = simular_plan_pagos(
        valor_solicitado,
        cantidad_periodos,
        ingresos_mensuales,
        tasa_interes_mensual
    )

    total_pagado_capital = df_finalizado_estudios["Abono Capital"].sum() + df_mientras_estudias["Abono Capital"].sum()
    total_pagado_intereses = df_finalizado_estudios["Abono Intereses"].sum() + df_mientras_estudias["Abono Intereses"].sum()
    
    return total_pagado_capital, total_pagado_intereses, total_pagado_capital + total_pagado_intereses

# Función para mostrar comparación con otras entidades
def mostrar_comparacion(valor_solicitado, cantidad_periodos, ingresos_mensuales):
    tasa_interes_nuestra = 0.0116  # Tasa mensual de nuestra entidad

    total_pagado_nuestra = calcular_costo_total(valor_solicitado, tasa_interes_nuestra, cantidad_periodos, 6)
    
    st.subheader("Comparación con Otras Entidades Financieras")
    
    resultados_comparacion = []
    
    for entidad, tasa_interes in tasas_competencia.items():
        total_pagado_competencia = calcular_costo_total(valor_solicitado, tasa_interes, cantidad_periodos, 6)
        ahorro_potencial = total_pagado_competencia[2] - total_pagado_nuestra[2]
        
        resultados_comparacion.append({
            "Entidad": entidad,
            "Valor Desembolsado": valor_solicitado * cantidad_periodos,
            "Total Crédito": total_pagado_competencia[2],
            "Intereses Pagados": total_pagado_competencia[1],
            "Ahorro Potencial": ahorro_potencial
        })
    
    df_comparacion = pd.DataFrame(resultados_comparacion)
    
    # Gráfica de comparación
    st.subheader("Gráfica de Comparación con Otras Entidades Financieras")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    df_comparacion.set_index("Entidad")["Total Crédito"].plot(kind='bar', ax=ax, color=COLOR_ICETEX_PRIMARY)
    
    ax.set_title('Comparación del Total Crédito Pagado con Otras Entidades Financieras')
    ax.set_ylabel('Total Crédito Pagado')
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    
    st.pyplot(fig)
    
    return df_comparacion

# Mostrar KPIs
def mostrar_kpis(df_mientras_estudias, df_finalizado_estudios, cuota_ideal, valor_solicitado, total_cuotas):
    st.subheader("KPIs de la Simulación de Crédito")
    
    total_pagado_capital, total_pagado_intereses, total_pagado = calcular_costo_total(valor_solicitado, 0.0116, total_cuotas, 6)
    
    st.metric("Total Valor Solicitado", f"${valor_solicitado:,.2f}")
    st.metric("Total Pagado (Capital + Intereses)", f"${total_pagado:,.2f}")
    st.metric("Total Intereses Pagados", f"${total_pagado_intereses:,.2f}")
    st.metric("Cuota Ideal Post Estudios", f"${cuota_ideal:,.2f}")
    st.metric("Número Total de Cuotas", f"{total_cuotas}")

# Ejecutar el código de la aplicación
if submit_button:
    # Simula el plan de pagos
    df_mientras_estudias, df_finalizado_estudios, saldo_final, cuota_ideal = simular_plan_pagos(
        valor_solicitado, cantidad_periodos, ingresos_mensuales, 0.0116
    )
    
    # Muestra los KPIs
    mostrar_kpis(df_mientras_estudias, df_finalizado_estudios, cuota_ideal, valor_solicitado, cantidad_periodos)
    
    # Muestra la comparación con otras entidades
    df_comparacion = mostrar_comparacion(valor_solicitado, cantidad_periodos, ingresos_mensuales)
    
    # Genera y muestra el PDF
    pdf_bytes = generar_pdf(valor_solicitado, cantidad_periodos, ingresos_mensuales, cuota_ideal, saldo_final >= 0)
    
    st.download_button(
        label="Descargar PDF",
        data=pdf_bytes,
        file_name="resumen_solicitud_credito.pdf",
        mime="application/pdf"
    )
elif clear_button:
    st.caching.clear_cache()
    st.write("Formulario limpiado. Por favor, completa de nuevo los datos.")

