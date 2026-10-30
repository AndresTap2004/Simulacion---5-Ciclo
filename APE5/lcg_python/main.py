from analysis import LcgAnalyzer
from lcg_generator import LinearCongruentialGenerator


def main():
    # Parámetros establecidos en la guía
    a = 1664525
    c = 1013904223
    m = 2**32
    seed = 12345

    print("--- INICIALIZANDO GENERADOR LCG ---")
    lcg_py = LinearCongruentialGenerator(seed=seed, a=a, c=c, m=m)

    # 1. Generar 10,000 valores
    valores_python = lcg_py.generate_sequence(10000)
    print(f"Se han generado {len(valores_python)} valores exitosamente en Python.")

    # Simulando que los resultados de Java son idénticos por usar el mismo algoritmo
    # (En la práctica real, aquí cargarías los datos generados por Java o los calcularías con la clase equivalente en Java)
    lcg_java_sim = LinearCongruentialGenerator(seed=seed, a=a, c=c, m=m)
    valores_java = lcg_java_sim.generate_sequence(10000)

    # 2. Comparar las primeras 20 observaciones
    print("\n--- COMPARACIÓN DE LAS PRIMERAS 20 OBSERVACIONES ---")
    LcgAnalyzer.print_comparison(valores_python, valores_java, limit=20)

    # 3. Graficar
    # LcgAnalyzer.plot_sequence(valores_python, "LCG - Python")


if __name__ == "__main__":
    main()