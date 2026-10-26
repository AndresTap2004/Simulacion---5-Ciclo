"""Pruebas unitarias de los modelos poblacionales."""

import unittest

import numpy as np

import modelos
from modelo_continuo_euler import modelo_continuo_euler
from modelo_deterministico import modelo_deterministico
from modelo_discreto import modelo_discreto
from modelo_estocastico import modelo_estocastico
from parametros import estimar_parametros


class ModelosCrecimientoTests(unittest.TestCase):
    def test_modelos_conserva_importaciones_anteriores(self):
        self.assertIs(modelos.modelo_discreto, modelo_discreto)
        self.assertIs(modelos.estimar_parametros, estimar_parametros)

    def test_modelo_deterministico(self):
        tiempos = np.array([0.0, 1.0, 2.0])
        resultado = modelo_deterministico(100.0, 0.1, tiempos)
        np.testing.assert_allclose(resultado, 100.0 * np.exp(0.1 * tiempos))

    def test_modelo_discreto(self):
        resultado = modelo_discreto(100.0, 0.1, cantidad=3)
        np.testing.assert_allclose(resultado, [100.0, 110.0, 121.0])

    def test_modelo_estocastico_reproducible(self):
        primero = modelo_estocastico(100.0, 0.1, 2.0, 5, semilla=17)
        segundo = modelo_estocastico(100.0, 0.1, 2.0, 5, semilla=17)
        np.testing.assert_array_equal(primero, segundo)

    def test_euler_se_acerca_a_exponencial_con_dt_pequeno(self):
        tiempos = np.array([0.0, 1.0, 2.0])
        exacto = modelo_deterministico(100.0, 0.1, tiempos)
        euler = modelo_continuo_euler(100.0, 0.1, tiempos, dt=0.001)
        np.testing.assert_allclose(euler, exacto, rtol=0.001)

    def test_estimacion_de_parametros(self):
        tiempos = np.arange(5, dtype=float)
        poblaciones = 100.0 * np.exp(0.08 * tiempos)
        parametros = estimar_parametros(tiempos, poblaciones)
        self.assertAlmostEqual(parametros.r, 0.08, places=6)
        self.assertAlmostEqual(parametros.sigma, 0.0, places=6)


if __name__ == "__main__":
    unittest.main()
