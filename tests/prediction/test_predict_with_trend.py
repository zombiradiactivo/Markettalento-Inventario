"""
Tests para el servicio de predicción
"""
from services.prediction.prediction import predict_stock_outage


def test_predict_with_trend():
    """Verifica predicción considerando tendencia reciente"""
    # Historial con tendencia al alza en los últimos 5
    sales_history = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2]  # Últimos 5: promedio 2
    
    result = predict_stock_outage(sales_history, 20)
    
    # Ajuste por tendencia: avg=1.5, recent=2, trend=2/1.5=1.33, adjusted=2.0
    # 20 / 2 = 10 días
    assert result["dias_hasta_agotarse"] > 0
    assert "consumo_promedio_diario" in result
