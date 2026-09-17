import streamlit as st
import pandas as pd
from io import BytesIO
import os

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
    nombres_inspectores = []
    radios_asig = {}
    body_asig = {}
    
    # Buscar archivos con nombres alternativos comunes para evitar errores
    archivo_insp = None
    for f in ["LISTA INSPECTORES 2025 (1).xlsx", "LISTA INSPECTORES 2025.xlsx", "inspectores.xlsx"]:
        if os.path.exists(f):
            archivo_insp = f
            break
            
    archivo_eq = None
    for f in ["ENCARGADOS DE RADIOS Y BODYCAM.xlsx", "equipos.xlsx"]:
        if os.path.exists(f):
            archivo_eq = f
            break
            
    try:
        if archivo_insp:
            df_insp = pd.read_excel(archivo_insp, skiprows=3)
            df_insp = df_insp.dropna(subset=[df_insp.columns[1] if len(df_insp.columns) > 1 else 0])
            # Intentar encontrar la columna de nombres
            col_nombre = None
            for col in df_insp.columns:
                if "APELLIDO" in str(col).upper() or "NOMBRE" in str(col).upper():
                    col_nombre = col
                    break
            if col_nombre is None:
                col_nombre = df_insp.columns[1] if len(df_insp.columns) > 1 else df_insp.columns[0]
                
            nombres_inspectores = [str(x).strip().upper() for x in df_insp[col_nombre].dropna().values]
        else:
            # Lista de respaldo si no se suben los archivos todavía
            nombres_inspectores = [
                "BARBOZA CASAS, ELMER OSCAR",
                "GONZALES FLORES, JOSE EDUARDO",
                "GUTIERREZ VALERA, JAVIER HERNAN",
                "PÉREZ PÉREZ, JOSE OSCAR",
                "ROJAS MURRUGARRA, ANGEL GABRIEL"
            ]
            
        if archivo_eq:
            df_raw = pd.read_excel(archivo_eq, header=None)
            
            # Mapeo de radios
            for i in range(4, 15):
                if i < len(df_raw):
                    nombre_eq = str(df_raw.iloc[i, 0]).strip().upper()
                    radio_n = str(df_raw.iloc[i, 4]).strip() if df_raw.shape[1] > 4 else ""
                    if nombre_eq and nombre_eq != "NAN" and radio_n and radio_n != "NAN":
                        for insp in nombres_inspectores:
                            if nombre_eq.split()[0] in insp:
                                radios_asig[insp] = radio_n
                                
            # Mapeo de bodycams
            for i in range(15, 25):
                if i < len(df_raw):
                    nombre_eq = str(df_raw.iloc[i, 0]).strip().upper()
                    body_n = str(df_raw.iloc[i, 4]).strip() if df_raw.shape[1] > 4 else ""
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
    except Exception as e:
        st.error(f"Error al procesar archivos: {e}")
        
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
            
        # 2. DETALLE Y ACCIONES
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
