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


@dataclass
class ResultadoAjuste:
    """Índice observado y valor estimado por el modelo exponencial."""
    hora: str
    humedad: float
    nubosidad: float
    temperatura: float
    h: float
    n: float
    tf: float
    indice_original: float
    indice_ajustado: float
    estado: str
    tendencia: str
    tasa: float


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
        return ResultadoSimulacion(
            datos, h, n, tf, indice, self.clasificar(indice)
        )

    @staticmethod
    def _hora_a_horas(hora):
        """Convierte HH:MM a horas decimales desde medianoche."""
        horas, minutos = hora.split(":")
        return int(horas) + int(minutos) / 60

    def ajustar_exponencial(self, resultados):
        """Ajusta curvas exponenciales continuas a ambos lados del máximo.

        El máximo observado actúa como P0 en ambas ramas. Las tasas se
        estiman por mínimos cuadrados en escala logarítmica y cada rama pasa
        por ese máximo, evitando un salto entre crecimiento y decrecimiento.
        """
        if len(resultados) < 2:
            raise ValueError("Se necesitan al menos dos mediciones para ajustar el modelo.")

        horas = np.array(
            [self._hora_a_horas(item.datos.hora) for item in resultados],
            dtype=float,
        )
        indices = np.array([item.indice for item in resultados], dtype=float)
        if np.any(indices <= 0):
            raise ValueError("El ajuste exponencial requiere índices mayores que cero.")
        if np.any(np.diff(horas) <= 0):
            raise ValueError("Las horas deben estar ordenadas y no repetirse.")

        maximo = int(np.argmax(indices))
        p0 = indices[maximo]
        horas_relativas = horas - horas[maximo]

        def estimar_tasa(desplazamientos, valores):
            denominador = float(np.dot(desplazamientos, desplazamientos))
            if denominador == 0:
                return 0.0
            return float(
                np.dot(desplazamientos, np.log(valores / p0)) / denominador
            )

        tasa_crecimiento = estimar_tasa(
            horas_relativas[: maximo + 1],
            indices[: maximo + 1],
        )
        tasa_decrecimiento = estimar_tasa(
            horas_relativas[maximo:],
            indices[maximo:],
        )

        ajustados = p0 * np.exp(
            np.where(
                horas_relativas <= 0,
                tasa_crecimiento * horas_relativas,
                tasa_decrecimiento * horas_relativas,
            )
        )

        ajustes = []
        for posicion, (resultado, indice_ajustado) in enumerate(
            zip(resultados, ajustados)
        ):
            if posicion < maximo:
                tendencia, tasa = "Crecimiento", tasa_crecimiento
            elif posicion > maximo:
                tendencia, tasa = "Decrecimiento", tasa_decrecimiento
            else:
                tendencia, tasa = "Maximo", 0.0
            datos = resultado.datos
            ajustes.append(
                ResultadoAjuste(
                    hora=datos.hora,
                    humedad=datos.humedad,
                    nubosidad=datos.nubosidad,
                    temperatura=datos.temperatura,
                    h=resultado.h,
                    n=resultado.n,
                    tf=resultado.tf,
                    indice_original=resultado.indice,
                    indice_ajustado=float(indice_ajustado),
                    estado=self.clasificar(float(indice_ajustado)),
                    tendencia=tendencia,
                    tasa=tasa,
                )
            )

        return ajustes, p0, tasa_crecimiento, tasa_decrecimiento