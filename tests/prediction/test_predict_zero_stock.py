"""
Tests para el servicio de predicción
"""
from services.prediction.prediction import predict_stock_outage


def test_predict_zero_stock():
    """Verifica predicción con stock cero"""
    result = predict_stock_outage([1, 2, 3], 0)
    
    assert result["dias_hasta_agotarse"] == 0
    assert result["estado"] == "AGOTADO"

