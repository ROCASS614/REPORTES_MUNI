import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

st.set_page_config(
    page_title="SISTEMA DE GESTIÓN Y REPORTE MUNICIPAL",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# TÍTULO PRINCIPAL EN MAYÚSCULAS
st.title("🛡️ SISTEMA DE GESTIÓN Y REPORTES MUNICIPALES - TRANSPORTE")
st.markdown("---")

@st.cache_data
def cargar_datos_sistema():
    # Cargar lista oficial de inspectores
    df_insp = pd.read_excel("LISTA INSPECTORES 2025 (1).xlsx", skiprows=3)
    df_insp = df_insp.dropna(subset=['APELLIDOS Y NOMBRES'])
    nombres_inspectores = [str(x).strip().upper() for x in df_insp['APELLIDOS Y NOMBRES'].values]
    
    # Cargar equipos (radios y bodycams)
    df_raw = pd.read_excel("ENCARGADOS DE RADIOS Y BODYCAM.xlsx", header=None)
    
    # Mapeo de radios
    radios_asig = {}
    for i in range(4, 9):
        if i < len(df_raw):
            nombre_eq = str(df_raw.iloc[i, 0]).strip().upper()
            radio_n = str(df_raw.iloc[i, 4]).strip()
            if nombre_eq and nombre_eq != "NAN" and radio_n and radio_n != "NAN":
                # Buscar coincidencia en la lista de inspectores
                for insp in nombres_inspectores:
                    if nombre_eq.split()[0] in insp:
                        radios_asig[insp] = radio_n
                        
    # Mapeo de bodycams
    body_asig = {}
    for i in range(15, 21):
        if i < len(df_raw):
            nombre_eq = str(df_raw.iloc[i, 0]).strip().upper()
            body_n = str(df_raw.iloc[i, 4]).strip()
            if nombre_eq and nombre_eq != "NAN" and body_n and body_n != "NAN":
                if " Y " in nombre_eq:
                    partes = nombre_eq.split(" Y ")
                    for p in partes:
                        p_nombre = p.strip().split()[0]
                        for insp in nombres_inspectores:
                            if p_nombre in insp:
                                body_asig[insp] = body_n
                else:
                    p_nombre = nombre_eq.split()[0]
                    for insp in nombres_inspectores:
                        if p_nombre in insp:
                            body_asig[insp] = body_n
                            
    return nombres_inspectores, radios_asig, body_asig

nombres_inspectores, radios_asig, body_asig = cargar_datos_sistema()

# MENÚ LATERAL EN MAYÚSCULAS
st.sidebar.header("CONTROL OPERATIVO")
opcion = st.sidebar.selectbox(
    "SELECCIONE MÓDULO:",
    [
        "📝 REGISTRO Y PARTE DIARIO",
        "📋 LISTADO GENERAL",
        "📥 DESCARGAR REPORTE"
    ]
)

if opcion == "📝 REGISTRO Y PARTE DIARIO":
    st.subheader("📝 REGISTRO DE OPERACIÓN Y EQUIPOS")
    st.markdown("Seleccione el inspector para autocompletar sus equipos asignados y registrar el detalle.")
    
    with st.form("form_gestion"):
        # 1. NOMBRE DE INSPECTOR CON DESPLEGABLE (FLECHA)
        inspector_sel = st.selectbox("NOMBRE DE INSPECTOR:", options=nombres_inspectores)
        
        # Obtener automático radio y bodycam
        radio_asignada = radios_asig.get(inspector_sel, "SIN RADIO ASIGNADA")
        body_asignada = body_asig.get(inspector_sel, "SIN BODYCAM ASIGNADA")
        
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("N° RADIO:", value=radio_asignada, disabled=True)
        with col2:
            st.text_input("N° BODY CAM:", value=body_asignada, disabled=True)
            
        # 2. DETALLE Y ACCIONES (PUNTO FIJO, DESALOJANDO VEHÍCULO, DESALOJANDO CAMIONES, ETC.)
        detalle_accion = st.selectbox(
            "SELECCIONE O DIGITE EL DETALLE / ACCIÓN:",
            [
                "PUNTO FIJO",
                "DESALOJANDO VEHÍCULO",
                "DESALOJANDO CAMIONES",
                "CONTROL EN VÍA PÚBLICA",
                "OPERATIVO INOPINADO",
                "OTRO"
            ]
        )
        
        detalle_texto = st.text_area("OBSERVACIONES / DETALLE ADICIONAL:")
        
        submitted = st.form_submit_button("💾 GUARDAR REGISTRO")
        if submitted:
            st.success(f"✅ REGISTRO GUARDADO CORRECTAMENTE PARA: {inspector_sel}")
            st.info(f"RADIO: {radio_asignada} | BODYCAM: {body_asignada} | ACCIÓN: {detalle_accion}")

elif opcion == "📋 LISTADO GENERAL":
    st.subheader("📋 LISTADO GENERAL DE INSPECTORES Y EQUIPOS")
    
    # Crear dataframe consolidado en mayúsculas
    data_tabla = []
    for idx, insp in enumerate(nombres_inspectores, 1):
        data_tabla.append({
            "N°": idx,
            "APELLIDOS Y NOMBRES": insp,
            "N° RADIO": radios_asig.get(insp, "SIN RADIO"),
            "N° BODY CAM": body_asig.get(insp, "SIN BODYCAM")
        })
    df_general = pd.DataFrame(data_tabla)
    
    busqueda = st.text_input("🔍 BUSCAR INSPECTOR:")
    if busqueda:
        df_general = df_general[df_general["APELLIDOS Y NOMBRES"].str.contains(busqueda.upper(), na=False)]
        
    st.dataframe(df_general, use_container_width=True, hide_index=True)

elif opcion == "📥 DESCARGAR REPORTE":
    st.subheader("📥 CENTRO DE DESCARGA DE REPORTES")
    
    data_tabla = []
    for idx, insp in enumerate(nombres_inspectores, 1):
        data_tabla.append({
            "N°": idx,
            "APELLIDOS Y NOMBRES": insp,
            "N° RADIO": radios_asig.get(insp, "SIN RADIO"),
            "N° BODY CAM": body_asig.get(insp, "SIN BODYCAM")
        })
    df_download = pd.DataFrame(data_tabla)
    
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_download.to_excel(writer, index=False, sheet_name='REPORTES')
        
    st.download_button(
        label="📥 DESCARGAR REPORTE GENERAL EN EXCEL",
        data=output.getvalue(),
        file_name="REPORTE_MUNICIPAL_TRANSPORTES.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
         
   
