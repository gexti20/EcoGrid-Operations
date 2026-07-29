import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="EcoGrid Operations",
    page_icon="⚡",
    layout="wide"
)

# Componentes del proyecto
#from componente_datos import cargar_y_validar_telemetria_grid
#from componente_metricas import calcular_balance_energetico
#from componente_prediccion import estimar_pico_demanda_futuro

st.title("⚡ EcoGrid Operations")
st.subheader("Centro de Control de Smart Grid")
st.write(
    "Visualiza en tiempo real la generación de energía renovable, la demanda eléctrica, el balance de la red y la predicción de picos de consumo."
)

# Barra lateral
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
from componentes_datos import IngestorDatos
from componetes_prediccion import MotorPrediccion

ingestor = IngestorDatos
predictor = MotorPrediccion



