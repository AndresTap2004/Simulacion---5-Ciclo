import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter, FuncFormatter, LinearLocator


class MonteCarloView:
    def __init__(self, directorio_salida=None):
        raiz_proyecto = Path(__file__).resolve().parents[2]
        self.directorio_salida = Path(directorio_salida or raiz_proyecto / "img")
        self.archivo_resultados_java = (
            raiz_proyecto / "java" / "output" / "resultados_java.csv"
        )

    def generar_graficas(self, resultados_python):
        if not resultados_python:
            raise ValueError("Se requieren resultados de Python para generar las gráficas.")

        resultados_java = self._leer_resultados_java()
        self.directorio_salida.mkdir(parents=True, exist_ok=True)
        resultados_python = sorted(resultados_python, key=lambda resultado: resultado["n"])
        if [resultado["n"] for resultado in resultados_python] != [
            resultado["n"] for resultado in resultados_java
        ]:
            raise ValueError("Java y Python deben contener los mismos tamaños de muestra.")

        rutas = [
            self.directorio_salida / "convergencia_python.png",
            self.directorio_salida / "comparativa_java_python.png",
        ]

        self._graficar_convergencia(resultados_python, rutas[0], "Python")
        self._graficar_comparativa(resultados_python, resultados_java, rutas[1])

        return rutas

    def _leer_resultados_java(self):
        if not self.archivo_resultados_java.is_file():
            raise FileNotFoundError(
                f"No se encontraron resultados Java en {self.archivo_resultados_java}. "
                "Ejecuta primero java.Main desde la raíz del proyecto."
            )

        with self.archivo_resultados_java.open(
            newline="", encoding="utf-8"
        ) as archivo:
            lector = csv.DictReader(archivo)
            columnas = {"n", "pi_estimado", "error_absoluto", "tiempo_ms"}
            if not lector.fieldnames or not columnas.issubset(lector.fieldnames):
                raise ValueError(
                    "El CSV de Java debe incluir n, pi_estimado, "
                    "error_absoluto y tiempo_ms."
                )

            resultados = [
                {
                    "n": int(fila["n"]),
                    "pi_estimado": float(fila["pi_estimado"]),
                    "error_absoluto": float(fila["error_absoluto"]),
                    "tiempo_ms": int(fila["tiempo_ms"]),
                }
                for fila in lector
            ]

        if not resultados:
            raise ValueError("El CSV de Java no contiene resultados.")
        return sorted(resultados, key=lambda resultado: resultado["n"])

    @staticmethod
    def _graficar_convergencia(resultados, ruta, lenguaje):
        tamanios = [resultado["n"] for resultado in resultados]
        estimaciones = [resultado["pi_estimado"] for resultado in resultados]
        errores = [resultado["error_absoluto"] for resultado in resultados]

        figura, ejes = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
        figura.suptitle(f"Convergencia de Monte Carlo - {lenguaje}", fontsize=16)

        ejes[0].set_title("Estimación de π")
        ejes[0].plot(
            tamanios,
            estimaciones,
            color="#2869AF",
            marker="o",
            linewidth=1.5,
            markersize=6,
            label="π estimado",
        )
        ejes[0].axhline(
            3.141592653589793,
            color="#BE3737",
            linestyle=(0, (8, 6)),
            linewidth=1.5,
            label="π real",
        )
        minimo_estimacion = min(min(estimaciones), 3.141592653589793)
        maximo_estimacion = max(max(estimaciones), 3.141592653589793)
        margen_estimacion = max((maximo_estimacion - minimo_estimacion) * 0.05, 0.0005)
        ejes[0].set_ylim(
            minimo_estimacion - margen_estimacion,
            maximo_estimacion + margen_estimacion,
        )
        ejes[0].legend(loc="upper right")

        ejes[1].set_title("Error absoluto")
        ejes[1].plot(
            tamanios,
            errores,
            color="#E67D23",
            marker="o",
            linewidth=1.5,
            markersize=6,
        )
        ejes[1].set_ylim(0, max(max(errores) * 1.05, 0.000001))
        ejes[1].set_xlabel("Número de puntos (N)")

        for eje in ejes:
            eje.set_xscale("log")
            eje.set_xticks(tamanios)
            eje.xaxis.set_major_formatter(
                FuncFormatter(lambda valor, posicion: f"{valor:,.0f}")
            )
            eje.yaxis.set_major_locator(LinearLocator(6))
            eje.yaxis.set_major_formatter(FormatStrFormatter("%.6f"))
            eje.minorticks_off()
            eje.grid(True, color="#E1E1E1", linewidth=0.8)

        figura.tight_layout()
        figura.savefig(ruta, dpi=150, bbox_inches="tight")
        plt.close(figura)

    @staticmethod
    def _graficar_comparativa(resultados_python, resultados_java, ruta):
        tamanios = [resultado["n"] for resultado in resultados_java]
        etiquetas = [f"{n:,}" for n in tamanios]
        posiciones = list(range(len(tamanios)))
        ancho_barra = 0.38

        figura, ejes = plt.subplots(2, 1, figsize=(10, 8))
        figura.suptitle("Comparación Java vs. Python")

        for eje, clave, titulo, etiqueta_y in (
            (ejes[0], "tiempo_ms", "Tiempo de ejecución", "Tiempo (ms)"),
            (ejes[1], "error_absoluto", "Error absoluto", "Error absoluto"),
        ):
            python_valores = [resultado[clave] for resultado in resultados_python]
            java_valores = [resultado[clave] for resultado in resultados_java]
            eje.bar(
                [posicion - ancho_barra / 2 for posicion in posiciones],
                python_valores,
                ancho_barra,
                label="Python",
                color="tab:blue",
            )
            eje.bar(
                [posicion + ancho_barra / 2 for posicion in posiciones],
                java_valores,
                ancho_barra,
                label="Java",
                color="tab:orange",
            )
            eje.set_title(titulo)
            eje.set_ylabel(etiqueta_y)
            eje.set_xticks(posiciones)
            eje.set_xticklabels(etiquetas)
            eje.legend()
            eje.grid(axis="y", alpha=0.3)

        ejes[1].set_xlabel("Número de puntos (N)")
        figura.tight_layout()
        figura.savefig(ruta, dpi=150, bbox_inches="tight")
        plt.close(figura)
