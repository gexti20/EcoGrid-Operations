

import pandas as pd


def cargar_y_validar_telemetria_grid(filepath_or_buffer) -> pd.DataFrame:
    

    
    df = pd.read_csv(filepath_or_buffer)

    
    df.columns = df.columns.str.strip()

    
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    
    if "generacion_kwh" in df.columns:
        df["generacion_kwh"] = df["generacion_kwh"].fillna(0.0)

    
    if "fuente_generacion" in df.columns:
        df["fuente_generacion"] = df["fuente_generacion"].astype(str)

    columnas_float = ["generacion_kwh", "demanda_kwh", "costo_mwh_eur"]
    for col in columnas_float:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)
            df[col] = df[col].astype("float64")

    
    return df
