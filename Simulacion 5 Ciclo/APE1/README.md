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
        ├── Main.java
        ├── DatosMeteorologicos.java
        ├── ResultadoSimulacion.java
        └── ModeloLluvia.java

### Responsabilidad de cada archivo
- `datos_climaticos.py`: representa y carga los datos meteorológicos.
- `modelo.py`: contiene el modelo matemático.
- `graficas.py`: genera la gráfica del índice de lluvia.
- `main.py`: coordina la ejecución.
- En Java, `DatosMeteorologicos`, `ModeloLluvia` y `ResultadoSimulacion` separan los datos, cálculos y resultados. Ambos programas leen las mismas filas de `python/datos.csv`.

## Modelo matemático
`I = 0.5H + 0.3N + 0.2Tf`

Donde:
- `H`: humedad normalizada.
- `N`: nubosidad normalizada.
- `Tf`: factor de temperatura.

La humedad y la nubosidad se normalizan dividiendo sus porcentajes para obtener valores entre 0 y 1.
Para temperaturas intermedias, como 17 °C, se usa interpolación lineal entre los valores de la tabla.

## Prompts utilizados como apoyo
Prompts para documentar únicamente el apoyo utilizado durante el desarrollo:

### Prompt 1
> Analiza el modelo matemático, variables, parámetros, reglas y datos que deben implementarse.

### Prompt 2
> Propón una arquitectura sencilla para implementar esta práctica en Python y Java usando varias clases, evitando concentrar toda la lógica en main.

### Prompt 3
> Revisa el código del modelo matemático y verifica que los cálculos y las gráficas correspondan con los datos y reglas.

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

