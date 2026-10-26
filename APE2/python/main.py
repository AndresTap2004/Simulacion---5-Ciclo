"""Punto de entrada de la simulación poblacional APE2."""

import argparse
import math
from pathlib import Path

import pandas as pd

from datos import cargar_datos
from graficas import (
    graficar_comparacion,
    graficar_sensibilidad_r,
    graficar_sensibilidad_sigma,
)
from modelo_continuo_euler import modelo_continuo_euler
from modelo_deterministico import modelo_deterministico
from modelo_discreto import modelo_discreto
from modelo_estocastico import modelo_estocastico
from parametros import estimar_parametros


DIRECTORIO_PYTHON = Path(__file__).resolve().parent


def crear_argumentos() -> argparse.ArgumentParser:
    """Configura los argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description="Compara cuatro modelos de crecimiento poblacional."
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=DIRECTORIO_PYTHON / "datos.csv",
        help="CSV con columnas tiempo,poblacion.",
    )
    parser.add_argument(
        "--r",
        type=float,
        default=None,
        help="Tasa de crecimiento; se estima desde los datos si se omite.",
    )
    parser.add_argument(
        "--sigma",
        type=float,
        default=None,
        help="Desviación del ruido; se estima desde los datos si se omite.",
    )
    parser.add_argument(
        "--dt", type=float, default=0.1, help="Paso máximo de Euler (0.1)."
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Semilla reproducible del modelo aleatorio."
    )
    return parser


def ejecutar(
    ruta_datos: Path,
    ruta_salida: Path,
    tasa: float | None = None,
    sigma: float | None = None,
    dt: float = 0.1,
    semilla: int = 42,
) -> pd.DataFrame:
    """Ejecuta los modelos y exporta resultados y gráficas."""
    datos = cargar_datos(ruta_datos)
    tiempos = datos["tiempo"].to_numpy(dtype=float)
    observados = datos["poblacion"].to_numpy(dtype=float)
    parametros = estimar_parametros(tiempos, observados)

    r = parametros.r if tasa is None else tasa
    sigma_usado = parametros.sigma if sigma is None else sigma
    if not math.isfinite(r) or r <= -1:
        raise ValueError("r debe ser finito y mayor que -1.")
    if not math.isfinite(sigma_usado) or sigma_usado < 0:
        raise ValueError("sigma debe ser finito y no negativo.")
    if not math.isfinite(dt) or dt <= 0:
        raise ValueError("dt debe ser finito y mayor que cero.")

    cantidad = len(datos)
    resultados = datos.copy()
    resultados["deterministico"] = modelo_deterministico(
        observados[0], r, tiempos
    )
    resultados["discreto"] = modelo_discreto(observados[0], r, cantidad)
    resultados["estocastico"] = modelo_estocastico(
        observados[0], r, sigma_usado, cantidad, semilla=semilla
    )
    resultados["continuo_euler"] = modelo_continuo_euler(
        observados[0], r, tiempos, dt
    )

    ruta_salida.mkdir(parents=True, exist_ok=True)
    resultados.to_csv(ruta_salida / "resultados.csv", index=False)
    graficar_comparacion(
        ruta_salida / "comparacion_modelos.png",
        tiempos,
        observados,
        r,
        sigma_usado,
        dt,
        semilla,
    )
    graficar_sensibilidad_r(
        ruta_salida / "sensibilidad_r.png", tiempos, observados[0], r
    )
    graficar_sensibilidad_sigma(
        ruta_salida / "sensibilidad_sigma.png",
        tiempos,
        observados[0],
        r,
        sigma_usado,
        semilla,
    )

    print(
        f"Parámetros estimados: r={parametros.r:.6f}, "
        f"sigma={parametros.sigma:.3f}"
    )
    if tasa is not None:
        print(f"r usado: {r:.6f}")
    if sigma is not None:
        print(f"sigma usado: {sigma_usado:.3f}")
    print(f"dt={dt:g}; semilla={semilla}")
    formatos = {
        columna: "{:.3f}".format
        for columna in (
            "poblacion",
            "deterministico",
            "discreto",
            "estocastico",
            "continuo_euler",
        )
    }
    print("\nResultados por período:")
    print(resultados.to_string(index=False, formatters=formatos))
    print(f"\nArchivos guardados en: {ruta_salida}")
    return resultados


def main() -> None:
    argumentos = crear_argumentos().parse_args()
    ejecutar(
        ruta_datos=argumentos.data,
        ruta_salida=DIRECTORIO_PYTHON / "output",
        tasa=argumentos.r,
        sigma=argumentos.sigma,
        dt=argumentos.dt,
        semilla=argumentos.seed,
    )


if __name__ == "__main__":
    main()
