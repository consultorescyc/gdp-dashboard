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

# Formulario
with st.form("registro_form"):
    nombre = st.text_input("Nombre")
    correo = st.text_input("Correo electrónico")
    enviar = st.form_submit_button("Guardar")

# Guardar datos
archivo = "usuarios.csv"
if enviar and nombre and correo:
    nuevo_dato = pd.DataFrame([[nombre, correo]], columns=["Nombre", "Correo"])

    if os.path.exists(archivo):
        try:
            datos = pd.read_csv(archivo)
            datos = pd.concat([datos, nuevo_dato], ignore_index=True)
        except Exception:
            datos = nuevo_dato
    else:
        datos = nuevo_dato

    datos.to_csv(archivo, index=False)
    st.success("¡Datos guardados correctamente!")

# Separador visual
st.markdown("---")

# Mostrar lista de usuarios almacenados
st.subheader("Usuarios registrados")
if os.path.exists(archivo):
    try:
        datos_registrados = pd.read_csv(archivo)
        if not datos_registrados.empty:
            st.dataframe(datos_registrados)
        else:
            st.info("No hay usuarios registrados aún.")
    except Exception:
        st.error("No se pudo leer el archivo de usuarios.")
else:
    st.info("No hay usuarios registrados aún.")
