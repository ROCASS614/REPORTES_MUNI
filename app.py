import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Sistema de Gestión y Reportes Municipales",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🛡️ Sistema de Gestión y Reportes Municipales - Transportes")
st.markdown("---")

@st.cache_data
def preparar_casilleros_equipos():
    try:
        # Cargamos la lista de inspectores (omitiendo cabeceras innecesarias)
        df_insp = pd.read_excel("LISTA INSPECTORES 2025 (1).xlsx", skiprows=3)
        df_insp = df_insp.dropna(subset=['APELLIDOS Y NOMBRES'])
        
        # Limpiamos y seleccionamos solo el nombre (sin DNI)
        nombres = df_insp['APELLIDOS Y NOMBRES'].reset_index(drop=True)
        
        # Equipos reales según tu registro de inventario
        # Radios asignadas oficialmente
        radios_dict = {
            1: "9800108",  # Miguel Angel Ortega (Subgerente)
            2: "9800109",  # Jonathan Anderson Barboza
            4: "9800111",  # Katherine Vanessa Calua
            4: "9800112"   # Movilidad Grúa
        }
        
        # Bodycams asignadas oficialmente
        bodycams_dict = {
            1: "GTS0155",  # Pako Omar Cruzado
            3: "GTS0150",  # Norma Cruzado y Vanessa Calua
            18: "GTS0154", # Alvaro Alonso Tacilla
            5: "GTS0152",  # Jennifer Julissa Renteria
            4: "GTS0153",  # Movilidad Grúa
            16: "GTS0151"  # Nicolas Tolentino Caja
        }
        
        # Armamos la tabla limpia sin DNI
        lista_datos = []
        for idx, nombre in enumerate(nombres, start=1):
            # Buscar si tiene radio o body asignada por índice o coincidencia
            radio_asig = "Sin Radio"
            body_asig = "Sin Bodycam"
            
            # Asignaciones directas según inventario oficial
            if idx == 34:  # Jonathan Barboza
                radio_asig = "9800109"
            elif idx == 35:  # Katherine Calua
                radio_asig = "9800111"
            elif idx == 33:  # Subgerente Miguel Ortega
                radio_asig = "9800108"
            elif idx == 37:  # Norma Cruzado
                body_asig = "GTS0150"
            elif idx == 35:  # Vanessa Calua
                body_asig = "GTS0150"
            elif idx == 19:  # Alvaro Tacilla
                body_asig = "GTS0154"
            elif idx == 6:   # Jennifer Renteria
                body_asig = "GTS0152"
            
            lista_datos.append({
                "N°": idx,
                "Inspector (Apellidos y Nombres)": nombre,
                "Casillero Radio": radio_asig,
                "Casillero Bodycam": body_asig
            })
            
        return pd.DataFrame(lista_datos), "Casilleros sincronizados con éxito."
    except Exception as e:
        # Datos de respaldo por si acaso
        return pd.DataFrame({
            "N°": [1, 2, 3],
            "Inspector (Apellidos y Nombres)": ["BARBOZA CASAS, ELMER", "GONZALES FLORES, JOSE", "GUTIERREZ VALERA, JAVIER"],
            "Casillero Radio": ["9800109", "Sin Radio", "Sin Radio"],
            "Casillero Bodycam": ["Sin Bodycam", "GTS0150", "Sin Bodycam"]
        }), f"Usando base temporal ({e})"

df_casilleros, mensaje = preparar_casilleros_equipos()

st.success(f"✅ {mensaje}")

# Menú lateral
st.sidebar.header("Control Operativo")
opcion = st.sidebar.selectbox(
    "Seleccione Módulo:",
    [
        "📻 Casilleros de Equipos (Radios y Bodycams)",
        "📊 Resumen General del Personal",
        "📍 Puntos Fijos",
        "🚗 Retiro Vehicular"
    ]
)

if opcion == "📻 Casilleros de Equipos (Radios y Bodycams)":
    st.subheader("📻 Control de Casilleros: Inspectores, Radios y Bodycams")
    st.markdown("Visualización directa del personal y sus equipos portátiles asignados para ir aprendiendo y modificando juntos.")
    
    # Buscador rápido de inspector
    busqueda = st.text_input("🔍 Buscar Inspector por Nombre:")
    if busqueda:
        df_mostrar = df_casilleros[df_casilleros["Inspector (Apellidos y Nombres)"].str.contains(busqueda, case=False, na=False)]
    else:
        df_mostrar = df_casilleros
        
    st.dataframe(df_mostrar, use_container_width=True, hide_index=True)

elif opcion == "📊 Resumen General del Personal":
    st.subheader("📊 Padrón de Inspectores (Sin Datos Sensibles)")
    st.dataframe(df_casilleros[["N°", "Inspector (Apellidos y Nombres)"]], use_container_width=True, hide_index=True)

elif opcion == "📍 Puntos Fijos":
    st.subheader("📍 Monitoreo de Puntos Fijos")
    st.info("Módulo de puntos fijos listo para enlazar con los inspectores de campo.")

elif opcion == "🚗 Retiro Vehicular":
    st.subheader("🚗 Gestión de Retiro y Desalojo Vehicular")
    st.info("Módulo de grúa y liberación de vías en desarrollo.")
         
   
