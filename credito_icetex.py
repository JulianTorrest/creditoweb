import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from fpdf import FPDF

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
    
    pdf.output("resumen_credito.pdf")

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
            "Intereses Pagados": total_pagado_competencia[1],
            "Total Crédito": total_pagado_competencia[2],
            "Ahorro Potencial": ahorro_potencial
        })
    
    df_comparacion = pd.DataFrame(resultados_comparacion)
    st.dataframe(df_comparacion)

# Funciones para graficar
def graficar_saldo_mientras_estudias(df_mientras_estudias):
    fig, ax = plt.subplots()
    ax.plot(df_mientras_estudias["Mes"], df_mientras_estudias["Saldo"], marker='o', color='blue', label="Saldo")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Saldo")
    ax.set_title("Evolución del Saldo durante los Estudios")

    # Formato de los ejes en números enteros
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    st.pyplot(fig)

def graficar_saldo_despues_estudios(df_finalizado_estudios):
    fig, ax = plt.subplots()
    ax.plot(df_finalizado_estudios["Mes"], df_finalizado_estudios["Saldo"], marker='o', color='red', label="Saldo")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Saldo")
    ax.set_title("Evolución del Saldo después de los Estudios")

    # Formato de los ejes en números enteros
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    st.pyplot(fig)

def graficar_distribucion_pagos(df_finalizado_estudios):
    fig, ax = plt.subplots()
    
    ax.bar(df_finalizado_estudios.index, df_finalizado_estudios["Abono Capital"], label="Capital", color="blue")
    ax.bar(df_finalizado_estudios.index, df_finalizado_estudios["Abono Intereses"], bottom=df_finalizado_estudios["Abono Capital"], label="Intereses", color="orange")

    # Formato de los ejes en números enteros
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

    ax.set_xlabel("Mes")
    ax.set_ylabel("Valor de la Cuota")
    ax.set_title("Distribución de Pagos después de los Estudios")
    ax.legend()
    
    st.pyplot(fig)

def mostrar_kpis(df_mientras_estudias, df_finalizado_estudios, cuota_ideal, valor_solicitado, total_cuotas):
    total_pagado_capital = df_finalizado_estudios["Abono Capital"].sum() + df_mientras_estudias["Abono Capital"].sum()
    total_pagado_intereses = df_finalizado_estudios["Abono Intereses"].sum() + df_mientras_estudias["Abono Intereses"].sum()
    
    # KPIs
    st.subheader("KPIs Estratégicos y Tácticos")
    st.metric("Total Intereses Pagados", f"${total_pagado_intereses:,.2f}")
    st.metric("Total Pagado (Capital + Intereses)", f"${total_pagado_capital + total_pagado_intereses:,.2f}")
    st.metric("Duración Total del Crédito (Meses)", len(df_mientras_estudias) + len(df_finalizado_estudios))
    st.metric("Proporción Capital/Intereses", f"{total_pagado_capital / total_pagado_intereses:.2f}:1")
    st.metric("Cuota Mensual Promedio Post Estudios", f"${cuota_ideal:,.2f}")
    st.metric("Saldo Restante después de los Estudios", f"${df_finalizado_estudios['Saldo'].iloc[-1]:,.2f}")

# Lógica para ejecutar y mostrar resultados
if submit_button:
    # Simular el plan de pagos con nuestra tasa
    df_mientras_estudias, df_finalizado_estudios, saldo_final, cuota_ideal = simular_plan_pagos(
        valor_solicitado,
        cantidad_periodos,
        ingresos_mensuales,
        0.0116  # Tasa mensual de nuestra entidad
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

    # Mostrar comparación con otras entidades
    mostrar_comparacion(valor_solicitado, cantidad_periodos, ingresos_mensuales)

# Limpiar datos si se presiona el botón de limpiar
if clear_button:
    valor_solicitado = 0
    cantidad_periodos = 1
    ingresos_mensuales = 0
    st.experimental_rerun()

