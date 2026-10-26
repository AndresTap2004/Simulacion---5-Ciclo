"""Modelo discreto de crecimiento poblacional."""

import numpy as np

from validaciones_modelos import validar_cantidad


def modelo_discreto(p0: float, r: float, cantidad: int) -> np.ndarray:
    """Calcula P(t+1) = P(t) + r*P(t) en períodos discretos."""
    validar_cantidad(cantidad)
    poblacion = np.empty(cantidad, dtype=float)
    poblacion[0] = p0
    for paso in range(cantidad - 1):
        poblacion[paso + 1] = poblacion[paso] + r * poblacion[paso]
    return poblacion
