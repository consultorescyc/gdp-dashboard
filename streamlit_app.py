import streamlit as st
import pandas as pd
import math
from pathlib import Path
import os

# Configuración de la página
st.set_page_config(
    page_title="GDP dashboard",
    page_icon="🌍",
)

st.title("Registro de usuarios")

# Archivo de usuarios
archivo = "usuarios.csv"

# Función para leer los datos
def leer_datos():
    if os.path.exists(archivo):
        try:
            datos = pd.read_csv(archivo)
        except Exception:
            datos = pd.DataFrame(columns=["Nombre", "Correo"])
    else:
        datos = pd.DataFrame(columns=["Nombre", "Correo"])
    return datos

# Función para guardar los datos
def guardar_datos(df):
    df.to_csv(archivo, index=False)

# Formulario
with st.form("registro_form"):
    nombre = st.text_input("Nombre")
    correo = st.text_input("Correo electrónico")
    enviar = st.form_submit_button("Guardar")

# Cargar los datos actuales
datos = leer_datos()

# Guardar datos si no existe el correo
if enviar and nombre and correo:
    # Validar que el correo no exista
    if correo in datos["Correo"].values:
        st.warning("El correo electrónico ya está registrado.")
    else:
        nuevo_dato = pd.DataFrame([[nombre, correo]], columns=["Nombre", "Correo"])
        datos = pd.concat([datos, nuevo_dato], ignore_index=True)
        guardar_datos(datos)
        st.success("¡Datos guardados correctamente!")

st.markdown("---")

# Mostrar lista de usuarios almacenados con paginación y eliminación
st.subheader("Usuarios registrados")

datos = leer_datos()
total_contactos = len(datos)

if not datos.empty:
    # Mostrar cantidad de contactos guardados
    st.info(f"Cantidad total de contactos guardados: {total_contactos}")

    # Paginación
    registros_por_pagina = 10
    total_paginas = math.ceil(total_contactos / registros_por_pagina)
    pagina = st.number_input(
        "Página", min_value=1, max_value=total_paginas, value=1, step=1, key="paginacion"
    )

    inicio = (pagina - 1) * registros_por_pagina
    fin = inicio + registros_por_pagina
    datos_pagina = datos.iloc[inicio:fin].reset_index(drop=True)

    # Mostrar los datos en la página actual
    st.dataframe(datos_pagina)

    # Selección para eliminar
    eliminar_idx = st.selectbox(
        "Selecciona el contacto a eliminar (índice de la tabla mostrada):",
        options=list(datos_pagina.index),
        format_func=lambda x: f"{datos_pagina.iloc[x]['Nombre']} - {datos_pagina.iloc[x]['Correo']}" if not datos_pagina.empty else "",
        key="select_eliminar"
    )

    if st.button("Eliminar contacto seleccionado"):
        # Calcular el índice real en el DataFrame original
        idx_real = inicio + eliminar_idx
        datos = datos.drop(datos.index[idx_real]).reset_index(drop=True)
        guardar_datos(datos)
        st.success("¡Contacto eliminado correctamente!")
        st.experimental_rerun()
else:
    st.info("No hay usuarios registrados aún.")
