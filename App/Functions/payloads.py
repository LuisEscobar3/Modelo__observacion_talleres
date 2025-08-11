# App/Functions/payloads.py
from __future__ import annotations
import polars as pl
from typing import Dict, Any

def build_json_para_n8n(df: pl.DataFrame) -> Dict[str, Any]:
    """
    Recibe un DataFrame de Polars y devuelve un diccionario con la clave 'registros'
    que contiene una lista de diccionarios con las columnas:
    NUMERO AVISO, NUMERO SINIESTRO, PLACA, FECHA OBSERVACION,
    USUARIO, ROL ANALISTA, OBSERVACION
    """
    columnas = [
        "NUMERO AVISO",
        "NUMERO SINIESTRO",
        "PLACA",
        "FECHA OBSERVACION",
        "USUARIO",
        "ROL ANALISTA",
        "OBSERVACION",
    ]
    df_sel = df.select(columnas)
    return {
        "registros": df_sel.to_dicts()
    }
