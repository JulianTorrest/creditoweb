import streamlit as st
import pandas as pd
import random
from datetime import datetime
import matplotlib.pyplot as plt


# Crear una función para generar datos ficticios
def generar_datos_ficticios(n):
    nombres = [f"Nombre_{i}" for i in range(n)]
    nacionalidades = ["Colombiano", "Otro"]
    estados_credito = ["Ninguno", "Castigado", "En mora y castigado"]
    listas_sarlaft = ["No está en ninguna lista", "Vinculantes", "Restrictivas", "Informativas"]
    
    datos = []
    for nombre in nombres:
        datos.append({
            "Nombre": nombre,
            "Nacionalidad": random.choice(nacionalidades),
            "Edad": random.randint(18, 65),
            "Estado Crédito": random.choice(estados_credito),
            "Lista SARLAFT": random.choice(listas_sarlaft),
            "Score Crediticio": random.randint(150, 900),
            "Capacidad de Pago (COP)": random.randint(1500000, 20000000),
            "Límite de Endeudamiento (COP)": random.randint(1500000, 20000000)
        })
    return datos

# Inicializar datos
beneficiarios_data = generar_datos_ficticios(500)
if "ofertas_enviadas" not in st.session_state:
    st.session_state.ofertas_enviadas = []
if "ofertas_en_proceso" not in st.session_state:
    st.session_state.ofertas_en_proceso = []

# Funciones de validación
def validar_deudor(deudor):
    if deudor['Nacionalidad'] == 'Colombiano' and deudor['Edad'] < 65:
        if deudor['Estado Crédito'] == 'Castigado':
            return False, "Estado Crédito es Castigado"
        if deudor['Estado Crédito'] == 'En mora y castigado':
            return False, "Estado en Mora/Castigado"
        return True, ""
    return False, "No es colombiano o mayor de 65 años"

def validar_sarlaft(deudor):
    if deudor['Lista SARLAFT'] in ['Vinculantes', 'Restrictivas', 'Informativas']:
        return False, f"Listas SARLAFT: {deudor['Lista SARLAFT']}"
    return True, ""

def validar_antecedentes(deudor,fecha_antecedentes):
    if (datetime.now() - deudor['Antecedentes']).days < 90:
        return False, "Antecedentes menores a 90 días"
    return True, ""

# Procesar validaciones y estadísticas
def procesar_validaciones(beneficiarios):
    validaciones = {
        "Validación 1": {"Aprobados": 0, "No Aprobados": 0, "Motivo No Aprobación": []},
        "Validación 2": {"Aprobados": 0, "No Aprobados": 0},
        "Validación 3": {"Aprobados": 0, "No Aprobados": 0},
    }

    for deudor in beneficiarios.to_dict(orient='records'):
        # Validación 1
        valido1, motivo1 = validar_deudor(deudor)
        if valido1:
            validaciones["Validación 1"]["Aprobados"] += 1
        else:
            validaciones["Validación 1"]["No Aprobados"] += 1
            validaciones["Validación 1"]["Motivo No Aprobación"].append(motivo1)

        # Validación 2
        valido2, motivo2 = validar_sarlaft(deudor)
        if valido2:
            validaciones["Validación 2"]["Aprobados"] += 1
        else:
            validaciones["Validación 2"]["No Aprobados"] += 1

        # Validación 3
        valido3, motivo3 = validar_antecedentes(deudor)
        if valido3:
            validaciones["Validación 3"]["Aprobados"] += 1
        else:
            validaciones["Validación 3"]["No Aprobados"] += 1

    return validaciones
    
# Funciones de la aplicación
def realizar_validaciones(beneficiario):
    errores = []
    if beneficiario["Score Crediticio"] < 200:
        errores.append("Score crediticio muy bajo.")
    if beneficiario["Capacidad de Pago (COP)"] < 3000000:
        errores.append("Capacidad de pago insuficiente.")
    return errores

def firma_garantias(oferta):
    st.write(f"Firmando garantías para {oferta['Nombre']}...")

