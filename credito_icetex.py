import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from fpdf import FPDF
from io import BytesIO
import tempfile

# Título de la página
st.title("Formulario de Crédito Educativo")

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

# Función para generar gráficos
def crear_graficos(df_mientras_estudias, df_finalizado_estudios):
    fig, ax = plt.subplots(2, 1, figsize=(10, 12))
    
    # Gráfico del saldo durante los estudios
    ax[0].plot(df_mientras_estudias["Mes"], df_mientras_estudias["Saldo"], marker='o', color='blue', label="Saldo")
    ax[0].set_xlabel("Mes")
    ax[0].set_ylabel("Saldo")
    ax[0].set_title("Evolución del Saldo durante los Estudios")
    ax[0].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax[0].xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    
    # Gráfico del saldo después de los estudios
    ax[1].plot(df_finalizado_estudios["Mes"], df_finalizado_estudios["Saldo"], marker='o', color='red', label="Saldo")
    ax[1].set_xlabel("Mes")
    ax[1].set_ylabel("Saldo")
    ax[1].set_title("Evolución del Saldo después de los Estudios")
    ax[1].yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax[1].xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    
    fig.tight_layout()
    
    # Guardar gráfico en archivo temporal
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    plt.savefig(temp_file.name, format='png')
    plt.close(fig)
    
    return temp_file.name

