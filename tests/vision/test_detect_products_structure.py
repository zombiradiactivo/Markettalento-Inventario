"""
Tests para el servicio de visión artificial (simulado)
"""
from unittest.mock import patch
from services.vision.vision import detect_products


def test_detect_products_structure():
    """Verifica que la estructura de respuesta sea correcta"""
    with patch('services.vision.vision.random.choice') as mock_choice:
        # Simular un escenario específico
        mock_choice.return_value = {
            "descripcion": "Estantería de prueba - Stock moderado",
            "productos": [
                {"nombre": "Leche", "cantidad": 8, "confianza": 0.92},
                {"nombre": "Huevos", "cantidad": 5, "confianza": 0.88}
            ]
        }
        
        result = detect_products()
        
        # Verificar estructura
        assert "descripcion" in result
        assert "productos" in result
        assert isinstance(result["productos"], list)
        assert len(result["productos"]) == 2
        
        # Verificar estructura de cada producto
        for producto in result["productos"]:
            assert "nombre" in producto
            assert "cantidad" in producto
            assert "confianza" in producto

