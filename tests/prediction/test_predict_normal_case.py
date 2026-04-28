"""
Tests para el servicio de predicción
"""
from services.prediction.prediction import predict_stock_outage


def test_predict_normal_case():
    """Verifica predicción con caso normal"""
    sales_history = [1, 2, 3, 4, 5]  # Promedio: 3
    current_stock = 30
    
    result = predict_stock_outage(sales_history, current_stock)
    
    # 30 / 3 = 10 días (<=10 se considera MODERADO según el código)
    assert result["dias_hasta_agotarse"] == 10
    assert result["estado"] == "MODERADO"
    assert result["consumo_promedio_diario"] == 3.0

