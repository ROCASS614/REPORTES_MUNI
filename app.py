import datetime
from io import BytesIO
import openpyxl
import pandas as pd
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Gestión y Reportes Municipales",
    page_icon="🛡️",
    layout="wide",
)

# Estilos visuales personalizados
st.markdown("""
<style>
.main { background-color: #0e1117; color: #ffffff; }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Sistema de Gestión y Reportes Municipales")
st.write("¡Aplicación conectada y lista en la nube!")
