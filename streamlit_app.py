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
if enviar and nombre and correo:
    nuevo_dato = pd.DataFrame([[nombre, correo]], columns=["Nombre", "Correo"])
    archivo = "usuarios.csv"

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

# -----------------------------------------------------------------------------
# Función para obtener los datos de GDP
@st.cache_data
def get_gdp_data():
    """Obtiene datos de GDP desde un archivo CSV."""
    DATA_FILENAME = Path(__file__).parent / 'data/gdp_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2022

    gdp_df = raw_gdp_df.melt(
        ['Country Name', 'Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'GDP',
    )

    # Convierte años a enteros
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])
    return gdp_df

gdp_df = get_gdp_data()

# -----------------------------------------------------------------------------
# Dashboard de GDP
