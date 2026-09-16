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
st.markdown(
    """
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stTextInput > div > div > input, .stSelectbox > div > div > select, .stTextArea > div > div > textarea {
        background-color: #1a1c24; color: white; border: 1px solid #30363d; border-radius: 6px;
    }
    h1, h2, h3 { color: #58a6ff; }
    </style>
""",
    unsafe_allow_html=True,
)

# Lista completa de inspectores (47 en total)
INSPECTORES = [
    "Abanto Silva, Juan Carlos",
    "Alva Bazán, María Elena",
    "Becerra Vargas, Luis Alberto",
    "Cabrera Cueva, Renato Omar",
    "Campos Rojas, Víctor Manuel",
    "Cerdán Huamán, Rosa María",
    "Chávez Medina, Jorge Luis",
    "Cerdán Silva, Carmen Rosa",
    "Dávila Pinedo, Carlos Enrique",
    "Díaz Sánchez, Ana Lucía",
    "Espinoza Torres, José Antonio",
    "Fernández Coronel, Manuel",
    "Flores Ramos, Patricia Milagros",
    "Gálvez Pérez, Walter Raúl",
    "García Huamán, Segundo",
    "González Medina, Rosa Isela",
    "Guevara Silva, Marco Antonio",
    "Hernández Rojas, Juana",
    "Huamán Cerdán, Pedro Pablo",
    "Llanos Sánchez, Kelly",
    "López Alva, Miguel Ángel",
    "Marín Torres, Carmen",
    "Medina Vargas, Luis Enrique",
    "Mejía Cueva, Rosa",
    "Mendoza Rojas, Carlos",
    "Muñoz Silva, Javier",
    "Narro Pérez, Lucía",
    "Paredes Castillo, Roberto",
    "Pérez Sánchez, Miguel",
    "Pinedo Ramos, Juan",
    "Quispe Mendoza, Ana",
    "Ramos Silva, Carlos",
    "Ríos Torres, María",
    "Rodríguez Alva, José",
    "Rojas Cerdán, Luis",
    "Sánchez Vargas, Rosa",
    "Silva Medina, Pedro",
    "Torres Rojas, Juan",
    "Valera Pérez, Carlos",
    "Vargas Cueva, María",
    "Vásquez Silva, Jorge",
    "Velásquez Ramos, Luis",
    "Zelada Torres, Ana",
    "Zorrilla Medina, Carlos",
    "Zurita Rojas, Rosa",
    "Poma Alva, Manuel",
    "Rázuri Silva, Carmen",
]

# Título Principal
st.markdown(
    "<h1>🛡️ Sistema de Gestión y Reportes Municipales</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h4>Módulo de control operativo, videovigilancia y comunicaciones de"
    " campo</h4>",
    unsafe_allow_html=True,
)
st.markdown("---")

# Menú de Navegación Lateral
menu = st.sidebar.selectbox(
    "Menú de Navegación",
    [
        "Registrar Nuevo Reporte",
        "Ver Registros / Exportar Excel",
        "Control de Equipos (Radios y Bodycams)",
    ],
)

# Inicializar base de datos temporal en memoria si no existe
if "registros" not in st.session_state:
  st.session_state["registros"] = []

if menu == "Registrar Nuevo Reporte":
  st.subheader("Ingresar Nuevo Registro Operativo")

  col1, col2 = st.columns(2)

  with col1:
    area = st.selectbox(
        "Área de Operación",
        [
            "Videovigilancia",
            "Inspección de Tránsito",
            "Radiocomunicaciones",
            "Operativo Conjunto",
        ],
    )
    inspector = st.selectbox(
        "Inspector / Operador Responsable", sorted(INSPECTORES)
    )

  with col2:
    estado = st.selectbox(
        "Estado Inicial", ["En Proceso", "Completado", "Pendiente de Apoyo"]
    )
    fecha_reporte = st.date_input(
        "Fecha del Reporte", datetime.date.today()
    )

  descripcion = st.text_area(
      "Descripción de la Actividad o Incidencia",
      placeholder=(
          "Detalle las novedades del turno, incidencias reportadas por radio o"
          " uso de bodycams..."
      ),
  )

  if st.button("Guardar y Registrar Reporte"):
    if descripcion.strip() == "":
      st.warning(
          "Por favor ingrese una descripción antes de guardar el reporte."
      )
    else:
      nuevo_registro = {
          "Fecha": str(fecha_reporte),
          "Área": area,
          "Inspector": inspector,
          "Estado": estado,
          "Descripción": descripcion,
      }
      st.session_state["registros"].append(nuevo_registro)
      st.success(
          "¡Reporte guardado correctamente en el sistema de la municipalidad!"
      )

elif menu == "Ver Registros / Exportar Excel":
  st.subheader("Historial de Registros Operativos")

  if len(st.session_state["registros"]) == 0:
    st.info("Aún no hay registros guardados en esta sesión.")
  else:
    df = pd.DataFrame(st.session_state["registros"])
    st.dataframe(df, use_container_width=True)

    # Botón para exportar a Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
      df.to_excel(writer, index=False, sheet_name="Reportes_Municipales")
    excel_data = output.getvalue()

    st.download_button(
        label="📥 Descargar Reporte en Excel",
        data=excel_data,
        file_name=f"Reportes_Municipales_{datetime.date.today()}.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        ),
    )

elif menu == "Control de Equipos (Radios y Bodycams)":
  st.subheader("Control de Asignación de Equipos de Campo")
  st.markdown(
      "Asigne radios portátiles y cámaras corporales (bodycams) a los inspectores"
      " en turno:"
  )

  inspector_equipo = st.selectbox(
      "Seleccionar Inspector", sorted(INSPECTORES), key="eq_inspector"
  )
  radio_code = st.text_input(
      "Código de Radio Portátil Asignada (Ej: RAD-014)"
  )
  bodycam_code = st.text_input(
      "Código de Bodycam Asignada (Ej: BCAM-008)"
  )

  if st.button("Registrar Asignación de Equipo"):
    st.success(
        f"Equipo registrado con éxito para el inspector {inspector_equipo}:"
        f" Radio [{radio_code}] | Bodycam [{bodycam_code}]"
    )


