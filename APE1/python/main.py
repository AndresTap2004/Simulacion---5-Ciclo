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


def mostrar_ajuste(ajustes, p0, tasa_crecimiento, tasa_decrecimiento):
    print("\nTABLA DEL MODELO EXPONENCIAL AJUSTADO")
    print("-" * 116)
    print(
        f"{'Hora':<8}{'Humr':>7}{'Nub.':>7}{'Temp.':>8}{'H':>7}{'N':>7}"
        f"{'Tf':>7}{'I original':>12}{'I ajustado':>13}{'Tendencia':>16}  Estado"
    )
    print("-" * 116)
    for ajuste in ajustes:
        print(
            f"{ajuste.hora:<8}{ajuste.humedad:>7.0f}{ajuste.nubosidad:>7.0f}"
            f"{ajuste.temperatura:>8.1f}{ajuste.h:>7.2f}{ajuste.n:>7.2f}"
            f"{ajuste.tf:>7.2f}{ajuste.indice_original:>12.3f}"
            f"{ajuste.indice_ajustado:>13.3f}{ajuste.tendencia:>16}  "
            f"{ajuste.estado}"
        )
    print(
        f"\nP0 = {p0:.3f}; r crecimiento = {tasa_crecimiento:.6f} h^-1; "
        f"r decrecimiento = {tasa_decrecimiento:.6f} h^-1"
    )


def main():
    datos = cargar_datos()
    modelo = ModeloLluvia()

    resultados = [modelo.evaluar(item) for item in datos]
    ajustes, p0, tasa_crecimiento, tasa_decrecimiento = (
        modelo.ajustar_exponencial(resultados)
    )

    mostrar_resultados(resultados)
    mostrar_ajuste(ajustes, p0, tasa_crecimiento, tasa_decrecimiento)
    generar_graficas(resultados, ajustes)

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

    ajuste_path = output / "ajuste_exponencial.csv"
    with open(ajuste_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "hora",
            "humedad",
            "nubosidad",
            "temperatura",
            "H",
            "N",
            "Tf",
            "indice_original",
            "indice_ajustado",
            "tendencia",
            "r_por_hora",
            "estado",
        ])
        for ajuste in ajustes:
            writer.writerow([
                ajuste.hora,
                f"{ajuste.humedad:.0f}",
                f"{ajuste.nubosidad:.0f}",
                f"{ajuste.temperatura:.1f}",
                f"{ajuste.h:.2f}",
                f"{ajuste.n:.2f}",
                f"{ajuste.tf:.2f}",
                f"{ajuste.indice_original:.3f}",
                f"{ajuste.indice_ajustado:.3f}",
                ajuste.tendencia,
                f"{ajuste.tasa:.6f}",
                ajuste.estado,
            ])

    print(
        "\nArchivos generados en python/output/: resultados.csv, "
        "ajuste_exponencial.csv, indice_lluvia.png y ajuste_exponencial.png"
    )

if __name__ == "__main__":
    main()
