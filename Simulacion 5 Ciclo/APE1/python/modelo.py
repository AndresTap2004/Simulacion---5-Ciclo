"""Modelo matemático para estimar la posibilidad de lluvia."""

from dataclasses import dataclass
import numpy as np

@dataclass
class ResultadoSimulacion:
    """Resultados del modelo para una fila de datos meteorológicos."""
    datos: object
    h: float
    n: float
    tf: float
    indice: float
    estado: str

class ModeloLluvia:
    """Calcula el factor de temperatura, el índice y su clasificación."""
    PUNTOS_TEMPERATURA = np.array([10, 12, 14, 16, 18, 20, 22, 24, 26, 28])
    FACTORES_TEMPERATURA = np.array([1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1])

    def factor_temperatura(self, temperatura):
        """Interpola linealmente Tf; para valores intermedios es una suposición."""
        return float(np.interp(
            temperatura,
            self.PUNTOS_TEMPERATURA,
            self.FACTORES_TEMPERATURA
        ))

    def clasificar(self, indice):
        """Clasifica el índice I según los intervalos de la guía."""
        if indice < 0.40:
            return "Sin lluvia"
        if indice < 0.60:
            return "Baja posibilidad"
        if indice < 0.75:
            return "Lluvia probable"
        return "Lluvia"

    def evaluar(self, datos):
        """Normaliza las entradas y calcula I = 0.5H + 0.3N + 0.2Tf."""
        h = datos.humedad / 100
        n = datos.nubosidad / 100
        tf = self.factor_temperatura(datos.temperatura)
        indice = 0.5 * h + 0.3 * n + 0.2 * tf
        ## indice = 0.4 * h + 0.2 * n + 0.1 * tf
        return ResultadoSimulacion(
            datos, h, n, tf, indice, self.clasificar(indice)
        )