# APE2: Modelos de crecimiento poblacional

## Objetivo
Implementar y comparar cuatro paradigmas de simulación de crecimiento poblacional: exponencial determinístico, discreto, estocástico y continuo
mediante el método de Euler. También se analiza la influencia de la tasa de crecimiento `r`, del ruido `sigma` y del tamaño de paso `dt`.

## Estructura del proyecto

```text
APE2/
├── .gitignore
├── README.md
├── requirements.txt
└── python/
    ├── datos.csv
    ├── datos.py
    ├── parametros.py
    ├── modelo_deterministico.py
    ├── modelo_discreto.py
    ├── modelo_estocastico.py
    ├── modelo_continuo_euler.py
    ├── validaciones_modelos.py
    ├── graficas.py
    ├── main.py
    ├── test_modelos.py
    └── output/               
```

### Responsabilidad de cada archivo
- `datos.csv`: observaciones de tiempo y población.
- `datos.py`: carga y valida el conjunto de entrada.
- `parametros.py`: define `ParametrosModelo` y estima `r` y `sigma`.
- `modelo_deterministico.py`: implementa el modelo exponencial determinístico.
- `modelo_discreto.py`: implementa el modelo de crecimiento por períodos.
- `modelo_estocastico.py`: implementa el modelo discreto con ruido normal.
- `modelo_continuo_euler.py`: implementa la aproximación de Euler del modelo continuo.
- `validaciones_modelos.py`: comparte las validaciones requeridas por los modelos discretos y estocásticos.
- `graficas.py`: produce las gráficas comparativa y de sensibilidad.
- `main.py`: coordina la ejecución y exporta resultados.
- `test_modelos.py`: prueba las implementaciones importadas desde sus módulos.
- `requirements.txt`: declara las dependencias de Python.

## Datos de entrada

El archivo `python/datos.csv` contiene siete observaciones:

```csv
tiempo,poblacion
0,1000
1,1100
2,1250
3,1400
4,1600
5,1850
6,2100
```

## Modelos matemáticos
1. **Exponencial determinístico:** `P(t) = P0 * exp(r*t)`.
2. **Discreto:** `P(t+1) = P(t) + r*P(t)`.
3. **Estocástico:** `P(t+1) = P(t) + r*P(t) + epsilon_t`, donde `epsilon_t ~ Normal(0, sigma^2)`.
4. **Continuo con Euler:** `P(t+dt) = P(t) + dt*r*P(t)`.

## Instalación, ejecución y pruebas

### Crear entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```
### Ejecutar Python:

```powershell
python python/main.py
python -m unittest discover -s python -p "test_*.py" -- Ejecutar pruebas
```

Opciones de ejecución:

```powershell
python python/main.py --r 0.12 --sigma 50 --dt 0.1 --seed 7
python python/main.py --data python/otro_conjunto.csv
```

Si no se proporcionan `--r` ni `--sigma`, se estiman desde el CSV.

## Archivos generados
La ejecución crea `python/output/` y guarda:

- `resultados.csv`: observaciones y resultados de los cuatro modelos.
- `comparacion_modelos.png`: datos y trayectorias simuladas.
- `sensibilidad_r.png`: curvas exponenciales con distintas tasas.
- `sensibilidad_sigma.png`: trayectorias estocásticas con distintos niveles de ruido.