# Página de captura de datos
def captura_datos():
    st.title("Formulario de Búsqueda de Captura de Datos para ICETEX")
    
    nombre = st.text_input("Nombre completo")
    tipo_documento = st.selectbox("Tipo de Documento", ["Tarjeta de Identidad", "Cédula de Ciudadanía"])
    numero_documento = st.text_input("Número de Documento")
    nacionalidad = st.multiselect("Nacionalidad", ["Colombiano", "Otro"])
    edad = st.slider("Edad", min_value=18, max_value=65, value=(18, 65), step=1)
    estado_credito = st.multiselect("Estado del crédito anterior", ["Ninguno", "Castigado", "En mora y castigado"])
    lista_sarlaft = st.multiselect("Lista SARLAFT", ["No está en ninguna lista", "Vinculantes", "Restrictivas", "Informativas"])
    score_credito = st.slider("Score crediticio", min_value=150, max_value=900, value=(150, 900), step=1)
    capacidad_pago = st.slider("Capacidad de pago (en COP)", min_value=1500000, max_value=20000000, value=(1500000, 20000000), step=10000)
    limite_endeudamiento = st.slider("Límite de endeudamiento (en COP)", min_value=1500000, max_value=20000000, value=(1500000, 20000000), step=10000)
    deudor = st.text_input("Nombre del deudor")  # Ejemplo de captura de datos
    fecha_antecedentes = st.date_input("Fecha de antecedentes", value=datetime.today())

    
    if st.button("Mostrar datos de beneficiarios"):
        df_beneficiarios = pd.DataFrame(beneficiarios_data)
        
        if nacionalidad:
            df_beneficiarios = df_beneficiarios[df_beneficiarios["Nacionalidad"].isin(nacionalidad)]
        if estado_credito:
            df_beneficiarios = df_beneficiarios[df_beneficiarios["Estado Crédito"].isin(estado_credito)]
        if lista_sarlaft:
            df_beneficiarios = df_beneficiarios[df_beneficiarios["Lista SARLAFT"].isin(lista_sarlaft)]
        if edad:
            df_beneficiarios = df_beneficiarios[df_beneficiarios["Edad"].between(edad[0], edad[1])]
        if score_credito:
            df_beneficiarios = df_beneficiarios[df_beneficiarios["Score Crediticio"].between(score_credito[0], score_credito[1])]
        if capacidad_pago:
            df_beneficiarios = df_beneficiarios[df_beneficiarios["Capacidad de Pago (COP)"].between(capacidad_pago[0], capacidad_pago[1])]
        if limite_endeudamiento:
            df_beneficiarios = df_beneficiarios[df_beneficiarios["Límite de Endeudamiento (COP)"].between(limite_endeudamiento[0], limite_endeudamiento[1])]
        
        st.dataframe(df_beneficiarios)

# Página de validación de beneficiarios
def validacion_beneficiarios():
    st.title("Validaciones de Elegibilidad para ICETEX")

    # Paso 1: Listas para almacenar beneficiarios
    beneficiarios_validados = []
    beneficiarios_con_errores = []

    if not beneficiarios_data:
        st.warning("No hay datos de beneficiarios disponibles.")
        return
    
    for i, beneficiario in enumerate(beneficiarios_data):
        st.subheader(f"Beneficiario {i+1}: {beneficiario['Nombre']}")
        
        errores = realizar_validaciones(beneficiario)
        if errores:
            st.error(f"Errores encontrados para {beneficiario['Nombre']}:")
            for error in errores:
                st.write(f"- {error}")
            # Agregar a la lista de beneficiarios con errores
            beneficiarios_con_errores.append(beneficiario)
        else:
            st.success(f"Beneficiario {beneficiario['Nombre']} pasó todas las validaciones.")
            st.write(f"Ofrecer crédito educativo.")
            # Agregar a la lista de beneficiarios validados
            beneficiarios_validados.append(beneficiario)

    # Guardar las listas en el estado para usarlas en otras páginas
    st.session_state['beneficiarios_validados'] = beneficiarios_validados
    st.session_state['beneficiarios_con_errores'] = beneficiarios_con_errores


# Página para enviar la oferta al beneficiario
def enviar_oferta():
    st.title("Enviar Oferta a los Beneficiarios")

    # Verificar si hay datos de beneficiarios validados y con errores
    if 'beneficiarios_validados' not in st.session_state or 'beneficiarios_con_errores' not in st.session_state:
        st.warning("No se ha realizado la validación de beneficiarios.")
        return
    
    beneficiarios_validados = st.session_state['beneficiarios_validados']
    beneficiarios_con_errores = st.session_state['beneficiarios_con_errores']

    # Mostrar cuántos beneficiarios pasaron las validaciones
    st.subheader(f"{len(beneficiarios_validados)} beneficiarios pasaron todas las validaciones")
    
    if len(beneficiarios_validados) > 0:
        # Botón para enviar la oferta a todos los beneficiarios que pasaron las validaciones
        if st.button("Enviar oferta a todos los beneficiarios validados"):
            for beneficiario in beneficiarios_validados:
                # Agregar beneficiarios validados a la lista de ofertas enviadas y en proceso
                st.session_state.ofertas_enviadas.append(beneficiario.copy())
                st.session_state.ofertas_en_proceso.append({
                    "Nombre": beneficiario["Nombre"],
                    "Estado": "Enviada"
                })
            st.success("Ofertas enviadas a todos los beneficiarios que pasaron las validaciones.")
        else:
            st.info("No se han enviado ofertas todavía.")

    # Mostrar cuántos beneficiarios tienen errores
    st.subheader(f"{len(beneficiarios_con_errores)} beneficiarios tienen errores")
    
    if len(beneficiarios_con_errores) > 0:
        # Información de que no se envían ofertas a beneficiarios con errores
        st.info("No se enviarán ofertas a los beneficiarios con errores.")

