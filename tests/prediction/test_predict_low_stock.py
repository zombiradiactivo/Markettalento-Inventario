"""
Tests para el servicio de predicción
"""
from services.prediction.prediction import predict_stock_outage


def test_predict_low_stock():
    """Verifica estado bajo (3-5 días)"""
    sales_history = [2, 2, 2]  # Promedio: 2
    current_stock = 8  # 8/2 = 4 días
    
    result = predict_stock_outage(sales_history, current_stock)
    
    assert result["dias_hasta_agotarse"] == 4
    assert result["estado"] == "BAJO"

