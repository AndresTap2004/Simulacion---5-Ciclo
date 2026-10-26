"""Carga y valida los datos poblacionales desde un archivo CSV."""

from pathlib import Path

import numpy as np
import pandas as pd


COLUMNAS_REQUERIDAS = {"tiempo", "poblacion"}


def cargar_datos(ruta: Path) -> pd.DataFrame:
    """Lee el CSV y valida tiempos ordenados y poblaciones no negativas."""
    if not ruta.is_file():
        raise FileNotFoundError(f"No se encontró el archivo de datos: {ruta}")

    datos = pd.read_csv(ruta)
    faltantes = COLUMNAS_REQUERIDAS.difference(datos.columns)
    if faltantes:
        columnas = ", ".join(sorted(faltantes))
        raise ValueError(f"Al CSV le faltan las columnas requeridas: {columnas}")
    if len(datos) < 2:
        raise ValueError("El CSV debe contener al menos dos observaciones.")

    datos = datos.loc[:, ["tiempo", "poblacion"]].copy()
    datos["tiempo"] = pd.to_numeric(datos["tiempo"], errors="raise")
    datos["poblacion"] = pd.to_numeric(datos["poblacion"], errors="raise")
    valores = datos[["tiempo", "poblacion"]].to_numpy(dtype=float)
    if not np.isfinite(valores).all():
        raise ValueError("Los tiempos y poblaciones deben ser valores finitos.")
    if (datos["poblacion"] < 0).any():
        raise ValueError("La población no puede ser negativa.")

    diferencias = datos["tiempo"].diff().dropna()
    if (diferencias <= 0).any():
        raise ValueError("Los tiempos deben ser únicos y estar ordenados.")
    if not np.allclose(diferencias, 1.0):
        raise ValueError(
            "Los tiempos deben representar períodos consecutivos separados por una unidad."
        )

    return datos.reset_index(drop=True)
