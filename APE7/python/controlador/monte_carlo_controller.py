# Asegura la ruta relativa para importar el modelo correctamente
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modelo.monte_carlo_model import MonteCarloModel

class MonteCarloController:
    def __init__(self):
        self.tamanios_muestra = [1000, 10000, 100000, 1000000]

    def procesar_simulaciones(self):
        resultados = []
        for n in self.tamanios_muestra:
            modelo = MonteCarloModel(n)
            modelo.ejecutar_simulacion()
            
            resultados.append({
                "n": modelo.get_n,
                "pi_estimado": modelo.get_pi_estimado,
                "error_absoluto": modelo.get_error_absoluto,
                "tiempo_ms": modelo.get_tiempo_ms
            })
        return resultados