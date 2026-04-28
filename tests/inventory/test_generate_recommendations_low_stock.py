"""
Tests para el servicio de inventario
"""
from services.inventory.recommendations import generate_recommendations


def test_generate_recommendations_low_stock():
    """Verifica recomendaciones para stock bajo"""
    low_stock_products = [
        {"producto": "Leche", "stock_actual": 3, "stock_minimo": 5}
    ]
    
    recs = generate_recommendations(low_stock_products)
    
    assert len(recs) == 1
    assert recs[0]["prioridad"] == "MEDIA"
    assert "Reponer" in recs[0]["recomendacion"]

