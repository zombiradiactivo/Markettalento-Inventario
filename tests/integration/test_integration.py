"""
Tests de integración para la API
"""
import json
import pytest
from unittest.mock import patch
from app import app


@pytest.fixture
def client():
    """Cliente de test para la aplicación Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_endpoint(client):
    """Verifica que la página principal cargue"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Inventario Inteligente' in response.data


def test_endpoint_dashboard(client):
    """Verifica que el dashboard de endpoints cargue"""
    response = client.get('/endpoint')
    assert response.status_code == 200
    assert b'Endpoints de la API' in response.data


def test_api_test(client):
    """Verifica endpoint de prueba"""
    response = client.get('/api/test')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'servicios' in data
    assert 'vision' in data['servicios']


def test_api_productos(client):
    """Verifica obtención de catálogo de productos"""
    response = client.get('/api/productos')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'productos' in data
    assert len(data['productos']) == 25  # 25 productos en 5 tablas


def test_api_producto_existente(client):
    """Verifica obtención de producto específico"""
    response = client.get('/api/producto/Leche Entera')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['producto']['nombre'] == 'Leche Entera'
    assert data['producto']['id'] == '1'


def test_api_producto_no_existente(client):
    """Verifica respuesta para producto inexistente"""
    response = client.get('/api/producto/ProductoInexistente')
    assert response.status_code == 404
    
    data = json.loads(response.data)
    assert data['status'] == 'error'


def test_api_recomendaciones(client):
    """Verifica endpoint de recomendaciones"""
    response = client.get('/api/recomendaciones')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert 'recomendaciones' in data
    assert len(data['recomendaciones']) <= 5


def test_api_analizar_inventario(client):
    """Verifica análisis de inventario con visión simulada"""
    with patch('api.routes.detect_products') as mock_detect:
        # Simular detección de productos
        mock_detect.return_value = {
            "descripcion": "Test scenario",
            "productos": [
                {"nombre": "Leche", "cantidad": 8, "confianza": 0.92}
            ]
        }
        
        response = client.get('/api/analizar-inventario')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'productos' in data
        assert 'analisis' in data
        assert 'valor_inventario' in data
