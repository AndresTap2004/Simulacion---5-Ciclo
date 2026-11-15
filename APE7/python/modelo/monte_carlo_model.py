import time
import numpy as np

class MonteCarloModel:
    def __init__(self, n):
        self.n = n
        self.pi_estimado = 0.0
        self.error_absoluto = 0.0
        self.tiempo_ejecucion_ms = 0.0

    def ejecutar_simulacion(self):
        inicio = time.time()
        
        # Generar puntos aleatorios con NumPy
        x = np.random.rand(self.n)
        y = np.random.rand(self.n)
        
        dentro_circulo = (x**2 + y**2) <= 1.0
        nc = np.sum(dentro_circulo)
        
        fin = time.time()
        
        self.pi_estimado = 4.0 * nc / self.n
        self.error_absoluto = abs(np.pi - self.pi_estimado)
        self.tiempo_ejecucion_ms = (fin - inicio) * 1000.0

    @property
    def get_n(self):
        return self.n

    @property
    def get_pi_estimado(self):
        return self.pi_estimado

    @property
    def get_error_absoluto(self):
        return self.error_absoluto

    @property
    def get_tiempo_ms(self):
        return self.tiempo_ejecucion_ms