import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from fpdf import FPDF
from io import BytesIO

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

# Función para generar gráficos y agregar al PDF
def graficar_y_guardar(fig, archivo):
    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    archivo.image(buf, x=10, y=None, w=190)  # Ajusta el ancho según sea necesario
    buf.close()

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
        pdf.cell(200, 10, txt="La solicitud no es viable con los ingresos actuales. La simulación aún se muestra para tu referencia.", ln=True)
    
    # Incluir tablas en el PDF
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    
    pdf.cell(200, 10, txt="Resumen de pagos durante los estudios:", ln=True)
    for index, row in df_mientras_estudias.iterrows():
        pdf.cell(200, 10, txt=f"Semestre {row['Semestre']} - Mes {row['Mes']}: Cuota: ${row['Cuota Mensual']}, Abono Capital: ${row['Abono Capital']}, Abono Intereses: ${row['Abono Intereses']}, AFIM: ${row['AFIM']}, Saldo: ${row['Saldo']}", ln=True)
    
    pdf.ln(10)
    pdf.cell(200, 10, txt="Resumen de pagos después de finalizar los estudios:", ln=True)
    for index, row in df_finalizado_estudios.iterrows():
        pdf.cell(200, 10, txt=f"Mes {row['Mes']}: Cuota: ${row['Cuota Mensual']}, Abono Capital: ${row['Abono Capital']}, Abono Intereses: ${row['Abono Intereses']}, Saldo: ${row['Saldo']}", ln=True)

    # Graficar y agregar gráficos al PDF
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Evolución del Saldo durante los Estudios", ln=True)
    fig, ax = plt.subplots()
    ax.plot(df_mientras_estudias["Mes"], df_mientras_estudias["Saldo"], marker='o', color='blue', label="Saldo")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Saldo")
    ax.set_title("Evolución del Saldo durante los Estudios")
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    graficar_y_guardar(fig, pdf)
    plt.close(fig)

    pdf.ln(10)
    pdf.cell(200, 10, txt="Evolución del Saldo después de los Estudios", ln=True)
    fig, ax = plt.subplots()
    ax.plot(df_finalizado_estudios["Mes"], df_finalizado_estudios["Saldo"], marker='o', color='red', label="Saldo")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Saldo")
    ax.set_title("Evolución del Saldo después de los Estudios")
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    graficar_y_guardar(fig, pdf)
    plt.close(fig)

    pdf.ln(10)
    pdf.cell(200, 10, txt="Distribución de Pagos Después de los Estudios", ln=True)
    fig, ax = plt.subplots()
    ax.bar(df_finalizado_estudios.index, df_finalizado_estudios["Abono Capital"], label="Capital", color="blue")
    ax.bar(df_finalizado_estudios.index, df_finalizado_estudios["Abono Intereses"], bottom=df_finalizado_estudios["Abono Capital"], label="Intereses", color="orange")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Valor de la Cuota")
    ax.set_title("Distribución de Pagos después de los Estudios")
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.legend()
    graficar_y_guardar(fig, pdf)
    plt.close(fig)

    pdf.ln(10)
    pdf.cell(200, 10, txt="KPIs Estratégicos y Tácticos", ln=True)
    pdf.cell(200, 10, txt=f"Total Intereses Pagados: ${df_finalizado_estudios['Abono Intereses'].sum() + df_mientras_estudias['Abono Intereses'].sum():,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Total Pagado (Capital + Intereses): ${df_finalizado_estudios['Abono Capital'].sum() + df_mientras_estudias['Abono Capital'].sum() + df_finalizado_estudios['Abono Intereses'].sum() + df_mientras_estudias['Abono Intereses'].sum():,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Duración Total del Crédito (Meses): {len(df_mientras_estudias) + len(df_finalizado_estudios)}", ln=True)
    pdf.cell(200, 10, txt=f"Proporción Capital/Intereses: {df_finalizado_estudios['Abono Capital'].sum() / df_finalizado_estudios['Abono Intereses'].sum():.2f}:1", ln=True)
    pdf.cell(200, 10, txt=f"Cuota Mensual Promedio Post Estudios: ${cuota_ideal:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Saldo Restante después de los Estudios: ${df_finalizado_estudios['Saldo'].iloc[-1]:,.2f}", ln=True)

    pdf.output("resumen_credito.pdf")

