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

    st.write("### Lista de usuarios")

    # Tabla en HTML para mayor control del layout
    tabla_html = """
    <style>
    .tabla-usuarios {
        width: 100%;
        border-collapse: collapse;
        font-family: "Roboto Condensed", Arial, sans-serif;
        font-size: 15px;
    }
    .tabla-usuarios th, .tabla-usuarios td {
        border-bottom: 1px solid #eee;
        padding: 4px 8px;
        text-align: left;
        vertical-align: middle;
    }
    .tabla-usuarios th {
        background-color: #f5f5f5;
        font-weight: bold;
    }
    .tabla-usuarios tr:last-child td {
        border-bottom: none;
    }
    </style>
    <table class="tabla-usuarios">
      <thead>
        <tr>
          <th style="width: 25%;">Nombre</th>
          <th style="width: 55%;">Correo</th>
          <th style="width: 20%;">Acción</th>
        </tr>
      </thead>
      <tbody>
    """
    st.markdown(tabla_html, unsafe_allow_html=True)

    # Usar columnas para los botones de eliminar junto a la tabla
    for i, row in datos_pagina.iterrows():
        cols = st.columns([0.25, 0.55, 0.2])
        with cols[0]:
            st.markdown(f"<div style='padding:4px 0'>{row['Nombre']}</div>", unsafe_allow_html=True)
        with cols[1]:
            st.markdown(f"<div style='padding:4px 0'>{row['Correo']}</div>", unsafe_allow_html=True)
        with cols[2]:
            eliminar_btn = st.button("🗑️ Eliminar", key=f"eliminar_{inicio + i}", help="Eliminar este usuario")
            if eliminar_btn:
                datos = datos.drop(datos.index[inicio + i]).reset_index(drop=True)
                guardar_datos(datos)
                st.success("¡Contacto eliminado correctamente!")
                st.experimental_rerun()

    # Cierre de tabla (visual, no funcional en Streamlit)
    st.markdown("</tbody></table>", unsafe_allow_html=True)

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
