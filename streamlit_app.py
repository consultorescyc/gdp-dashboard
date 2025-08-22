import streamlit as st
import pandas as pd
import math
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
    st.info(f"Cantidad total de contactos guardados: {total_contactos}")

    # Paginación minimalista
    registros_por_pagina = 10
    total_paginas = max(math.ceil(total_contactos / registros_por_pagina), 1)

    # Estado de la página en session_state
    if "pagina" not in st.session_state:
        st.session_state.pagina = 1

    # Calcular inicio y fin
    inicio = (st.session_state.pagina - 1) * registros_por_pagina
    fin = inicio + registros_por_pagina
    datos_pagina = datos.iloc[inicio:fin].reset_index(drop=True)

    # Fuente compacta y lista más cerrada (fuente Roboto Condensed, o Arial si no está disponible)
    st.write("### Lista de usuarios")
    for i, row in datos_pagina.iterrows():
        st.markdown(
            f"""
            <div style='
                display:flex;
                align-items:center;
                justify-content:space-between;
                font-family:"Roboto Condensed", Arial, sans-serif;
                font-size:15px;
                padding:2px 0 2px 0;
                border-bottom:1px solid #eee;
            '>
                <span style='width:5%'>{row["Nombre"]}</span>
                <span style='width:50%'>{row["Correo"]}</span>
            </div>
            """,
            unsafe_allow_html=True,
        
        )
        eliminar_btn = st.button("🗑️", key=f"eliminar_{inicio + i}", help="Eliminar este usuario")
        if eliminar_btn:
            datos = datos.drop(datos.index[inicio + i]).reset_index(drop=True)
            guardar_datos(datos)
            st.success("¡Contacto eliminado correctamente!")
            st.experimental_rerun()

        

    # Navegación minimalista debajo de la lista
    st.markdown("---")
    col_prev, col_page, col_next = st.columns([1, 2, 1])
    with col_prev:
        if st.session_state.pagina > 1:
            if st.button("⬅️", key="prev"):
                st.session_state.pagina -= 1
                st.experimental_rerun()
    with col_page:
        st.markdown(
            f"<div style='text-align: center;'>Página <b>{st.session_state.pagina}</b> de <b>{total_paginas}</b></div>",
            unsafe_allow_html=True,
        )
    with col_next:
        if st.session_state.pagina < total_paginas:
            if st.button("➡️", key="next"):
                st.session_state.pagina += 1
                st.experimental_rerun()
else:
    st.info("No hay usuarios registrados aún.")
