import streamlit as st

# Título de la página
st.title("Solicitud de Crédito Educativo - ICETEX")

# Descripción
st.write("""
Por favor, completa el siguiente formulario para solicitar un crédito educativo con ICETEX.
""")

# Formulario
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
