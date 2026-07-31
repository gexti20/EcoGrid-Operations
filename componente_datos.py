"""Componente 1: Lector de Telemetría (Ingesta y Validación de Datos)

Este componente realiza el cargado, limpieza, conversión de fechas
y tipado estricto de las lecturas IoT para la red eléctrica EcoGrid.
"""

import pandas as pd


def cargar_y_validar_telemetria_grid(filepath_or_buffer) -> pd.DataFrame:
    """Carga y sanitiza los datos de telemetría IoT de la red eléctrica.

    En esta función desarrollo la ingesta de datos desde un archivo CSV o
    stream, asegurando la conversión de formatos de fecha, el tratamiento de
    nulos en generación y la asignación estricta de tipos de datos requeridos por
    el contrato del proyecto.

    Parámetros:
        filepath_or_buffer: Ruta del archivo CSV o stream de datos IoT.

    Retorna:
        pd.DataFrame: DataFrame validado según la especificación exacta.
    """
    # 1. Cargar el dataset desde la fuente de entrada (CSV o Buffer)
    df = pd.read_csv(filepath_or_buffer)

    # Limpiar posibles espacios en blanco en los nombres de las columnas
    df.columns = df.columns.str.strip()

    # 2. Convertir la columna 'timestamp' al formato estricto datetime64[ns]
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    # 3. Reemplazar lecturas nulas en 'generacion_kwh' por 0.0
    if "generacion_kwh" in df.columns:
        df["generacion_kwh"] = df["generacion_kwh"].fillna(0.0)

    # 4. Asignación explícita del contrato de tipos de datos Pandas
    # Se convierte 'fuente_generacion' a string y los valores numéricos a float64
    if "fuente_generacion" in df.columns:
        df["fuente_generacion"] = df["fuente_generacion"].astype(str)

    columnas_float = ["generacion_kwh", "demanda_kwh", "costo_mwh_eur"]
    for col in columnas_float:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
            df[col] = df[col].astype("float64")

    # 5. Retornar el DataFrame validado listo para los demás componentes
    return df
