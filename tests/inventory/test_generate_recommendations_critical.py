"""
Tests para el servicio de inventario
"""
from services.inventory.metrics import calculate_inventory_metrics
from services.inventory.recommendations import generate_recommendations
from services.inventory.value import calculate_inventory_value


def test_generate_recommendations_critical():
    """Verifica recomendaciones para productos críticos"""
    critical_products = [
        {"producto": "Huevos", "stock_actual": 0, "stock_minimo": 3}
    ]
    
    recs = generate_recommendations(critical_products)
    
    assert len(recs) == 1
    assert recs[0]["prioridad"] == "ALTA"
    assert "urgentemente" in recs[0]["recomendacion"]

