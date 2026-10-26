"""Estimación de parámetros para los modelos de crecimiento poblacional."""

from dataclasses import dataclass

import numpy as np
from scipy.optimize import curve_fit


@dataclass(frozen=True)
class ParametrosModelo:
    """Parámetros estimados a partir de las observaciones."""

    r: float
    sigma: float


def estimar_parametros(
    tiempos: np.ndarray, poblaciones: np.ndarray
) -> ParametrosModelo:
    """Estima r por ajuste exponencial y sigma desde los residuos."""
    tiempos = np.asarray(tiempos, dtype=float)
    poblaciones = np.asarray(poblaciones, dtype=float)
    if tiempos.ndim != 1 or poblaciones.ndim != 1:
        raise ValueError("Los tiempos y poblaciones deben ser arreglos unidimensionales.")
    if tiempos.size != poblaciones.size or tiempos.size < 2:
        raise ValueError("Se requieren al menos dos pares tiempo-población.")
    if not np.isfinite(tiempos).all() or not np.isfinite(poblaciones).all():
        raise ValueError("Los datos deben contener valores finitos.")
    if poblaciones[0] <= 0 or (poblaciones < 0).any():
        raise ValueError("La población inicial debe ser positiva y ninguna negativa.")
    if (np.diff(tiempos) <= 0).any() or not np.allclose(np.diff(tiempos), 1.0):
        raise ValueError("Los tiempos deben ser consecutivos y estar ordenados.")

    t_relativo = tiempos - tiempos[0]
    p0 = float(poblaciones[0])

    def curva_exponencial(t: np.ndarray, tasa: float) -> np.ndarray:
        return p0 * np.exp(tasa * t)

    ajuste, _ = curve_fit(
        curva_exponencial,
        t_relativo,
        poblaciones,
        p0=(0.1,),
        bounds=(-0.99, 5.0),
        maxfev=10_000,
    )
    r = float(ajuste[0])
    residuos = poblaciones - curva_exponencial(t_relativo, r)
    sigma = float(np.std(residuos, ddof=1))
    return ParametrosModelo(r=r, sigma=sigma)
