"""
Tests para el servicio de inventario
"""
from services.inventory.value import calculate_inventory_value


def test_calculate_inventory_value_empty():
    """Verifica valor con lista vacía"""
    value = calculate_inventory_value([], {})
    assert value == 0
