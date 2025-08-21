# App/Functions/reader.py
from __future__ import annotations
import hashlib
import pathlib
from typing import List
import polars as pl

REQUIRED_COLS = [
    "NUMERO AVISO",
    "NUMERO SINIESTRO",
    "NOMBRE TALLER",
    "PLACA",
    "FECHA OBSERVACION",
    "USUARIO",
    "ROL ANALISTA",
    "OBSERVACION",
]

HEADER_HINTS = ("NUMERO AVISO", "PLACA")


def detect_header_start(lines: List[str]) -> int:
    for i, line in enumerate(lines):
        if all(h in line for h in HEADER_HINTS):
            return i
    raise ValueError("No se encontró encabezado de tabla en el CSV.")


def file_fingerprint(path: str) -> str:
    p = pathlib.Path(path)
    base = f"{p.name}|{p.stat().st_size}|{int(p.stat().st_mtime)}"
    return hashlib.sha1(base.encode("utf-8")).hexdigest()


def leer_solo_tabla_csv_filtrado(ruta_csv: str) -> pl.DataFrame:
    with open(ruta_csv, "r", encoding="utf-8") as f:
        lineas = f.readlines()
    start_idx = None
    for i, linea in enumerate(lineas):
        if "NUMERO AVISO" in linea and "PLACA" in linea:
            start_idx = i
            break
    if start_idx is None:
        raise ValueError("No se encontró encabezado de tabla")

    df = pl.read_csv(ruta_csv, skip_rows=start_idx, ignore_errors=True)

    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas requeridas: {missing}")

    df_filtrado = (
        df
        .filter(
            (pl.col("ROL ANALISTA") == "ASESOR DE SERVICIO TALLER")
            & (pl.col("NOMBRE TALLER") == "CARIBE SAS CALI")  # 👈 Nuevo filtro
        )
        .select([
            pl.col("NUMERO AVISO"),
            pl.col("NUMERO SINIESTRO"),
            pl.col("PLACA"),
            pl.col("FECHA OBSERVACION"),
            pl.col("USUARIO"),
            pl.col("ROL ANALISTA"),
            pl.col("NOMBRE TALLER"),  # 👈 Incluyo el taller en el resultado
            pl.col("OBSERVACION"),
        ])
        .sort(["NUMERO SINIESTRO", "FECHA OBSERVACION"])
    )

    df_filtrado = df_filtrado.head(4)
    return df_filtrado


def leer_solo_tabla_csv_filtrado(ruta_csv: str) -> pl.DataFrame:
    with open(ruta_csv, "r", encoding="utf-8") as f:
        lineas = f.readlines()
    start_idx = None
    for i, linea in enumerate(lineas):
        if "NUMERO AVISO" in linea and "PLACA" in linea:
            start_idx = i
            break
    if start_idx is None:
        raise ValueError("No se encontró encabezado de tabla")

    df = pl.read_csv(ruta_csv, skip_rows=start_idx, ignore_errors=True)

    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas requeridas: {missing}")

    df_filtrado = (
        df
        .filter(
            (pl.col("ROL ANALISTA") == "ASESOR DE SERVICIO TALLER")
            & (pl.col("NOMBRE TALLER") == "CARIBE SAS CALI")  # 👈 Nuevo filtro
        )
        .select([
            pl.col("NUMERO AVISO"),
            pl.col("NUMERO SINIESTRO"),
            pl.col("PLACA"),
            pl.col("FECHA OBSERVACION"),
            pl.col("USUARIO"),
            pl.col("ROL ANALISTA"),
            pl.col("NOMBRE TALLER"),  # 👈 Incluyo el taller en el resultado
            pl.col("OBSERVACION"),
        ])
        .sort(["NUMERO SINIESTRO", "FECHA OBSERVACION"])
    )

    df_filtrado = df_filtrado.head(200)
    return df_filtrado
