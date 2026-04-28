"""
Tests para el servicio de predicción
"""
from services.prediction.prediction import predict_stock_outage


def test_predict_critical_stock():
    """Verifica estado crítico (≤2 días)"""
    sales_history = [5, 5, 5]  # Promedio: 5
    current_stock = 10  # 10/5 = 2 días
    
    result = predict_stock_outage(sales_history, current_stock)
    
    assert result["dias_hasta_agotarse"] == 2
    assert result["estado"] == "CRITICO"

