# Práctica 01 - Construcción y simulación computacional de un modelo matemático

## Asignatura
Simulación - Unidad 1: Introducción a la Simulación

## Objetivo
Construir un modelo matemático para analizar la posibilidad de lluvia a partir de humedad, nubosidad y temperatura, implementándolo en Python y Java.

## Tecnologías
- Python
- Java
- NumPy
- Matplotlib

## Arquitectura
APE1/
├── README.md
├── requirements.txt
│
├── python/
│   ├── main.py
│   ├── modelo.py
│   ├── datos_climaticos.py
│   ├── graficas.py
│   └── datos.csv
│
└── java/
    └── src/
        ├── AjusteExponencial.java
        ├── GraficasSvg.java
        ├── Main.java
        ├── DatosMeteorologicos.java
        ├── ResultadoSimulacion.java
        └── ModeloLluvia.java

### Responsabilidad de cada archivo Python
- `datos_climaticos.py`: representa los datos de cada medición horaria y carga la información desde el archivo datos.csv
- `modelo.py`: normaliza humedad y nubosidad, calcula Tf, el índice de lluvia, su clasificación y el ajuste exponencial por tramos.
- `graficas.py`: genera las gráficas en formato PNG del índice original y del ajuste exponencial utilizando Matplotlib.
- `main.py`: coordina la ejecución, procesa los datos, imprime las tablas en consola y exporta los resultados.

### Responsabilidad de cada archivo Java
- `DatosMeteorologicos.java`: representa los datos de cada medición horaria (hora, humedad, nubosidad y temperatura).
- `ModeloLluvia.java`: normaliza humedad y nubosidad, calcula `Tf`, el índice de lluvia y su clasificación.
- `ResultadoSimulacion.java`: almacena los valores calculados para cada medición, incluidos `H`, `N`, `Tf`, `I` y el estado.
- `AjusteExponencial.java`: ajusta el índice con curvas exponenciales de crecimiento y decrecimiento alrededor del máximo observado.
- `GraficasSvg.java`: crea la gráfica SVG del índice calculado y del ajuste.
- `Main.java`: coordina la ejecución, carga los datos, ejecuta el modelo e imprime y exporta los resultados.

Python y Java leen las mismas filas de `python/datos.csv`, pero cada programa genera sus propios archivos de salida en su carpeta correspondiente.

## Modelo matemático
`I = 0.5H + 0.3N + 0.2Tf`

Donde:
- `H`: humedad normalizada.
- `N`: nubosidad normalizada.
- `Tf`: factor de temperatura.

La humedad y la nubosidad se normalizan dividiendo sus porcentajes para obtener valores entre 0 y 1.
Para temperaturas intermedias, como 17 °C, se usa interpolación lineal entre los valores de la tabla.

## Ajuste exponencial y alcance de los datos
El programa localiza el máximo del índice observado y ajusta una curva exponencial
continua en cada lado:

- Antes del máximo: `I(t) = P0 * exp(r_crecimiento * (t - t0))`.
- Después del máximo: `I(t) = P0 * exp(r_decrecimiento * (t - t0))`.

Python genera `python/output/resultados.csv`, `python/output/ajuste_exponencial.csv`,`python/output/indice_lluvia.png` y `python/output/ajuste_exponencial.png`.
Java genera sus dos tablas CSV y la gráfica vectorial en `java/output/`.
Ambos programas leen las mismas filas de `python/datos.csv`.

## Cómo ejecutar

### Crear entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Ejecutar Python:

```powershell
python python/main.py
```

### Ejecutar Java:

```powershell
javac -d out java/src/*.java
java -cp out Main
```
