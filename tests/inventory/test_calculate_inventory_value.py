"""
Tests para el servicio de inventario
"""
from services.inventory.value import calculate_inventory_value


def test_calculate_inventory_value():
    """Verifica cálculo de valor de inventario"""
    product_db = {
        "Leche": {"precio": 1.20},
        "Huevos": {"precio": 2.50}
    }
    
    detected = [
        {"nombre": "Leche", "cantidad": 10},  # 12.0
        {"nombre": "Huevos", "cantidad": 5},   # 12.5
        {"nombre": "Pan", "cantidad": 3}        # No está en BD, ignorado
    ]
    
    value = calculate_inventory_value(detected, product_db)
    expected = (10 * 1.20) + (5 * 2.50)  # 12.0 + 12.5 = 24.5
    
    assert value == expected

