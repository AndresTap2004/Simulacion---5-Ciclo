"""Modelo estocástico de crecimiento poblacional."""

import numpy as np

from validaciones_modelos import validar_cantidad


def modelo_estocastico(
    p0: float,
    r: float,
    sigma: float,
    cantidad: int,
    semilla: int | None = 42,
) -> np.ndarray:
    """Simula el crecimiento discreto añadiendo ruido normal en cada paso."""
    validar_cantidad(cantidad)
    if sigma < 0 or not np.isfinite(sigma):
        raise ValueError("sigma debe ser un número finito no negativo.")

    generador = np.random.default_rng(semilla)
    ruido = generador.normal(loc=0.0, scale=sigma, size=cantidad - 1)
    poblacion = np.empty(cantidad, dtype=float)
    poblacion[0] = p0
    for paso in range(cantidad - 1):
        poblacion[paso + 1] = (
            poblacion[paso] + r * poblacion[paso] + ruido[paso]
        )
    return poblacion
