"""
Tests para el servicio de inventario
"""
from services.inventory.metrics import calculate_inventory_metrics



def test_calculate_inventory_metrics_counts():
    """Verifica conteos de productos críticos/bajos/adecuados"""
    product_db = {
        "Leche": {"stock_minimo": 5},
        "Huevos": {"stock_minimo": 3}
    }
    detected = [
        {"nombre": "Leche", "cantidad": 3},   # 3 < 5 -> bajo
        {"nombre": "Huevos", "cantidad": 0},   # 0 -> crítico
        {"nombre": "Pan", "cantidad": 10}       # no en BD -> ignorado
    ]
    
    result = calculate_inventory_metrics(detected, product_db)
    resumen = result["resumen"]
    
    assert resumen["total_productos"] == 3
    assert resumen["productos_criticos"] == 1
    assert resumen["productos_bajos"] == 1
    assert resumen["productos_adecuados"] == 0