# Página de gestión comercial de ofertas
def gestion_comercial():
    st.title("Gestión Comercial de Ofertas Enviadas")
    
    if not st.session_state.ofertas_en_proceso:
        st.warning("No hay ofertas en proceso para gestionar.")
        return

    # Filtros para seleccionar el estado de las ofertas
    estado_filtrado = st.selectbox("Selecciona el estado de la oferta", ["Todos", "Sí", "No", "Sí, pero después"])
    
    # Crear un DataFrame para filtrar las ofertas según el estado
    df_ofertas = pd.DataFrame(st.session_state.ofertas_en_proceso)
    
    if estado_filtrado != "Todos":
        df_ofertas = df_ofertas[df_ofertas['Estado'] == estado_filtrado]
    
    # Informe de seguimiento
    st.subheader("Informe de Seguimiento")
    
    total_interesados = sum(1 for oferta in st.session_state.ofertas_en_proceso if oferta.get('Interesado') == "Sí")
    total_no_interesados = sum(1 for oferta in st.session_state.ofertas_en_proceso if oferta.get('Interesado') == "No")
    total_si_pero_despues = sum(1 for oferta in st.session_state.ofertas_en_proceso if oferta.get('Interesado') == "Sí, pero después")
    
    # Filtrar los que respondieron "Sí" y verificar si hay garantía firmada
    total_garantias_firmadas = sum(1 for oferta in st.session_state.ofertas_en_proceso 
                                    if oferta.get('Interesado') == "Sí" and oferta.get('GarantiaFirmada', False))
    
    total_garantias_no_firmadas = total_interesados - total_garantias_firmadas

    # Mostrar informe
    st.write(f"Total ofertas de beneficiarios interesados: {total_interesados}")
    st.write(f"Total ofertas de beneficiarios no interesados: {total_no_interesados}")
    st.write(f"Total ofertas de beneficiarios 'sí, pero después': {total_si_pero_despues}")
    st.write(f"Total garantías firmadas: {total_garantias_firmadas}")
    st.write(f"Total garantías no firmadas: {total_garantias_no_firmadas}")

    # Crear primer gráfico: Distribución de interesados
    st.subheader("Distribución de Interesados")
    labels_interesados = ['Interesados', 'No Interesados', 'Sí, pero después']
    sizes_interesados = [total_interesados, total_no_interesados, total_si_pero_despues]

    plt.figure(figsize=(10, 6))
    plt.pie(sizes_interesados, labels=labels_interesados, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    st.pyplot(plt)

    # Crear segundo gráfico: Garantías firmadas y no firmadas
    st.subheader("Estado de Garantías")
    labels_garantias = ['Garantías Firmadas', 'Garantías No Firmadas']
    sizes_garantias = [total_garantias_firmadas, total_garantias_no_firmadas]

    plt.figure(figsize=(10, 6))
    plt.bar(labels_garantias, sizes_garantias, color=['green', 'red'])
    plt.ylabel('Número de Garantías')
    plt.title('Estado de Garantías Firmadas y No Firmadas')
    st.pyplot(plt)

    # Mostrar las ofertas filtradas
    if not df_ofertas.empty:
        for i, oferta in enumerate(df_ofertas.to_dict('records')):
            st.subheader(f"Oferta {i+1}: {oferta['Nombre']}")
            st.write(f"Estado: {oferta['Estado']}")
            
            # Simulación de respuestas aleatorias para demostración
            oferta['Interesado'] = random.choice(["Sí", "No", "Sí, pero después"])
            oferta['GarantiaFirmada'] = random.choice([True, False]) if oferta['Interesado'] == "Sí" else None
            
            st.session_state.ofertas_en_proceso[i].update(oferta)

            interesado = st.selectbox("¿Está interesado el potencial beneficiario?", ["Sí", "No", "Sí, pero después"], key=f"interesado_{i}")
            st.session_state.ofertas_en_proceso[i]['Interesado'] = interesado
            
            if interesado == "Sí, pero después":
                st.write("Generando marca 'Sí, pero después'...")
                firma_garantias(oferta)
                st.session_state.ofertas_en_proceso[i]["Estado"] = "Marca Sí, pero después"
            elif interesado == "No":
                st.write("Actualizando registros y finalizando el flujo.")
                st.session_state.ofertas_en_proceso[i]["Estado"] = "Finalizada"
                st.session_state.ofertas_en_proceso.remove(oferta)
                st.success("Registros actualizados y flujo finalizado.")
            elif interesado == "Sí":
                st.write("Generando marca positiva...")
                st.write("Realizando seguimiento periódico para retomar contacto.")

                garantia_firmada = st.checkbox("Garantía firmada recibida", key=f"garantia_firmada_{i}")
                
                if garantia_firmada:
                    st.session_state.ofertas_en_proceso[i]['GarantiaFirmada'] = True
                    st.write("Garantía firmada registrada.")

# Página de gestión del ordenador del gasto
def gestion_ordenador_gasto():
    st.title("Gestión Ordenador del Gasto")
    
    if not st.session_state.beneficiarios:
        st.warning("No hay beneficiarios con garantía firmada para gestionar.")
        return

    # Verificar información de la IES para cada beneficiario
    for beneficiario in st.session_state.beneficiarios:
        st.subheader(f"Gestión para {beneficiario['Nombre']}")
        
        # Preguntar si la IES tiene convenio
        tiene_convenio = st.selectbox(f"¿La {beneficiario['IES']} tiene convenio?", ["Selecciona", "Sí", "No"], key=f"convenio_{beneficiario['Nombre']}")
        
        if tiene_convenio == "No":
            info_giro = st.text_input(f"Información para giro a {beneficiario['IES']}", key=f"info_giro_{beneficiario['Nombre']}")
            if st.button("Enviar información", key=f"enviar_{beneficiario['Nombre']}"):
                # Aquí iría la lógica para procesar la información de giro
                st.success("Información enviada para giro. Esperando confirmación del beneficiario.")
                # Simulación de validación
                # Puedes implementar lógica adicional para verificar que el beneficiario envíe la información
                # Asumimos que la validación es exitosa
                st.session_state.beneficiarios.remove(beneficiario)
        elif tiene_convenio == "Sí":
            # Liquidación automática de desembolso
            st.success("Iniciando liquidación automática del desembolso...")
            # Aquí iría la lógica para la liquidación automática
            instruccion_giro = f"Instrucción de giro generada para {beneficiario['Nombre']}."
            st.write(instruccion_giro)

            # Control presupuestal
            alertas_presupuestales = "Alertas generadas sobre el cumplimiento del presupuesto."
            st.write(alertas_presupuestales)

    # Botón para aprobación digital
    if st.button("Aprobar Digitalmente", key="aprobar"):
        st.success("Aprobación digital registrada por el ordenador del gasto.")

# Llamar a la función principal
gestion_ordenador_gasto()

#Pagina de creación de indicadores 
def Indicadores_Proceso():
    st.title("Dashboard")

    if st.button("Generar Estadísticas"):
        validaciones_resultado = procesar_validaciones(beneficiarios_data)

        st.subheader("Validación 1")
        st.write(f"Aprobados: {validaciones_resultado['Validación 1']['Aprobados']}")
        st.write(f"No Aprobados: {validaciones_resultado['Validación 1']['No Aprobados']}")
        st.write("Motivos de No Aprobación:")
        st.write(validaciones_resultado['Validación 1']['Motivo No Aprobación'])

        st.subheader("Validación 2")
        st.write(f"Aprobados: {validaciones_resultado['Validación 2']['Aprobados']}")
        st.write(f"No Aprobados: {validaciones_resultado['Validación 2']['No Aprobados']}")

        st.subheader("Validación 3")
        st.write(f"Aprobados: {validaciones_resultado['Validación 3']['Aprobados']}")
        st.write(f"No Aprobados: {validaciones_resultado['Validación 3']['No Aprobados']}")

# Configurar el menú de la aplicación
menu = st.sidebar.selectbox(
    "Selecciona una página",
    ["Captura de Datos", "Validación de Beneficiarios", "Enviar Oferta", "Gestión Comercial", "Gestión Ordenador del Gasto", "Indicadores Proceso"]
)

# Ejecutar la página seleccionada
if menu == "Captura de Datos":
    captura_datos()
elif menu == "Validación de Beneficiarios":
    validacion_beneficiarios()
elif menu == "Enviar Oferta":
    enviar_oferta()
elif menu == "Gestión Comercial":
    gestion_comercial()
elif menu == "Gestión Ordenador del Gasto":
    gestion_ordenador_gasto()
elif menu == "Indicadores Proceso":
    Indicadores_Proceso()
