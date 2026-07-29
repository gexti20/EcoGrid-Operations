"""
Componente 3: Predicción de Picos

Este componente estima el pico máximo de demanda eléctrica para el
siguiente intervalo horario utilizando la demanda máxima registrada
y un margen de seguridad operacional.
"""

import pandas as pd


def estimar_pico_demanda_futuro(df: pd.DataFrame) -> float:
    """
    Estima el pico de demanda eléctrica para el siguiente intervalo horario.

    Parámetros:
        df (pd.DataFrame): DataFrame validado con la información de la red.

    Retorna:
        float: Pico de demanda proyectado (kWh).
    """

    # Verificar que el DataFrame no esté vacío
    if df.empty:
        return 0.0

    # Obtener la demanda máxima registrada
    demanda_maxima = df["demanda_kwh"].max()

    # Margen de seguridad operacional
    margen_seguridad = 0.10

    # Calcular el pico de demanda proyectado
    pico_demanda = demanda_maxima * (1 + margen_seguridad)

    # Devolver el resultado redondeado a dos decimales
    return round(pico_demanda, 2)