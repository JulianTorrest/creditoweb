import streamlit as st
import pandas as pd
from fpdf import FPDF

# Título de la página
st.title("Solicitud de Crédito Educativo - ICETEX")

# Estilo de encabezado
st.markdown("""
    <style>
    .stApp {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 5px;
        font-size: 16px;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    .stDataFrame {
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Formulario combinado
with st.form(key='credito_y_simulacion_form'):
    st.header("Formulario de Solicitud y Simulación")
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
    meses_gracia = 6  # Ejemplo de meses de periodo de gracia
    tiempo_credito_maximo = cantidad_periodos * 2  # Tiempo máximo del crédito es el doble del periodo de estudio
    num_cuotas_finales = tiempo_credito_maximo * 6  # Máximo doble de semestres de estudio
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
            
            if ingresos_mensuales > 0:
                intereses = saldo_periodo * tasa_interes_mensual  # Intereses mensuales
                if ingresos_mensuales >= intereses:
                    abono_capital = ingresos_mensuales - intereses  # Abono a capital
                    cuota_mensual = ingresos_mensuales
                else:
                    abono_capital = 0
                    cuota_mensual = intereses  # Cuota solo cubre intereses
                # Ajustar el saldo
                saldo_periodo = saldo_periodo + intereses - abono_capital
                abono_intereses = intereses
            else:
                # Si la cuota mensual es cero
                intereses = saldo_periodo * tasa_interes_mensual  # Intereses mensuales
                abono_capital = 0
                cuota_mensual = 0  # Cuota mensual es cero
                abono_intereses = 0  # No hay abono a intereses cuando la cuota es cero
                # Ajustar el saldo
                saldo_periodo = saldo_periodo + intereses
            
            # Actualizar la tabla
            data_mientras_estudias.append({
                "Semestre": f"Semestre {semestre+1}",
                "Mes": mes + 1 + semestre * 6,
                "Cuota Mensual": cuota_mensual,
                "Abono Capital": abono_capital,
                "Abono Intereses": abono_intereses,
                "Saldo": saldo_periodo
            })

    # Saldo final después de estudios
    saldo_final = saldo_periodo
    data_finalizado_estudios = []
    saldo_final_total = saldo_final  # Saldo final a ajustar

    # Calcular saldo inicial para después de estudios
    saldo_inicial_post_estudios = saldo_final

    for mes in range(tiempo_credito_maximo * 6):  # Total meses después de estudios
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
            "Saldo": saldo_inicial_post_estudios
        })

    # Si queda saldo remanente, distribuirlo equitativamente en las cuotas
    if saldo_final_total > 0 and len(data_finalizado_estudios) > 0:
        cuota_extra = saldo_final_total / len(data_finalizado_estudios)
        for entry in data_finalizado_estudios:
            entry["Cuota Mensual"] += cuota_extra
            # Recalcular los abonos
            intereses = entry["Saldo"] * tasa_interes_mensual
            entry["Abono Intereses"] = intereses
            entry["Abono Capital"] = entry["Cuota Mensual"] - intereses
            entry["Saldo"] -= entry["Abono Capital"]
            # Asegurarse que el saldo no sea negativo
            if entry["Saldo"] < 0:
                entry["Saldo"] = 0
                entry["Cuota Mensual"] = entry["Abono Capital"] + entry["Abono Intereses"]
                break  # Salir del bucle si el saldo es 0

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
    
    # Mostrar tablas
    st.subheader("Resumen de Pagos Durante los Estudios")
    st.dataframe(df_mientras_estudias)
    
    st.subheader("Resumen de Pagos Después de Finalizar los Estudios")
    st.dataframe(df_finalizado_estudios)
    
    # Verificar viabilidad
    viable, promedio_cuota = calcular_viabilidad(
        ingresos_mensuales,
        valor_solicitado,
        cantidad_periodos,
        cuota_mensual_post_estudios,
        df_finalizado_estudios['Cuota Mensual'].sum()  # Total cuotas finales
    )
    
    # Generar PDF
    generar_pdf(
        valor_solicitado,
        cantidad_periodos,
        ingresos_mensuales,
        promedio_cuota,
        viable
    )
    
    st.success("¡Solicitud y simulación completadas con éxito!")
    
    # Enlace para descargar el PDF
    with open("resumen_credito.pdf", "rb") as f:
        st.download_button(
            label="Descargar Resumen en PDF",
            data=f,
            file_name="resumen_credito.pdf",
            mime="application/pdf"
        )

if clear_button:
    st.caching.clear_cache()
    st.experimental_rerun()
