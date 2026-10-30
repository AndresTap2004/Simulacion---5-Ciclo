import matplotlib.pyplot as plt


class LcgAnalyzer:

    @staticmethod
    def print_comparison(seq1: list[float], seq2: list[float], limit: int = 20):
        """Compara e imprime las primeras N observaciones de dos secuencias."""
        print(f"{'Índice':<8} | {'Python (U_n)':<15} | {'Java (U_n)':<15}")
        print("-" * 44)
        for i in range(min(limit, len(seq1), len(seq2))):
            print(f"{i+1:<8} | {seq1[i]:<15.6f} | {seq2[i]:<15.6f}")

    @staticmethod
    def plot_sequence(sequence: list[float], title: str = "Secuencia LCG"):
        """Grafica la secuencia generada."""
        plt.figure(figsize=(10, 4))
        plt.plot(sequence[:500], marker="o", markersize=2, linestyle="none", alpha=0.6)
        plt.title(f"{title} (Primeros 500 puntos)")
        plt.xlabel("Índice (n)")
        plt.ylabel("Valor U(n)")
        plt.grid(True)
        plt.show()