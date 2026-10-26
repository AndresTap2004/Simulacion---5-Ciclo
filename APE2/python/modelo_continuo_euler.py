"""Modelo de crecimiento continuo aproximado mediante Euler."""

import numpy as np


def modelo_continuo_euler(
    p0: float, r: float, tiempos: np.ndarray, dt: float
) -> np.ndarray:
    """Integra dP/dt=rP con pasos de Euler hasta cada tiempo solicitado."""
    tiempos = np.asarray(tiempos, dtype=float)
    if tiempos.ndim != 1 or tiempos.size == 0:
        raise ValueError("Se requiere un arreglo unidimensional de tiempos.")
    if not np.isfinite(tiempos).all() or (np.diff(tiempos) <= 0).any():
        raise ValueError("Los tiempos deben ser finitos, únicos y crecientes.")
    if not np.isfinite(dt) or dt <= 0:
        raise ValueError("dt debe ser un número finito mayor que cero.")

    resultado = np.empty(tiempos.size, dtype=float)
    poblacion = float(p0)
    tiempo_actual = float(tiempos[0])
    resultado[0] = poblacion

    for posicion, tiempo_objetivo in enumerate(tiempos[1:], start=1):
        while tiempo_actual < tiempo_objetivo:
            paso = min(dt, float(tiempo_objetivo - tiempo_actual))
            poblacion += paso * r * poblacion
            tiempo_actual += paso
        resultado[posicion] = poblacion
    return resultado
