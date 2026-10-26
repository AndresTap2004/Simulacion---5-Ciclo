"""Generación de gráficas comparativas y análisis de sensibilidad."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from modelo_continuo_euler import modelo_continuo_euler
from modelo_deterministico import modelo_deterministico
from modelo_discreto import modelo_discreto
from modelo_estocastico import modelo_estocastico


def graficar_comparacion(
    ruta: Path,
    tiempos: np.ndarray,
    observados: np.ndarray,
    r: float,
    sigma: float,
    dt: float,
    semilla: int,
) -> None:
    """Grafica los datos observados y las trayectorias de los cuatro modelos."""
    p0 = float(observados[0])
    deterministico = modelo_deterministico(p0, r, tiempos)
    discreto = modelo_discreto(p0, r, len(tiempos))
    estocastico = modelo_estocastico(
        p0, r, sigma, len(tiempos), semilla=semilla
    )
    euler = modelo_continuo_euler(p0, r, tiempos, dt)

    figura, eje = plt.subplots(figsize=(10, 6))
    eje.plot(tiempos, observados, "ko", label="Datos observados")
    eje.plot(tiempos, deterministico, marker=".", label="Exponencial determinístico")
    eje.step(tiempos, discreto, where="post", marker="s", label="Discreto")
    eje.plot(tiempos, estocastico, marker="x", label="Estocástico")
    eje.plot(tiempos, euler, marker="^", label=f"Continuo (Euler, dt={dt:g})")
    eje.set_title("Comparación de modelos de crecimiento poblacional")
    eje.set_xlabel("Tiempo")
    eje.set_ylabel("Población")
    eje.grid(True, alpha=0.3)
    eje.legend()
    figura.tight_layout()
    figura.savefig(ruta, dpi=160)
    plt.close(figura)


def graficar_sensibilidad_r(
    ruta: Path, tiempos: np.ndarray, p0: float, r: float
) -> None:
    """Compara las curvas determinísticas bajo distintas tasas r."""
    magnitud = max(abs(r), 0.05)
    tasas = (r - 0.5 * magnitud, r, r + 0.5 * magnitud)
    figura, eje = plt.subplots(figsize=(9, 5))
    for tasa in tasas:
        curva = modelo_deterministico(p0, tasa, tiempos)
        eje.plot(tiempos, curva, marker=".", label=f"r = {tasa:.4f}")
    eje.set_title("Sensibilidad del crecimiento a la tasa r")
    eje.set_xlabel("Tiempo")
    eje.set_ylabel("Población")
    eje.grid(True, alpha=0.3)
    eje.legend()
    figura.tight_layout()
    figura.savefig(ruta, dpi=160)
    plt.close(figura)


def graficar_sensibilidad_sigma(
    ruta: Path,
    tiempos: np.ndarray,
    p0: float,
    r: float,
    sigma: float,
    semilla: int,
) -> None:
    """Compara trayectorias aleatorias con distintos niveles de sigma."""
    magnitud = max(sigma, 0.05 * p0)
    niveles = (0.0, sigma, 2.0 * magnitud)
    figura, eje = plt.subplots(figsize=(9, 5))
    for nivel in niveles:
        curva = modelo_estocastico(
            p0, r, nivel, len(tiempos), semilla=semilla
        )
        eje.plot(tiempos, curva, marker="x", label=f"sigma = {nivel:.2f}")
    eje.set_title("Sensibilidad del modelo estocástico al ruido sigma")
    eje.set_xlabel("Tiempo")
    eje.set_ylabel("Población")
    eje.grid(True, alpha=0.3)
    eje.legend()
    figura.tight_layout()
    figura.savefig(ruta, dpi=160)
    plt.close(figura)
