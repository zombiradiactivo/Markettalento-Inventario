"""
Tests para el servicio de visión artificial (simulado)
"""
from unittest.mock import patch
from services.vision.vision import detect_products

def test_detect_products_confidence_range():
    """Verifica que los niveles de confianza estén en rango válido"""
    with patch('services.vision.vision.random.choice') as mock_choice:
        mock_choice.return_value = {
            "descripcion": "Test",
            "productos": [
                {"nombre": "Leche", "cantidad": 10, "confianza": 0.95}
            ]
        }
        
        result = detect_products()
        confianza = result["productos"][0]["confianza"]
        
        assert 0.0 <= confianza <= 1.0

