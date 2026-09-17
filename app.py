import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Sistema de Gestión y Reportes Municipales",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛡️ Sistema de Gestión y Reportes Municipales")
st.markdown("---")

@st.cache_data
def cargar_datos():
    excel_files = [f for f in os.listdir('.') if f.endswith(('.xlsx', '.xls', '.csv'))]
    if excel_files:
        try:
            df = pd.read_excel(excel_files[0])
            return df, f"Datos cargados desde: {excel_files[0]}"
        except Exception as e:
            return pd.DataFrame(), f"Error al leer archivo: {e}"
    else:
        data = {
            "Inspector": ["Inspector 1", "Inspector 2", "Inspector 3", "Inspector 4"],
            "Ubicación / Calle": ["Jr. Dos de Mayo", "Av. Perú", "Plaza de Armas", "Jr. Junín"],
            "Punto Fijo": ["Sí", "No", "Sí", "Sí"],
            "Estado Vehicular": ["Operativo", "Retirado", "Operativo", "Operativo"]
        }
        return pd.DataFrame(data), "Usando estructura base temporal"

df_inspectores, mensaje_estado = cargar_datos()

st.info(mensaje_estado)

st.sidebar.header("Panel de Control Municipal")
opcion = st.sidebar.selectbox(
    "Seleccione Módulo:",
    ["Resumen General", "Inspectores y Calles", "Puntos Fijos", "Retiro de Vehículos"]
)

if opcion == "Resumen General":
    st.subheader("📊 Panel Operativo General")
    col1, col2, col3 = st.columns(3)
    col1.metric("Inspectores Activos", len(df_inspectores))
    col2.metric("Sectores Monitoreados", "Municipal")
    col3.metric("Estado del Sistema", "Conectado")
    
    st.markdown("### Listado Operativo Reciente")
    st.dataframe(df_inspectores, use_container_width=True)

elif opcion == "Inspectores y Calles":
    st.subheader("👮 Control de Inspectores por Calle")
    st.dataframe(df_inspectores[["Inspector", "Ubicación / Calle"]], use_container_width=True)

elif opcion == "Puntos Fijos":
    st.subheader("📍 Monitoreo de Puntos Fijos")
    st.dataframe(df_inspectores[df_inspectores["Punto Fijo"] == "Sí"], use_container_width=True)

elif opcion == "Retiro de Vehículos":
    st.subheader("🚗 Gestión de Retirando Vehículos")
    st.dataframe(df_inspectores[df_inspectores["Estado Vehicular"] == "Retirado"], use_container_width=True)
