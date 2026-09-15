import datetime
import os
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Gestión de Reportes - Municipalidad",
    page_icon="🛡️",
    layout="wide",
)

# Estilo visual limpio y profesional
st.markdown(
    """
    <style>
    .main-header {
        font-size: 26px;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 10px;
    }
    .sub-header {
        font-size: 16px;
        color: #4B5563;
        margin-bottom: 25px;
    }
    .card {
        background-color: #F8FAFC;
        padding: 20px;
        border-radius: 8px;
        border-left: 5px solid #2563EB;
        margin-bottom: 15px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Título principal
st.markdown(
    '<div class="main-header">🛡️ Sistema de Gestión y Reportes Municipales</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">Módulo de control operativo, videovigilancia y comunicaciones de campo</div>',
    unsafe_allow_html=True,
)

# Simulación de base de datos local en memoria para la sesión
if "reportes" not in st.session_state:
    st.session_state.reportes = [
        {
            "id": 101,
            "area": "Videovigilancia",
            "operador": "Roca C.",
            "detalle": "Mantenimiento preventivo de cámara domo en sector central.",
            "estado": "Completado",
            "fecha": "2026-09-14",
        },
        {
            "id": 102,
            "area": "Radio Comunicación",
            "operador": "Central Base",
            "detalle": (
                "Revisión de frecuencias y canales de patrullaje nocturno."
            ),
            "estado": "En Proceso",
            "fecha": "2026-09-15",
        },
    ]

# Menú lateral
menu = st.sidebar.selectbox(
    "Menú de Navegación",
    [
        "📋 Ver Reportes Activos",
        "➕ Registrar Nuevo Reporte",
        "📊 Panel de Estadísticas",
    ],
)

if menu == "📋 Ver Reportes Activos":
    st.subheader("Listado General de Incidencias y Reportes")

    # Filtros rápidos
    filtro_estado = st.selectbox(
        "Filtrar por estado", ["Todos", "En Proceso", "Completado"]
    )

    for rep in st.session_state.reportes:
        if filtro_estado == "Todos" or rep["estado"] == filtro_estado:
            color_badge = (
                "🟢" if rep["estado"] == "Completado" else "🟡"
            )
            with st.container():
                st.markdown(
                    f"""
                <div class="card">
                    <b>Reporte #{rep['id']}</b> | <b>Área:</b> {rep['area']} | <b>Responsable:</b> {rep['operador']}<br>
                    <b>Detalle:</b> {rep['detalle']}<br>
                    <b>Estado:</b> {color_badge} {rep['estado']} &nbsp;&nbsp;|&nbsp;&nbsp; <i>Fecha: {rep['fecha']}</i>
                </div>
                """,
                    unsafe_allow_html=True,
                )

elif menu == "➕ Registrar Nuevo Reporte":
    st.subheader("Ingresar Nuevo Registro Operativo")

    with st.form("form_reporte"):
        col1, col2 = st.columns(2)
        with col1:
            area_op = st.selectbox(
                "Área de Operación",
                [
                    "Videovigilancia",
                    "Radio Comunicación",
                    "Cuerpo de Inspectores",
                    "Logística",
                ],
            )
            operador_name = st.text_input(
                "Nombre del Técnico / Operador", value="Roca"
            )
        with col2:
            estado_op = st.selectbox(
                "Estado Inicial", ["En Proceso", "Completado"]
            )
            fecha_op = st.date_input(
                "Fecha del Reporte", datetime.date.today()
            )

        detalle_op = st.text_area(
            "Descripción de la Actividad o Incidencia"
        )

        submit_btn = st.form_submit_button("Guardar y Registrar Reporte")

        if submit_btn:
            if detalle_op.strip() == "":
                st.error("Por favor, ingrese una descripción detallada.")
            else:
                nuevo_id = (
                    st.session_state.reportes[-1]["id"] + 1
                    if st.session_state.reportes
                    else 101
                )
                nuevo_registro = {
                    "id": nuevo_id,
                    "area": area_op,
                    "operador": operador_name,
                    "detalle": detalle_op,
                    "estado": estado_op,
                    "fecha": str(fecha_op),
                }
                st.session_state.reportes.append(nuevo_registro)
                st.success(
                    f"¡Reporte #{nuevo_id} guardado con éxito en el sistema!"
                )

elif menu == "📊 Panel de Estadísticas":
    st.subheader("Resumen y Métricas Generales")

    total_rep = len(st.session_state.reportes)
    completados = sum(
        1 for r in st.session_state.reportes if r["estado"] == "Completado"
    )
    proceso = total_rep - completados

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Registros", total_rep)
    col2.metric("Completados", completados)
    col3.metric("En Proceso", proceso)

    st.markdown("---")
    st.info("Sistema operando de forma autónoma y sincronizada.")