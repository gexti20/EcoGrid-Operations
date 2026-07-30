import pandas as pd

def calcular_balance_energetico(df: pd.DataFrame) -> dict:
    """
    En esta función desarrollo la lógica para calcular las métricas operativas 
    de la red eléctrica a partir del DataFrame de telemetría que me entrega el Componente 1.
    
    Parámetros:
        df (pd.DataFrame): DataFrame validado con el contrato de datos.
        
    Retorna:
        dict: Diccionario con los 5 indicadores clave del balance energético.
    """
    # 1. Calculo los Totales Generado y Demandado
    # Obtengo la suma total de las columnas 'generacion_kwh' y 'demanda_kwh'.
    # Las convierto a float de Python para evitar problemas de compatibilidad al exportar.
    total_generado = float(df['generacion_kwh'].sum())
    total_demandado = float(df['demanda_kwh'].sum())
    
    # 2. Calculo el Balance Neto de la Red    # Aplico la fórmula solicitada: Suma(generacion_kwh) - Suma(demanda_kwh)
    balance_red = total_generado - total_demandado
    
    # 3. Estimo las Toneladas de CO2 Ahorradas
    # Aplico la fórmula exacta: (Suma(generacion_kwh) * 0.40) / 1000
    # Multiplico por 0.40 kg/kWh y divido entre 1000 para pasar el resultado a toneladas.
    co2_ahorrado = float((total_generado * 0.40) / 1000)
    
    # 4. Determino el Estado de Estabilidad de la Red
    # Evalúo la condición dada:
    # Si el balance es mayor o igual a 0, considero la red "Estable (Superávit)".
    # De lo contrario, marco "Riesgo Déficit (Activar Baterías)".
    if balance_red >= 0:
        estado = "Estable (Superávit)"
    else:
        estado = "Riesgo Déficit (Activar Baterías)"
        
    # 5. Retorno el Diccionario Final
    # Empaqueto y devuelvo los resultados usando exactamente las claves pedidas
    # para que la app principal (Streamlit) pueda consumirlos sin errores.
    metricas = {
        "total_generado_kwh": total_generado,
        "total_demandado_kwh": total_demandado,
        "balance_red_kwh": balance_red,
        "co2_ahorrado_ton": co2_ahorrado,
        "estado_estabilidad": estado
    }
    
    return metricas