"""
Fixtures compartidas para tests
"""
import pytest
from app import app


@pytest.fixture
def client():
    """Cliente de test para la aplicación Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_product_database():
    """Base de datos de productos simplificada para tests"""
    return {
        "Leche": {
            "id": "PROD001", "nombre": "Leche", "categoria": "Lácteos",
            "precio": 1.20, "unidad": "litro", "stock_minimo": 5,
            "stock_maximo": 30, "tiempo_reposicion": 2,
            "historial_ventas": [3, 4, 5, 2, 6]
        },
        "Huevos": {
            "id": "PROD002", "nombre": "Huevos", "categoria": "Huevos",
            "precio": 2.50, "unidad": "docena", "stock_minimo": 3,
            "stock_maximo": 20, "tiempo_reposicion": 1,
            "historial_ventas": [2, 3, 2, 4, 3]
        }
    }


@pytest.fixture
def sample_detected_products():
    """Productos detectados simulados para tests"""
    return [
        {"nombre": "Leche", "cantidad": 3, "confianza": 0.92},
        {"nombre": "Huevos", "cantidad": 0, "confianza": 0.88},
        {"nombre": "Pan", "cantidad": 10, "confianza": 0.85}
    ]
