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

def validar_antecedentes(deudor, fecha_antecedentes):
    if (datetime.now() - fecha_antecedentes).days < 90:
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
    
    # Inicializar listas en el estado de sesión si no existen
    if 'ofertas_enviadas' not in st.session_state:
        st.session_state.ofertas_enviadas = []
    
    if 'ofertas_en_proceso' not in st.session_state:
        st.session_state.ofertas_en_proceso = []

    beneficiarios_validados = st.session_state['beneficiarios_validados']
    beneficiarios_con_errores = st.session_state['beneficiarios_con_errores']

    # Mostrar cuántos beneficiarios pasaron las validaciones
    st.subheader(f"{len(beneficiarios_validados)} beneficiarios pasaron todas las validaciones")
    
    # Mostrar ofertas ya enviadas
    if st.session_state.ofertas_enviadas:
        st.write("Ofertas ya enviadas:")
        for oferta in st.session_state.ofertas_enviadas:
            st.write(oferta)

    if len(beneficiarios_validados) > 0:
        # Botón para enviar la oferta a todos los beneficiarios que pasaron las validaciones
        if st.button("Enviar oferta a todos los beneficiarios validados"):
            for beneficiario in beneficiarios_validados:
                # Agregar beneficiarios validados a la lista de ofertas enviadas y en proceso
                oferta = beneficiario.copy()
                oferta["Interesado"] = random.choice(["Sí", "No", "Sí, pero después"])  # Asignar interés aleatorio
                oferta["GarantiaFirmada"] = random.choice([True, False])  # Asignar garantía aleatoria
                st.session_state.ofertas_enviadas.append(oferta)
                st.session_state.ofertas_en_proceso.append({
                    "Nombre": beneficiario["Nombre"],
                    "Estado": "Enviada",
                    "Interesado": oferta["Interesado"],
                    "GarantiaFirmada": oferta["GarantiaFirmada"]
                })
            st.success("Ofertas enviadas a todos los beneficiarios que pasaron las validaciones.")
        else:
            st.info("No se han enviado ofertas todavía.")

    # Mostrar cuántos beneficiarios tienen errores
    st.subheader(f"{len(beneficiarios_con_errores)} beneficiarios tienen errores")
    
    if len(beneficiarios_con_errores) > 0:
        # Información de que no se enviarán ofertas a beneficiarios con errores
        st.info("No se enviarán ofertas a los beneficiarios con errores.")

# Página de gestión comercial de ofertas
def gestion_comercial():
    st.title("Gestión Comercial de Ofertas Enviadas")

    # Verificar si hay ofertas en proceso
    if 'ofertas_en_proceso' not in st.session_state or not st.session_state.ofertas_en_proceso:
        st.warning("No hay ofertas en proceso para gestionar.")
        return

    # Filtros para seleccionar el estado de las ofertas
    estado_filtrado = st.selectbox("Selecciona el estado de la oferta", ["Todos", "Sí", "No", "Sí, pero después"])

    # Inicializar la variable para el estado de garantías
    estado_garantia_filtrado = None

    # Mostrar filtro de Estado de Garantías solo si se selecciona "Sí"
    if estado_filtrado == "Sí":
        estado_garantia_filtrado = st.selectbox("Estado de Garantías", ["Todas", "Garantías Firmadas", "Garantías No Firmadas"])

    # Crear un DataFrame para filtrar las ofertas según el estado
    df_ofertas = pd.DataFrame(st.session_state.ofertas_en_proceso)

    if estado_filtrado != "Todos":
        df_ofertas = df_ofertas[df_ofertas['Interesado'] == estado_filtrado]

    # Filtrar por estado de garantías si se seleccionó "Sí"
    if estado_filtrado == "Sí" and estado_garantia_filtrado != "Todas":
        if estado_garantia_filtrado == "Garantías Firmadas":
            df_ofertas = df_ofertas[df_ofertas['GarantiaFirmada'] == True]
        elif estado_garantia_filtrado == "Garantías No Firmadas":
            df_ofertas = df_ofertas[df_ofertas['GarantiaFirmada'] == False]

    # Informe de seguimiento
    st.subheader("Informe de Seguimiento")

    # Contar interesados y garantías
    total_interesados = df_ofertas[df_ofertas['Interesado'] == "Sí"].shape[0]
    total_no_interesados = df_ofertas[df_ofertas['Interesado'] == "No"].shape[0]
    total_si_pero_despues = df_ofertas[df_ofertas['Interesado'] == "Sí, pero después"].shape[0]

    # Filtrar los que respondieron "Sí" y verificar si hay garantía firmada
    total_garantias_firmadas = df_ofertas[(df_ofertas['Interesado'] == "Sí") & (df_ofertas['GarantiaFirmada'] == True)].shape[0]
    total_garantias_no_firmadas = total_interesados - total_garantias_firmadas if total_interesados > 0 else 0

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
        # Registro de beneficiarios con garantía firmada
        st.session_state.beneficiarios = []  # Inicializar la lista si no existe
        for i, oferta in enumerate(df_ofertas.to_dict('records')):
            st.subheader(f"Oferta {i + 1}: {oferta['Nombre']}")
            st.write(f"Estado: {oferta['Estado']}")
            st.write(f"Interesado: {oferta['Interesado']}")

            # Ajustar la respuesta de garantía firmada
            if oferta['Interesado'] == "No":
                st.write("¿Garantía firmada? No")  # No se firma garantía si no está interesado
            elif oferta['Interesado'] == "Sí":
                st.write(f"¿Garantía firmada? {'Sí'}")
                garantia_firmada = st.checkbox("Garantía firmada recibida", value=True, key=f"garantia_firmada_{i}")
                if garantia_firmada:
                    st.session_state.ofertas_en_proceso[i]['GarantiaFirmada'] = True
                    st.session_state.beneficiarios.append(oferta)  # Agregar a beneficiarios
                    st.write("Gracias, hemos registrado la garantía firmada.")
                else:
                    st.write("Esperando la confirmación de la garantía firmada.")
            elif oferta['Interesado'] == "Sí, pero después":
                st.write("¿Garantía firmada? No se requiere pregunta.")  # No se hace seguimiento de garantías

            if oferta['Interesado'] == "Sí, pero después":
                st.write("Generando marca 'Sí, pero después'...")
                st.session_state.ofertas_en_proceso[i]["Estado"] = "Marca Sí, pero después"
            elif oferta['Interesado'] == "No":
                st.write("Actualizando registros y finalizando el flujo.")
                st.session_state.ofertas_en_proceso.remove(oferta)
                st.success("Registros actualizados y flujo finalizado.")
            elif oferta['Interesado'] == "Sí":
                st.write("Generando marca positiva...")
                st.write("Realizando seguimiento periódico para retomar contacto.")
                
