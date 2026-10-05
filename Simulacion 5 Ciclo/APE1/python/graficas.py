"""Genera las gráficas"""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Patch


def generar_graficas(resultados):
    """Guarda el índice calculado y los umbrales de clasificación."""
    salida = Path(__file__).parent / "output"
    salida.mkdir(exist_ok=True)

    horas = [resultado.datos.hora for resultado in resultados]
    indices = [resultado.indice for resultado in resultados]
    bandas = [
        (0.00, 0.40, "#dcefe5", "Sin lluvia (I < 0.40)"),
        (0.40, 0.60, "#fff0c2", "Baja posibilidad (0.40 <= I < 0.60)"),
        (0.60, 0.75, "#ffdfbf", "Lluvia probable (0.60 <= I < 0.75)"),
        (0.75, 1.00, "#f5dada", "Lluvia (I >= 0.75)"),
    ]

    figura, eje = plt.subplots(figsize=(10, 6))
    for inferior, superior, color, _ in bandas:
        eje.axhspan(inferior, superior, color=color, alpha=0.65, zorder=0)

    eje.plot(horas, indices, color="#183b56", marker="o", linewidth=2, zorder=2)
    for hora, indice in zip(horas, indices):
        eje.annotate(
            f"{indice:.3f}",
            (hora, indice),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            fontsize=8,
        )

    for umbral in (0.40, 0.60, 0.75):
        eje.axhline(umbral, color="#59636e", linestyle="--", linewidth=1, zorder=1)
        eje.annotate(
            f"{umbral:.2f}",
            xy=(1, umbral),
            xycoords=("axes fraction", "data"),
            xytext=(5, 0),
            textcoords="offset points",
            va="center",
            fontsize=8,
            color="#39424c",
        )

    leyenda = [Patch(facecolor=color, label=etiqueta) for _, _, color, etiqueta in bandas]
    eje.set_title("Índice del modelo de lluvia por hora")
    eje.set_xlabel("Hora")
    eje.set_ylabel("Índice I (0 a 1)")
    eje.set_ylim(0, 1)
    eje.grid(axis="x", color="white", linewidth=1)
    eje.legend(handles=leyenda, loc="lower left", fontsize=8, framealpha=0.95)
    figura.tight_layout(rect=(0, 0, 0.94, 1))
    figura.savefig(salida / "indice_lluvia.png", dpi=150)
    plt.close(figura)