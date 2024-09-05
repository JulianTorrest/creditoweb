import pandas as pd
from fpdf import FPDF
import streamlit as st

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
    # Total meses durante los estudios
    total_meses_estudios = cantidad_periodos * 6  # 6 meses por semestre
    # Total meses después de estudios (depende de la cantidad de cuotas finales)
    total_meses_post_estudios = len(df_finalizado_estudios)
    # Total meses en el crédito
    total_meses = total_meses_estudios + total_meses_post_estudios
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
    
    pdf.output("resumen_credito.pdf")

# Función para simular el plan de pagos
def simular_plan_pagos(valor_solicitado, cantidad_periodos, ingresos_mensuales, cuota_mensual_post_estudios):
    tasa_interes_mensual = 0.0116  # Tasa mensual (1.16%)

    # Inicialización
    saldo_periodo = 0  # Inicia en 0, ya que el saldo inicial se suma en el primer mes de cada semestre

    # Dataframe durante los estudios
    data_mientras_estudias = []
    for semestre in range(cantidad_periodos):
        for mes in range(6):  # 6 meses por semestre
            if mes == 0:
                saldo_periodo += valor_solicitado  # Sumar el valor solicitado en el primer mes de cada semestre

            if saldo_periodo <= 0:
                break  # No hacer cálculos si el saldo es cero o negativo
            
            intereses = saldo_periodo * tasa_interes_mensual  # Intereses mensuales

            if ingresos_mensuales > 0:
                abono_capital = max(ingresos_mensuales - intereses, 0)  # Abono a capital
                cuota_mensual = ingresos_mensuales  # La cuota mensual es igual a los ingresos mensuales
                saldo_periodo -= abono_capital  # Reducción del saldo por el abono a capital
            else:
                abono_capital = 0  # Sin abono a capital
                cuota_mensual = 0  # Sin cuota mensual
                saldo_periodo += intereses  # El saldo aumenta por los intereses

            # Ajustar el saldo
            saldo_periodo = max(saldo_periodo, 0)  # Asegurar que el saldo no sea negativo
            
            # Actualizar la tabla
            data_mientras_estudias.append({
                "Semestre": f"Semestre {semestre+1}",
                "Mes": mes + 1 + semestre * 6,
                "Cuota Mensual": cuota_mensual,
                "Abono Capital": abono_capital,
                "Abono Intereses": intereses if ingresos_mensuales > 0 else 0,  # Solo mostrar abono a intereses cuando hay cuota
                "Saldo": saldo_periodo
            })

    # Saldo final después de estudios
    saldo_final = saldo_periodo
    data_finalizado_estudios = []
    saldo_inicial_post_estudios = saldo_final
    num_cuotas_finales = (valor_solicitado // cuota_mensual_post_estudios) + 1

    # Calcular cuotas después de los estudios
    for mes in range(num_cuotas_finales):
        if saldo_inicial_post_estudios <= 0:
            break
        intereses = saldo_inicial_post_estudios * tasa_interes_mensual  # Intereses mensuales
        cuota_pago_final = min(cuota_mensual_post_estudios, saldo_inicial_post_estudios + intereses)
        abono_capital = cuota_pago_final - intereses
        saldo_inicial_post_estudios -= abono_capital

        data_finalizado_estudios.append({
            "Mes": mes + 1,
            "Cuota Mensual": cuota_pago_final,
            "Abono Capital": abono_capital,
            "Abono Intereses": intereses,
            "Saldo": max(saldo_inicial_post_estudios, 0)  # Asegurar que el saldo no sea negativo
        })

    # Convertir las listas en DataFrames
    df_mientras_estudias = pd.DataFrame(data_mientras_estudias)
    df_finalizado_estudios = pd.DataFrame(data_finalizado_estudios)

    return df_mientras_estudias, df_finalizado_estudios, saldo_final

# Lógica para ejecutar y mostrar resultados
if submit_button:
    # Simular el plan de pagos
    df_mientras_estudias, df_finalizado_estudios, saldo_final = simular_plan_pagos(
        valor_solicitado,
        cantidad_periodos,
        ingresos_mensuales,
        cuota_mensual_post_estudios
    )

    # Calcular el promedio de cuota
    total_cuotas = df_mientras_estudias["Cuota Mensual"].sum() + df_finalizado_estudios["Cuota Mensual"].sum()
    total_meses = len(df_mientras_estudias) + len(df_finalizado_estudios)
    promedio_cuota_calculado = total_cuotas / total_meses if total_meses > 0 else 0

    # Verificar viabilidad del crédito
    viable, promedio_cuota_calculado = calcular_viabilidad(
        ingresos_mensuales,
        valor_solicitado,
        cantidad_periodos,
        cuota_mensual_post_estudios,
        total_cuotas
    )

    # Generar el PDF
    generar_pdf(
        valor_solicitado,
        cantidad_periodos,
        ingresos_mensuales,
        promedio_cuota_calculado,
        viable
    )

    # Mostrar la viabilidad del crédito
    if viable:
        st.success("¡La solicitud es viable con los ingresos actuales!")
    else:
        st.warning("La solicitud no es viable con los ingresos actuales. Verifica la simulación para más detalles.")
    
    st.write(f"Para que la solicitud sea viable, necesitas poder pagar al menos ${promedio_cuota_calculado:,.2f} por mes.")
    
    # Mostrar DataFrames
    st.subheader("Plan de Pagos durante el Periodo de Estudios")
    st.dataframe(df_mientras_estudias)

    st.subheader("Plan de Pagos después de Estudios")
    st.dataframe(df_finalizado_estudios)
    
if clear_button:
    st.experimental_rerun()
