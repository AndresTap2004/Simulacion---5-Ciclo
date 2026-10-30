class LinearCongruentialGenerator:
    """Implementación del Generador Congruencial Lineal (LCG)."""

    def __init__(self, seed: int, a: int, c: int, m: int):
        self.seed = seed
        self.a = a
        self.c = c
        self.m = m
        self.current = seed

    def next_value(self) -> float:
        """Genera el siguiente valor normalizado U(n) entre 0 y 1."""
        self.current = (self.a * self.current + self.c) % self.m
        return self.current / self.m

    def generate_sequence(self, n: int) -> list[float]:
        """Genera una secuencia de n valores pseudoaleatorios."""
        return [self.next_value() for _ in range(n)]

    def reset(self, new_seed: int = None):
        """Reinicia la semilla del generador."""
        if new_seed is not None:
            self.seed = new_seed
        self.current = self.seed