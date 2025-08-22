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

st.markdown("""
# :earth_americas: GDP dashboard

Browse GDP data from the [World Bank Open Data](https://data.worldbank.org/) website. As you'll
notice, the data only goes to 2022 right now, and datapoints for certain years are often missing.
But it's otherwise a great (and did I mention _free_?) source of data.
""")

min_value = int(gdp_df['Year'].min())
max_value = int(gdp_df['Year'].max())

from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])

countries = gdp_df['Country Code'].unique().tolist()

if not countries:
    st.warning("Select at least one country")

selected_countries = st.multiselect(
    'Which countries would you like to view?',
    countries,
    ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN'] if set(['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN']).issubset(countries) else countries[:6]
)

# Filtra los datos
filtered_gdp_df = gdp_df[
    (gdp_df['Country Code'].isin(selected_countries)) &
    (gdp_df['Year'] >= from_year) &
    (gdp_df['Year'] <= to_year)
]

st.header('GDP over time', divider='gray')

st.line_chart(
    filtered_gdp_df,
    x='Year',
    y='GDP',
    color='Country Code',
)

first_year = gdp_df[gdp_df['Year'] == from_year]
last_year = gdp_df[gdp_df['Year'] == to_year]

st.header(f'GDP in {to_year}', divider='gray')

cols = st.columns(4)

for i, country in enumerate(selected_countries):
    col = cols[i % len(cols)]
    try:
        first_gdp = first_year[first_year['Country Code'] == country]['GDP'].iat[0] / 1e9
    except IndexError:
        first_gdp = float('nan')
    try:
        last_gdp = last_year[last_year['Country Code'] == country]['GDP'].iat[0] / 1e9
    except IndexError:
        last_gdp = float('nan')

    if math.isnan(first_gdp) or first_gdp == 0:
        growth = 'n/a'
        delta_color = 'off'
    else:
        growth = f'{last_gdp / first_gdp:,.2f}x'
        delta_color = 'normal'

    col.metric(
        label=f'{country} GDP',
        value=f'{last_gdp:,.0f}B' if not math.isnan(last_gdp) else 'n/a',
        delta=growth,
        delta_color=delta_color
    )
