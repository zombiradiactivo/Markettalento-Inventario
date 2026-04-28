"""
Tests para el servicio de inventario
"""
from services.inventory.metrics import calculate_inventory_metrics


def test_calculate_inventory_metrics_structure():
    """Verifica estructura de métricas"""
    product_db = {
        "Leche": {"stock_minimo": 5},
        "Huevos": {"stock_minimo": 3}
    }
    detected = [
        {"nombre": "Leche", "cantidad": 3},
        {"nombre": "Huevos", "cantidad": 0},
        {"nombre": "Pan", "cantidad": 10}
    ]
    
    result = calculate_inventory_metrics(detected, product_db)
    
    assert "resumen" in result
    assert "recomendaciones" in result
    
    resumen = result["resumen"]
    assert "total_productos" in resumen
    assert "total_unidades" in resumen
    assert "productos_criticos" in resumen
    assert "productos_bajos" in resumen
    assert "productos_adecuados" in resumen