# Función para generar el PDF
def generar_pdf(valor_solicitado, cantidad_periodos, ingresos_mensuales, promedio_cuota, viable, df_mientras_estudias, df_finalizado_estudios, cuota_ideal):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Título
    pdf.cell(200, 10, txt="Resumen de Solicitud de Crédito Educativo - ICETEX", ln=True, align='C')
    pdf.ln(10)
    
    # Información del crédito
    pdf.cell(200, 10, txt=f"Valor solicitado por periodo académico: ${valor_solicitado:,}", ln=True)
    pdf.cell(200, 10, txt=f"Cantidad de periodos a financiar: {cantidad_periodos}", ln=True)
    pdf.cell(200, 10, txt=f"Pago mensual promedio: ${promedio_cuota:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Pago mensual mientras estudias: ${ingresos_mensuales:,}", ln=True)
    
    if viable:
        pdf.cell(200, 10, txt="La solicitud es viable con los ingresos actuales.", ln=True)
    else:
        pdf.cell(200, 10, txt="La solicitud no es viable con los ingresos actuales. La simulación aún se muestra para tu referencia.", ln=True)
    
    pdf.ln(10)
    
    # Agregar tablas
    pdf.set_font("Arial", size=10)
    
    pdf.cell(200, 10, txt="Resumen de pagos durante los estudios:", ln=True)
    pdf.ln(5)
    
    # Agregar tabla durante los estudios
    col_widths = [30, 20, 30, 30, 30, 30, 30]
    headers = ["Semestre", "Mes", "Cuota Mensual", "Abono Capital", "Abono Intereses", "AFIM", "Saldo"]
    for header, width in zip(headers, col_widths):
        pdf.cell(width, 10, header, border=1)
    pdf.ln()
    
    for i, row in df_mientras_estudias.iterrows():
        pdf.cell(col_widths[0], 10, str(row["Semestre"]), border=1)
        pdf.cell(col_widths[1], 10, str(row["Mes"]), border=1)
        pdf.cell(col_widths[2], 10, f"${row['Cuota Mensual']:.2f}", border=1)
        pdf.cell(col_widths[3], 10, f"${row['Abono Capital']:.2f}", border=1)
        pdf.cell(col_widths[4], 10, f"${row['Abono Intereses']:.2f}", border=1)
        pdf.cell(col_widths[5], 10, f"${row['AFIM']:.2f}", border=1)
        pdf.cell(col_widths[6], 10, f"${row['Saldo']:.2f}", border=1)
        pdf.ln()
    
    pdf.ln(10)
    
    pdf.cell(200, 10, txt="Resumen de pagos después de finalizar los estudios:", ln=True)
    pdf.ln(5)
    
    # Agregar tabla después de los estudios
    for header, width in zip(headers[1:], col_widths[1:]):
        pdf.cell(width, 10, header, border=1)
    pdf.ln()
    
    for i, row in df_finalizado_estudios.iterrows():
        pdf.cell(col_widths[1], 10, str(row["Mes"]), border=1)
        pdf.cell(col_widths[2], 10, f"${row['Cuota Mensual']:.2f}", border=1)
        pdf.cell(col_widths[3], 10, f"${row['Abono Capital']:.2f}", border=1)
        pdf.cell(col_widths[4], 10, f"${row['Abono Intereses']:.2f}", border=1)
        pdf.cell(col_widths[5], 10, "", border=1)  # No AFIM en esta tabla
        pdf.cell(col_widths[6], 10, f"${row['Saldo']:.2f}", border=1)
        pdf.ln()
    
    pdf.ln(10)
    
    # Agregar KPIs
    pdf.cell(200, 10, txt="KPIs Estratégicos y Tácticos", ln=True)
    pdf.ln(5)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Total Intereses Pagados: ${df_finalizado_estudios['Abono Intereses'].sum() + df_mientras_estudias['Abono Intereses'].sum():,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Total Pagado (Capital + Intereses): ${df_finalizado_estudios['Abono Capital'].sum() + df_finalizado_estudios['Abono Intereses'].sum() + df_mientras_estudias['Abono Capital'].sum() + df_mientras_estudias['Abono Intereses'].sum():,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Duración Total del Crédito (Meses): {len(df_mientras_estudias) + len(df_finalizado_estudios)}", ln=True)
    pdf.cell(200, 10, txt=f"Proporción Capital/Intereses: {df_finalizado_estudios['Abono Capital'].sum() / (df_finalizado_estudios['Abono Intereses'].sum() if df_finalizado_estudios['Abono Intereses'].sum() > 0 else 1):.2f}:1", ln=True)
    pdf.cell(200, 10, txt=f"Cuota Mensual Ideal: ${cuota_ideal:,.2f}", ln=True)
    
    # Agregar gráficos
    temp_img_path = crear_graficos(df_mientras_estudias, df_finalizado_estudios)
    pdf.image(temp_img_path, x=10, y=None, w=190)
    
    # Eliminar archivo temporal
    os.remove(temp_img_path)
    
    # Guardar PDF
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_output.seek(0)
    
    return pdf_output

# Función para simular el plan de pagos
def simular_plan_pagos(valor_solicitado, cantidad_periodos, ingresos_mensuales):
    meses_gracia = 6  # Ejemplo de meses de periodo de gracia
    tiempo_credito_maximo = cantidad_periodos * 2  # Tiempo máximo del crédito es el doble del periodo de estudio
    num_cuotas_finales = tiempo_credito_maximo * 6  # Máximo doble de semestres de estudio
    tasa_interes_mensual = 0.0116  # Tasa mensual (1.16%)

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

# Lógica para ejecutar y mostrar resultados
if submit_button:
    # Simular el plan de pagos
    df_mientras_estudias, df_finalizado_estudios, saldo_final, cuota_ideal = simular_plan_pagos(
        valor_solicitado,
        cantidad_periodos,
        ingresos_mensuales
    )

    # Calcular el promedio de cuota
    total_cuotas = df_mientras_estudias["Cuota Mensual"].sum() + df_finalizado_estudios["Cuota Mensual"].sum()
    total_meses = len(df_mientras_estudias) + len(df_finalizado_estudios)
    viable, promedio_cuota = calcular_viabilidad(
        ingresos_mensuales,
        total_cuotas,
        total_meses
    )
    
    # Mostrar DataFrames
    st.write("Resumen de pagos durante los estudios:")
    st.dataframe(df_mientras_estudias)
    
    st.write("Resumen de pagos después de finalizar los estudios:")
    st.dataframe(df_finalizado_estudios)

    # Generar PDF
    pdf_output = generar_pdf(
        valor_solicitado,
        cantidad_periodos,
        ingresos_mensuales,
        promedio_cuota,
        viable,
        df_mientras_estudias,
        df_finalizado_estudios,
        cuota_ideal
    )

    # Crear enlace para descargar el PDF
    st.download_button(
        label="Descargar PDF de la Simulación",
        data=pdf_output,
        file_name="resumen_credito.pdf",
        mime="application/pdf"
    )

    # Mensaje de viabilidad
    if viable:
        st.success("La solicitud es viable con los ingresos actuales.")
    else:
        st.warning(f"La solicitud no es viable con los ingresos actuales. La simulación se muestra para tu referencia. "
                   f"La cuota mensual simulada es de: ${cuota_ideal:,.2f}.")

    # Mostrar gráficos
    st.subheader("Evolución del Saldo")
    graficar_saldo_mientras_estudias(df_mientras_estudias)
    graficar_saldo_despues_estudios(df_finalizado_estudios)

    st.subheader("Distribución de Pagos Después de los Estudios")
    graficar_distribucion_pagos(df_finalizado_estudios)
    
    # Mostrar KPIs
    mostrar_kpis(df_mientras_estudias, df_finalizado_estudios, cuota_ideal, valor_solicitado, total_cuotas)

# Limpiar datos si se presiona el botón de limpiar
if clear_button:
    valor_solicitado = 0
    cantidad_periodos = 1
    ingresos_mensuales = 0
    st.experimental_rerun()

