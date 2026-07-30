import streamlit as st
import pandas as pd
 
from componente_datos import cargar_y_validar_telemetria_grid
from componente_metrica import calcular_balance_energetico
from componente_prediccion import estimar_pico_demanda_futuro
 
st.set_page_config(
    page_title="EcoGrid Operations",
    page_icon="⚡",
    layout="wide"
)
 
st.title("⚡ EcoGrid Operations")
st.subheader("Centro de Control de Smart Grid")
st.write(
    "Visualiza en tiempo real la generación de energía renovable, la demanda "
    "eléctrica, el balance de la red y la predicción de picos de consumo."
)
 
# Inicializamos el estado de la sesión para conservar los datos entre interacciones
if "datos_grid" not in st.session_state:
    st.session_state.datos_grid = pd.DataFrame()
 
# ---------------------------------------------------------------
# Barra lateral
# ---------------------------------------------------------------
st.sidebar.title("Menú")
st.sidebar.markdown("---")
 
archivo = st.sidebar.file_uploader(
    "📂 Selecciona un archivo CSV",
    type=["csv"]
)
 
st.sidebar.markdown("---")
st.sidebar.info(
    "Sube un archivo CSV para visualizar los datos de la Smart Grid."
)
 
# ---------------------------------------------------------------
# Componente 1: Ingesta y validación de datos
# ---------------------------------------------------------------
if archivo:
    try:
        st.session_state.datos_grid = cargar_y_validar_telemetria_grid(archivo)
        st.sidebar.success("✅ Componente de Datos: ingesta y validación exitosas.")
    except Exception as e:
        st.sidebar.error(f"❌ Fallo en la interfaz de datos: {e}")
 
df = st.session_state.datos_grid
 
# ---------------------------------------------------------------
# Si hay datos disponibles, se activan los componentes visuales
# ---------------------------------------------------------------
if not df.empty:
 
    # -------------------------------------------------------
    # Selector interactivo por fuente de generación
    # -------------------------------------------------------
    st.markdown("### 🔍 Filtro por fuente de generación")
 
    fuentes_disponibles = ["Todas"] + sorted(df["fuente_generacion"].unique().tolist())
    fuente_seleccionada = st.selectbox("Selecciona una fuente de generación", fuentes_disponibles)
 
    if fuente_seleccionada == "Todas":
        df_filtrado = df
    else:
        df_filtrado = df[df["fuente_generacion"] == fuente_seleccionada]
 
    st.markdown("---")
 
    # -------------------------------------------------------
    # Componente 2: Métricas de balance energético
    # -------------------------------------------------------
    metricas = calcular_balance_energetico(df_filtrado)
 
    st.markdown("### 📊 Indicadores de balance energético")
 
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Generación total (kWh)", f"{metricas['total_generado_kwh']:.2f}")
    col2.metric("Demanda total (kWh)", f"{metricas['total_demandado_kwh']:.2f}")
    col3.metric("Balance de red (kWh)", f"{metricas['balance_red_kwh']:.2f}")
    col4.metric("CO2 ahorrado (ton)", f"{metricas['co2_ahorrado_ton']:.2f}")
 
    # -------------------------------------------------------
    # Tarjeta visual de alerta según el estado de estabilidad
    # -------------------------------------------------------
    st.markdown("### 🚦 Estado de estabilidad de la red")
 
    if metricas["estado_estabilidad"] == "Estable (Superávit)":
        st.success(f"🟢 {metricas['estado_estabilidad']}: la generación cubre la demanda actual.")
    else:
        st.error(f"🔴 {metricas['estado_estabilidad']}: se recomienda activar el banco de baterías.")
 
    st.markdown("---")
 
    # -------------------------------------------------------
    # Componente 3: Predicción de picos de demanda
    # -------------------------------------------------------
    st.markdown("### 🔮 Predicción de pico de demanda")
 
    pico_estimado = estimar_pico_demanda_futuro(df_filtrado)
    st.metric("Pico de demanda proyectado (kWh)", f"{pico_estimado:.2f}")
 
    if pico_estimado > metricas["total_generado_kwh"]:
        st.warning(
            "⚠️ El pico de demanda proyectado supera la generación total actual. "
            "Evalúa reforzar la capacidad de generación o activar baterías."
        )
 
    st.markdown("---")
 
    # -------------------------------------------------------
    # Registro de datos filtrado
    # -------------------------------------------------------
    st.markdown("### 📋 Registro de datos filtrado")
    st.dataframe(df_filtrado, width="stretch")
 
    # -------------------------------------------------------
    # Visualización de generación vs demanda
    # -------------------------------------------------------
    st.markdown("### 📈 Generación vs Demanda")
    if "timestamp" in df_filtrado.columns:
        datos_grafico = df_filtrado.set_index("timestamp")[["generacion_kwh", "demanda_kwh"]]
    else:
        datos_grafico = df_filtrado[["generacion_kwh", "demanda_kwh"]]
    st.line_chart(datos_grafico)
 
else:
    st.info("👈 Sube un archivo CSV desde la barra lateral para comenzar a visualizar el dashboard.")





