from datos_climaticos import cargar_datos
from modelo import ModeloLluvia
from graficas import generar_graficas
import csv
from pathlib import Path

def mostrar_resultados(resultados):
    print("\nRESULTADOS")
    print("-" * 90)
    print(
        f"{'Hora':<8}{'Hum.':>7}{'Nub.':>7}{'Temp.':>8}"
        f"{'H':>7}{'N':>7}{'Tf':>7}{'I':>9}  Estado"
    )
    print("-" * 90)

    for resultado in resultados:
        w = resultado.datos
        print(
            f"{w.hora:<8}{w.humedad:>7.0f}{w.nubosidad:>7.0f}"
            f"{w.temperatura:>8.1f}{resultado.h:>7.2f}{resultado.n:>7.2f}"
            f"{resultado.tf:>7.2f}{resultado.indice:>9.3f}  {resultado.estado}"
        )

def main():
    datos = cargar_datos()
    modelo = ModeloLluvia()

    resultados = [modelo.evaluar(item) for item in datos]

    mostrar_resultados(resultados)
    generar_graficas(resultados)

    output = Path(__file__).parent / "output"
    output.mkdir(exist_ok=True)

    # Escribir CSV de resultados con H, N, Tf, Índice y Estado
    csv_path = output / "resultados.csv"
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["hora", "humedad", "nubosidad", "temperatura", "H", "N", "Tf", "indice", "estado"])
        for resultado in resultados:
            w = resultado.datos
            writer.writerow([
                w.hora,
                int(w.humedad),
                int(w.nubosidad),
                float(w.temperatura),
                f"{resultado.h:.2f}",
                f"{resultado.n:.2f}",
                f"{resultado.tf:.2f}",
                f"{resultado.indice:.3f}",
                resultado.estado,
            ])

    print("\nGráficas generadas en python/output/ y resultados exportados en python/output/resultados.csv")

if __name__ == "__main__":
    main()