# Generación aleatoria de información bancaria
def generar_info_bancaria():
    return {
        "NIT": random.randint(100000000, 999999999),
        "Nombre IES": random.choice(["Universidad A", "Universidad B", "Universidad C"]),
        "Tipo de Cuenta": random.choice(["Ahorros", "Corriente"]),
        "Numero de Cuenta": random.randint(10000000, 99999999),
        "Nombre del Banco": random.choice(["Banco A", "Banco B", "Banco C"]),
        "Numero de Factura": random.randint(100000, 999999)
    }

# Función para la gestión del ordenador del gasto
def gestion_ordenador_gasto():
    st.title("Gestión Ordenador del Gasto")

    # Asegúrate de que las ofertas en sesión están inicializadas
    if "ofertas_en_proceso" not in st.session_state or not st.session_state.ofertas_en_proceso:
        st.warning("No hay ofertas en proceso para gestionar.")
        return

    # Filtrar las ofertas para solo mostrar las que tienen garantía firmada
    df_ofertas = pd.DataFrame(st.session_state.ofertas_en_proceso)
    df_ofertas = df_ofertas[df_ofertas['GarantiaFirmada'] == True]

    if df_ofertas.empty:
        st.warning("No hay ofertas con garantías firmadas para gestionar.")
        return

    # Procesar cada beneficiario
    for index, beneficiario in enumerate(df_ofertas.to_dict('records')):  # Usar df_ofertas para las ofertas filtradas
        st.subheader(f"Gestión para {beneficiario['Nombre']}")
        
        # Verificar si la IES tiene convenio
        if 'tiene_convenio' not in beneficiario:  # Asegúrate de que existe la clave
            beneficiario['tiene_convenio'] = random.choice(["Sí", "No"])

        # Preguntar si la IES tiene convenio
        if beneficiario['tiene_convenio'] == "No":
            if st.button(f"Solicitar información para giro a {beneficiario['IES']}", key=f"solicitar_{index}"):
                info_bancaria = generar_info_bancaria()  # Asumiendo que esta función genera la info bancaria
                st.write(f"NIT: {info_bancaria['NIT']}")
                st.write(f"Nombre IES: {info_bancaria['Nombre']}")
                st.write(f"Tipo de Cuenta: {info_bancaria['Tipo Cuenta']}")
                st.write(f"Número de Cuenta: {info_bancaria['Numero Cuenta']}")
                st.write(f"Nombre del Banco: {info_bancaria['Nombre Banco']}")
                st.write(f"Número de Factura de Matrícula: {info_bancaria['Numero Factura']}")

                if st.button(f"Confirmar información para giro de {beneficiario['IES']}", key=f"confirmar_{index}"):
                    # Aquí se debe validar la información y continuar con el flujo
                    validacion_info = random.choice(["Sí", "No"])  # Simulación de validación
                    if validacion_info == "Sí":
                        st.success("Validación exitosa. Procediendo a liquidación automática...")
                        # Aquí seguiría el proceso de liquidación automática
                    else:
                        st.warning("La validación de la información ha fallado. Por favor, intente nuevamente.")
        
        elif beneficiario['tiene_convenio'] == "Sí":
            st.success("Iniciando liquidación automática del desembolso...")
            instruccion_giro = f"Instrucción de giro generada para {beneficiario['Nombre']}."
            st.write(instruccion_giro)
            alertas_presupuestales = "Alertas generadas sobre el cumplimiento del presupuesto."
            st.write(alertas_presupuestales)

    if st.button("Aprobar Digitalmente", key="aprobar"):
        st.success("Aprobación digital registrada por el ordenador del gasto.")
        giro_exitoso = random.choice(["Sí", "No"])  # Simulación de éxito en el giro
        st.write(f"Giro Exitoso: {giro_exitoso}")

        if giro_exitoso == "Sí":
            st.success("Información enviada para creación de cartera y notificación al beneficiario.")
        else:
            subsanacion = st.radio("¿Se puede subsanar?", ["Sí", "No"], key="subsanacion")
            if subsanacion == "Sí":
                st.write("Solicitando nueva información para giro...")
                # Lógica para solicitar nueva información
            else:
                st.error("Notificando inconsistencia y finalizando el proceso.")


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