# Función para simular el plan de pagos
def simular_plan_pagos(valor_solicitado, cantidad_periodos, ingresos_mensuales, tasa_interes_mensual):
    meses_gracia = 6  # Ejemplo de meses de periodo de gracia
    tiempo_credito_maximo = cantidad_periodos * 2  # Tiempo máximo del crédito es el doble del periodo de estudio
    num_cuotas_finales = tiempo_credito_maximo * 6  # Máximo doble de semestres de estudio

    # Inicialización de los DataFrames para gráficos
    df_mientras_estudias = pd.DataFrame(columns=["Semestre", "Mes", "Cuota Mensual", "Abono Capital", "Abono Intereses", "AFIM", "Saldo"])
    df_finalizado_estudios = pd.DataFrame(columns=["Mes", "Cuota Mensual", "Abono Capital", "Abono Intereses", "Saldo"])

    saldo_actual = valor_solicitado
    cuota_mensual = valor_solicitado * tasa_interes_mensual / (1 - (1 + tasa_interes_mensual) ** (-cantidad_periodos))
    
    for semestre in range(1, cantidad_periodos + 1):
        for mes in range(1, 7):  # 6 meses por semestre
            interes_mensual = saldo_actual * tasa_interes_mensual
            abono_capital = cuota_mensual - interes_mensual
            saldo_actual -= abono_capital
            
            df_mientras_estudias = df_mientras_estudias.append({
                "Semestre": semestre,
                "Mes": mes,
                "Cuota Mensual": cuota_mensual,
                "Abono Capital": abono_capital,
                "Abono Intereses": interes_mensual,
                "AFIM": cuota_mensual - abono_capital - interes_mensual,
                "Saldo": saldo_actual
            }, ignore_index=True)
    
    saldo_actual = valor_solicitado
    for mes in range(1, num_cuotas_finales + 1):
        interes_mensual = saldo_actual * tasa_interes_mensual
        abono_capital = cuota_mensual - interes_mensual
        saldo_actual -= abono_capital
        
        df_finalizado_estudios = df_finalizado_estudios.append({
            "Mes": mes,
            "Cuota Mensual": cuota_mensual,
            "Abono Capital": abono_capital,
            "Abono Intereses": interes_mensual,
            "Saldo": saldo_actual
        }, ignore_index=True)

    return df_mientras_estudias, df_finalizado_estudios, cuota_mensual

# Simular el crédito
if submit_button:
    tasa_interes_mensual = 0.018  # Tasa de interés fija para el ejemplo
    df_mientras_estudias, df_finalizado_estudios, cuota_ideal = simular_plan_pagos(
        valor_solicitado, cantidad_periodos, ingresos_mensuales, tasa_interes_mensual
    )
    
    viable, promedio_cuota = calcular_viabilidad(
        ingresos_mensuales, valor_solicitado, cantidad_periodos * 6
    )
    
    # Generar y mostrar el PDF
    generar_pdf(
        valor_solicitado, cantidad_periodos, ingresos_mensuales, promedio_cuota, viable,
        df_mientras_estudias, df_finalizado_estudios, cuota_ideal
    )
    
    st.success("El PDF ha sido generado exitosamente y guardado como 'resumen_credito.pdf'.")
    
    # Mostrar gráficos
    st.subheader("Evolución del Saldo durante los Estudios")
    st.pyplot(fig)
    st.subheader("Evolución del Saldo después de los Estudios")
    st.pyplot(fig)
    st.subheader("Distribución de Pagos Después de los Estudios")
    st.pyplot(fig)
    
    # Mostrar KPIs
    st.subheader("KPIs Estratégicos y Tácticos")
    st.write(f"Total Intereses Pagados: ${df_finalizado_estudios['Abono Intereses'].sum() + df_mientras_estudias['Abono Intereses'].sum():,.2f}")
    st.write(f"Total Pagado (Capital + Intereses): ${df_finalizado_estudios['Abono Capital'].sum() + df_mientras_estudias['Abono Capital'].sum() + df_finalizado_estudios['Abono Intereses'].sum() + df_mientras_estudias['Abono Intereses'].sum():,.2f}")
    st.write(f"Duración Total del Crédito (Meses): {len(df_mientras_estudias) + len(df_finalizado_estudios)}")
    st.write(f"Proporción Capital/Intereses: {df_finalizado_estudios['Abono Capital'].sum() / df_finalizado_estudios['Abono Intereses'].sum():.2f}:1")
    st.write(f"Cuota Mensual Promedio Post Estudios: ${cuota_ideal:,.2f}")
    st.write(f"Saldo Restante después de los Estudios: ${df_finalizado_estudios['Saldo'].iloc[-1]:,.2f}")

if clear_button:
    st.experimental_rerun()


