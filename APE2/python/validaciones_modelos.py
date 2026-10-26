"""Validaciones compartidas por los modelos de simulación."""


def validar_cantidad(cantidad: int) -> None:
    """Comprueba que haya al menos un período para simular."""
    if cantidad < 1:
        raise ValueError("La cantidad de períodos debe ser al menos uno.")
