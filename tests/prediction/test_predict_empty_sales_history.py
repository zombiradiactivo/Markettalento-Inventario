"""
Tests para el servicio de predicción
"""
from services.prediction.prediction import predict_stock_outage


def test_predict_empty_sales_history():
    """Verifica predicción con historial vacío"""
    result = predict_stock_outage([], 10)
    
    assert result["dias_hasta_agotarse"] == 0
    assert result["estado"] == "SIN HISTORIAL"

