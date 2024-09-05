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
def calcular_viabilidad(ingresos, valor_solicitado, cantidad_periodos, cuota_mensual_post_estudios, df_finalizado_estudios):
    if ingresos == 0:
        return False, 0, 0  # Previene división por cero
    saldo_final = df_finalizado_estudios['Saldo'].iloc[-1] if not df_finalizado_estudios.empty else 0
    viable = saldo_final <= 0
    promedio_cuota = df_finalizado_estudios['Cuota Mensual'].mean() if not df_finalizado_estudios.empty else 0
    return viable, promedio_cuota, saldo_final

# Función para generar el PDF
def generar_pdf(valor_solicitado, cantidad_periodos, ingresos_mensuales, df_mientras_estudias, df_finalizado_estudios, viable, saldo_final):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Resumen de Solicitud de Crédito Educativo - ICETEX", ln=True, align='C')
    pdf.ln(10)
    
    pdf.cell(200, 10, txt=f"Valor solicitado por periodo académico: ${valor_solicitado:,}", ln=True)
    pdf.cell(200, 10, txt=f"Cantidad de periodos a financiar: {cantidad_periodos}", ln=True)
    pdf.cell(200, 10, txt=f"Pago mensual mientras estudias: ${ingresos_mensuales:,}", ln=True)
    
    if viable:
        pdf.cell(200, 10, txt="La solicitud es viable con los ingresos actuales.", ln=True)
    else:
        pdf.cell(200, 10, txt="La solicitud no es viable con los ingresos actuales. La simulación aún se muestra para tu referencia.", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Resumen de Pagos Durante los Estudios", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", size=10)
    pdf.cell(40, 10, txt="Semestre", border=1)
    pdf.cell(30, 10, txt="Mes", border=1)
    pdf.cell(40, 10, txt="Cuota Mensual", border=1)
    pdf.cell(40, 10, txt="Abono Capital", border=1)
    pdf.cell(40, 10, txt="Abono Intereses", border=1)
    pdf.cell(40, 10, txt="Saldo", border=1)
    pdf.ln()
    
    for index, row in df_mientras_estudias.iterrows():
        pdf.cell(40, 10, txt=str(row['Semestre']), border=1)
        pdf.cell(30, 10, txt=str(row['Mes']), border=1)
        pdf.cell(40, 10, txt=f"${row['Cuota Mensual']:.2f}", border=1)
        pdf.cell(40, 10, txt=f"${row['Abono Capital']:.2f}", border=1)
        pdf.cell(40, 10, txt=f"${row['Abono Intereses']:.2f}", border=1)
        pdf.cell(40, 10, txt=f"${row['Saldo']:.2f}", border=1)
        pdf.ln()
    
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Resumen de Pagos Después de Finalizar los Estudios", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", size=10)
    pdf.cell(30, 10, txt="Mes", border=1)
    pdf.cell(40, 10, txt="Cuota Mensual", border=1)
    pdf.cell(40, 10, txt="Abono Capital", border=1)
    pdf.cell(40, 10, txt="Abono Intereses", border=1)
    pdf.cell(40, 10, txt="Saldo", border=1)
    pdf.ln()
    
    for index, row in df_finalizado_estudios.iterrows():
        pdf.cell(30, 10, txt=str(row['Mes']), border=1)
        pdf.cell(40, 10, txt=f"${row['Cuota Mensual']:.2f}", border=1)
        pdf.cell(40, 10, txt=f"${row['Abono Capital']:.2f}", border=1)
        pdf.cell(40, 10, txt=f"${row['Abono Intereses']:.2f}", border=1)
        pdf.cell(40, 10, txt=f"${row['Saldo']:.2f}", border=1)
        pdf.ln()
    
    pdf.ln(10)
    if saldo_final > 0:
        pdf.cell(200, 10, txt=f"Saldo pendiente final: ${saldo_final:.2f}", ln=True)
    
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
                "Semestre": semestre + 1,
                "Mes": mes + 1,
                "Cuota Mensual": cuota_mensual,
                "Abono Capital": abono_capital,
                "Abono Intereses": abono_intereses,
                "Saldo": saldo_periodo
            })
        
        # Fin del semestre
        saldo_periodo += valor_solicitado  # Aumentar el saldo por cada semestre
        
    # Dataframe después de finalizar estudios
    saldo_final = saldo_periodo  # Saldo al final del periodo de estudios
    data_finalizado_estudios = []
    for mes in range(num_cuotas_finales):
        if saldo_final <= 0:
            break  # No hacer cálculos si el saldo es cero o negativo
        
        if cuota_mensual_post_estudios > 0:
            intereses = saldo_final * tasa_interes_mensual  # Intereses mensuales
            if cuota_mensual_post_estudios >= intereses:
                abono_capital = cuota_mensual_post_estudios - intereses  # Abono a capital
                cuota_mensual = cuota_mensual_post_estudios
            else:
                abono_capital = 0
                cuota_mensual = intereses  # Cuota solo cubre intereses
            # Ajustar el saldo
            saldo_final = saldo_final + intereses - abono_capital
            abono_intereses = intereses
        else:
            # Si la cuota mensual es cero
            intereses = saldo_final * tasa_interes_mensual  # Intereses mensuales
            abono_capital = 0
            cuota_mensual = 0  # Cuota mensual es cero
            abono_intereses = 0  # No hay abono a intereses cuando la cuota es cero
            # Ajustar el saldo
            saldo_final = saldo_final + intereses
        
        # Actualizar la tabla
        data_finalizado_estudios.append({
            "Mes": mes + 1,
            "Cuota Mensual": cuota_mensual,
            "Abono Capital": abono_capital,
            "Abono Intereses": abono_intereses,
            "Saldo": saldo_final
        })

    # Crear dataframes
    df_mientras_estudias = pd.DataFrame(data_mientras_estudias)
    df_finalizado_estudios = pd.DataFrame(data_finalizado_estudios)

    return df_mientras_estudias, df_finalizado_estudios, saldo_final

# Función para manejar el envío del formulario
def manejar_formulario(valor_solicitado, cantidad_periodos, ingresos_mensuales, cuota_mensual_post_estudios):
    df_mientras_estudias, df_finalizado_estudios, saldo_final = simular_plan_pagos(valor_solicitado, cantidad_periodos, ingresos_mensuales, cuota_mensual_post_estudios)
    viable, promedio_cuota, saldo_final = calcular_viabilidad(ingresos_mensuales, valor_solicitado, cantidad_periodos, cuota_mensual_post_estudios, df_finalizado_estudios)
    
    st.subheader("Detalles de la Simulación")
    st.write("Datos mientras estudias")
    st.dataframe(df_mientras_estudias)
    
    st.write("Datos después de finalizar los estudios")
    st.dataframe(df_finalizado_estudios)
    
    if viable:
        st.success("¡La solicitud es viable con los ingresos actuales!")
    else:
        st.warning("La solicitud no es viable con los ingresos actuales. Aquí está la simulación para tu referencia.")
    
    # Generar PDF
    generar_pdf(valor_solicitado, cantidad_periodos, ingresos_mensuales, df_mientras_estudias, df_finalizado_estudios, viable, saldo_final)
    
    # Descargar PDF
    with open("resumen_credito.pdf", "rb") as pdf_file:
        st.download_button(
            label="Descargar PDF",
            data=pdf_file,
            file_name="resumen_credito.pdf",
            mime="application/pdf"
        )

# Manejando el formulario
if submit_button:
    manejar_formulario(valor_solicitado, cantidad_periodos, ingresos_mensuales, cuota_mensual_post_estudios)
elif clear_button:
    st.experimental_rerun()

