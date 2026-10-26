"""Modelo exponencial determinístico de crecimiento poblacional."""

import numpy as np


def modelo_deterministico(
    p0: float, r: float, tiempos: np.ndarray
) -> np.ndarray:
    """Calcula P(t) = P0 * exp(r*t), relativo al primer tiempo."""
    tiempos = np.asarray(tiempos, dtype=float)
    return p0 * np.exp(r * (tiempos - tiempos[0]))
