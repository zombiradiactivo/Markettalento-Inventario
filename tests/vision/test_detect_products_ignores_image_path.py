"""
Tests para el servicio de visión artificial (simulado)
"""
from unittest.mock import patch
from services.vision.vision import detect_products

def test_detect_products_ignores_image_path():
    """Verifica que el parámetro image_path sea ignorado (simulación)"""
    result1 = detect_products()
    result2 = detect_products(image_path="/ruta/inexistente.jpg")
    
    # Ambos deben tener la misma estructura
    assert type(result1) == type(result2)
    assert "descripcion" in result1
