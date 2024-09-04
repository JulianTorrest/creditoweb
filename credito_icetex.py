import streamlit as st
import pandas as pd
from fpdf import FPDF

# Título de la página
st.title("Solicitud de Crédito Educativo - ICETEX")

# Descripción
st.write("""
Por favor, completa el siguiente formulario para solicitar un crédito educativo con ICETEX.
""")

# Formulario de solicitud de crédito
with st.form(key='credito_form'):
    # Campo 1: Valor solicitado por periodo académico
    valor_solicitado = st.number_input("¿Cuál es el valor solicitado por periodo académico?", min_value=0, step=100000)
    
    # Campo 2: Cantidad de periodos a financiar
    cantidad_periodos = st.number_input("Cantidad de periodos a financiar:", min_value=1, max_value=10, step=1)
    
    # Campo 3: Cuánto puedes pagar mensualmente mientras estudias
    pago_mensual = st.number_input("¿Cuánto puedes pagar mensualmente mientras estudias?", min_value=0, step=10000)
    
    # Botón de enviar
    submit_button = st.form_submit_button(label='Enviar Solicitud')

# Al enviar el formulario
if submit_button:
    st.success(f"Solicitud enviada exitosamente. Valor solicitado: ${valor_solicitado:,}. "
               f"Periodos a financiar: {cantidad_periodos}. Pago mensual: ${pago_mensual:,}.")

# Función para calcular la viabilidad del crédito
def calcular_viabilidad(ingresos, valor_solicitado, cantidad_periodos):
    cuota_maxima = ingresos * 0.3  # 30% de los ingresos como cuota máxima sugerida
    cuota_calculada = valor_solicitado / (cantidad_periodos * 12)  # Cuota mensual estimada
    if cuota_calculada <= cuota_maxima:
        return True, cuota_calculada
    else:
        return False, cuota_calculada

# Función para generar el PDF
def generar_pdf(valor_solicitado, cantidad_periodos, pago_mensual, cuota_calculada):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Resumen de Solicitud de Crédito Educativo - ICETEX", ln=True, align='C')
    pdf.ln(10)
    
    pdf.cell(200, 10, txt=f"Valor solicitado por periodo académico: ${valor_solicitado:,}", ln=True)
    pdf.cell(200, 10, txt=f"Cantidad de periodos a financiar: {cantidad_periodos}", ln=True)
    pdf.cell(200, 10, txt=f"Cuota mensual estimada: ${cuota_calculada:,.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Pago mensual mientras estudias: ${pago_mensual:,}", ln=True)
    
    pdf.output("resumen_credito.pdf")
    st.success("PDF generado exitosamente.")

# Función para simular diferentes escenarios de pago
def simular_pago(valor_solicitado, tasa_interes, plazo):
    tasa_mensual = tasa_interes / 12 / 100
    n = plazo * 12
    cuota_mensual = valor_solicitado * (tasa_mensual * (1 + tasa_mensual) ** n) / ((1 + tasa_mensual) ** n - 1)
    return cuota_mensual

# Función para precalificación
def precalificar(ingresos, valor_solicitado, cantidad_periodos):
    ratio_ingresos = valor_solicitado / (ingresos * cantidad_periodos)
    if ratio_ingresos < 3:  # Regla arbitraria para precalificación
        return True
    else:
        return False

# Sección de viabilidad del crédito
st.header("Cálculo de Viabilidad del Crédito")
ingresos = st.number_input("Ingresos mensuales:", min_value=0, step=100000)
es_viable, cuota_calculada = calcular_viabilidad(ingresos, valor_solicitado, cantidad_periodos)

# Mostrar resultado de viabilidad
if es_viable:
    st.success(f"El crédito es viable. Cuota mensual estimada: ${cuota_calculada:,.2f}")
else:
    st.error(f"El crédito no es viable con los ingresos actuales. Cuota mensual estimada: ${cuota_calculada:,.2f}")

# Botón para generar PDF
if st.button("Generar PDF"):
    generar_pdf(valor_solicitado, cantidad_periodos, pago_mensual, cuota_calculada)

# Simulación de diferentes escenarios de pago
st.header("Simulación de Diferentes Escenarios de Pago")
tasa_interes = st.slider("Tasa de interés anual (%):", 1.0, 20.0, 5.0)
plazo = st.slider("Plazo (años):", 1, 15, 5)
cuota_simulada = simular_pago(valor_solicitado, tasa_interes, plazo)
st.write(f"Con una tasa de interés de {tasa_interes}% y un plazo de {plazo} años, la cuota mensual sería: ${cuota_simulada:,.2f}")

# Precalificación automática
st.header("Precalificación Automática")
precalificado = precalificar(ingresos, valor_solicitado, cantidad_periodos)

# Mostrar resultado de la precalificación
if precalificado:
    st.success("Precalificación aprobada.")
else:
    st.error("Precalificación no aprobada.")

# Comparador de créditos
st.header("Comparador de Créditos")
comparacion_creditos = {
    "Entidad": ["Banco A", "Banco B", "ICETEX"],
    "Tasa de Interés (%)": [8.5, 9.0, 7.5],
    "Cuota Mensual Estimada ($)": [
        simular_pago(valor_solicitado, 8.5, plazo),
        simular_pago(valor_solicitado, 9.0, plazo),
        simular_pago(valor_solicitado, 7.5, plazo)
    ]
}
df_comparacion = pd.DataFrame(comparacion_creditos)
st.write("Comparación de Opciones de Crédito:")
st.dataframe(df_comparacion)

