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
    submit_button = st.form_submit_button(label='Enviar Solicitud y Simulación')
    clear_button = st.form_submit_button(label='Limpiar Datos', help="Haz clic aquí para limpiar todos los datos del formulario")

# Función para calcular la viabilidad del crédito
def calcular_viabilidad(ingresos, valor_solicitado, cantidad_periodos, total_cuotas):
    if ingresos == 0:
        return False, 0  # Previene división por cero
    # Total meses durante los estudios
    total_meses_estudios = cantidad_periodos * 6  # 6 meses por semestre
    promedio_cuota = total_cuotas / total_meses_estudios  # Promedio de las cuotas mensuales
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

# Función para simular el plan de pagos con AFIM
def simular_plan_pagos(valor_solicitado, cantidad_periodos, ingresos_mensuales):
    meses_gracia = 6  # Ejemplo de meses de periodo de gracia
    tiempo_credito_maximo = cantidad_periodos * 2  # Tiempo máximo del crédito es el doble del periodo de estudio
    tasa_interes_mensual = 0.0116  # Tasa mensual (1.16%)
    tasa_afim = 0.02  # 2% de AFIM por desembolso

    # Inicialización
    saldo_periodo = 0  # Inicia en 0, ya que el saldo inicial se suma en el primer mes de cada semestre

    # Dataframe durante los estudios
    data_mientras_estudias = []
    for semestre in range(cantidad_periodos):
        afim = valor_solicitado * tasa_afim  # Cálculo del AFIM para este semestre
        afim_mensual = afim / 6  # Distribuir el AFIM en los 6 meses del semestre
        
        for mes in range(6):  # 6 meses por semestre
            if mes == 0:
                saldo_periodo += valor_solicitado  # Sumar el valor solicitado en el primer mes de cada semestre

            if saldo_periodo <= 0:
                break  # No hacer cálculos si el saldo es cero o negativo
            
            intereses = saldo_periodo * tasa_interes_mensual  # Intereses mensuales

            # Cuota mensual incluye el AFIM, los intereses y el pago de capital
            cuota_mensual = ingresos_mensuales + afim_mensual
            abono_capital = max(0, ingresos_mensuales - intereses)  # Abono a capital si es posible
            saldo_periodo = saldo_periodo + intereses - abono_capital

            # Actualizar la tabla
            data_mientras_estudias.append({
                "Semestre": f"Semestre {semestre+1}",
                "Mes": mes + 1 + semestre * 6,
                "Cuota Mensual": cuota_mensual,
                "AFIM": afim_mensual,
                "Abono Capital": abono_capital,
                "Abono Intereses": intereses,
                "Saldo": saldo_periodo
            })

    # Convertir la lista en DataFrame
    df_mientras_estudias = pd.DataFrame(data_mientras_estudias)

    return df_mientras_estudias

# Función para simular el plan de pagos después de finalizar los estudios
def simular_plan_pagos_post_estudios(valor_solicitado, cantidad_periodos, ingresos_mensuales):
    meses_gracia = 6  # Ejemplo de meses de periodo de gracia
    tiempo_credito_maximo = cantidad_periodos * 2  # Tiempo máximo del crédito es el doble del periodo de estudio
    tasa_interes_mensual = 0.0116  # Tasa mensual (1.16%)
    
    saldo_pendiente = valor_solicitado
    cuota_mensual = ingresos_mensuales

    # Dataframe después de los estudios
    data_post_estudios = []
    for mes in range(tiempo_credito_maximo):
        intereses = saldo_pendiente * tasa_interes_mensual  # Intereses mensuales
        abono_capital = cuota_mensual - intereses  # Abono a capital si es posible
        saldo_pendiente = saldo_pendiente - abono_capital

        # Ajustar la cuota mensual del último mes para que el saldo sea cero
        if mes == tiempo_credito_maximo - 1:
            cuota_mensual = saldo_pendiente + intereses
            abono_capital = saldo_pendiente

        # Actualizar la tabla
        data_post_estudios.append({
            "Mes": mes + 1,
            "Cuota Mensual": cuota_mensual,
            "Abono Capital": abono_capital,
            "Abono Intereses": intereses,
            "Saldo": saldo_pendiente
        })

    # Convertir la lista en DataFrame
    df_post_estudios = pd.DataFrame(data_post_estudios)

    return df_post_estudios

# Lógica para ejecutar y mostrar resultados
if submit_button:
    # Simular el plan de pagos durante los estudios
    df_mientras_estudias = simular_plan_pagos(
        valor_solicitado,
        cantidad_periodos,
        ingresos_mensuales
    )

    # Simular el plan de pagos después de finalizar los estudios
    df_post_estudios = simular_plan_pagos_post_estudios(
        valor_solicitado,
        cantidad_periodos,
        ingresos_mensuales
    )
    
    # Calcular el promedio de cuota
    total_cuotas = df_post_estudios["Cuota Mensual"].sum()
    viable, promedio_cuota = calcular_viabilidad(
        ingresos_mensuales,
        valor_solicitado,
        cantidad_periodos,
        total_cuotas
    )
    
    # Mostrar DataFrames
    st.write("Resumen de pagos durante los estudios:")
    st.dataframe(df_mientras_estudias)
    
    st.write("Resumen de pagos después de finalizar los estudios:")
    st.dataframe(df_post_estudios)
    
    # Generar PDF
    generar_pdf(
        valor_solicitado,
        cantidad_periodos,
        ingresos_mensuales,
        promedio_cuota,
        viable
    )

    # Mensaje de viabilidad
    if viable:
        st.success("La solicitud es viable con los ingresos actuales.")
    else:
        st.warning("La solicitud no es viable con los ingresos actuales. La simulación se muestra para tu referencia.")
    
# Limpiar datos si se presiona el botón de limpiar
if clear_button:
    st.experimental_rerun()

