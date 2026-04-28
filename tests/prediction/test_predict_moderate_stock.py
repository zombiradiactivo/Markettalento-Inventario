"""
Tests para el servicio de predicción
"""
from services.prediction.prediction import predict_stock_outage


def test_predict_moderate_stock():
    """Verifica estado moderado (6-10 días)"""
    sales_history = [1, 1, 1]  # Promedio: 1
    current_stock = 8  # 8/1 = 8 días
    
    result = predict_stock_outage(sales_history, current_stock)
    
    assert result["dias_hasta_agotarse"] == 8
    assert result["estado"] == "MODERADO"

