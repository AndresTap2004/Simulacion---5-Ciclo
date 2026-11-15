import sys
import os

# Añade la carpeta actual al path para encontrar los módulos
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from controlador.monte_carlo_controller import MonteCarloController
from vista.monte_carlo_view import MonteCarloView

def main():
    controlador = MonteCarloController()
    resultados = controlador.procesar_simulaciones()

    print("=======================================================================")
    print(" N          | Pi Estimado      | Error Absoluto   | Tiempo Python (ms)")
    print("=======================================================================")

    for res in resultados:
        print(f"{res['n']:<11} | {res['pi_estimado']:<16.6f} | {res['error_absoluto']:<16.6f} | {res['tiempo_ms']:<20.2f}")
        
    print("=======================================================================")

    vista = MonteCarloView()
    rutas_graficas = vista.generar_graficas(resultados)
    print("\nGráficas guardadas:")
    for ruta in rutas_graficas:
        print(f"- {ruta}")

if __name__ == "__main__":
    main()