"""Carga y representa los datos meteorológicos"""

import csv
from dataclasses import dataclass
from pathlib import Path

@dataclass
class DatosMeteorologicos:
    hora: str
    humedad: float
    nubosidad: float
    temperatura: float

def cargar_datos():
    """Lee los registros de `datos.csv`."""
    ruta = Path(__file__).parent / "datos.csv"

    with open(ruta, "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        return [
            DatosMeteorologicos(
                fila["hora"],
                float(fila["humedad"]),
                float(fila["nubosidad"]),
                float(fila["temperatura"]),
            )
            for fila in lector
        ]