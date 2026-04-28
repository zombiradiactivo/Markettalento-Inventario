"""
Servicio de Visión Artificial (simulado)
"""
import random
from datetime import datetime


def detect_products(image_path=None):
    """
    Simula la detección de productos mediante visión artificial.
    
    Args:
        image_path: Ruta de la imagen (no utilizado en simulación)
    
    Returns:
        dict: Escenario con productos detectados y niveles de confianza
    """
    print("Analizando imagen para deteccion de productos...")
    
    escenarios = [
        {
            "descripcion": "Estanteria de supermercado - Stock moderado",
            "productos": [
                {"nombre": "Leche", "cantidad": 8, "confianza": 0.92},
                {"nombre": "Huevos", "cantidad": 5, "confianza": 0.88},
                {"nombre": "Pan", "cantidad": 3, "confianza": 0.85},
                {"nombre": "Agua", "cantidad": 12, "confianza": 0.95},
                {"nombre": "Cafe", "cantidad": 6, "confianza": 0.90}
            ]
        },
        {
            "descripcion": "Almacen de tienda - Stock alto",
            "productos": [
                {"nombre": "Arroz", "cantidad": 25, "confianza": 0.94},
                {"nombre": "Leche", "cantidad": 18, "confianza": 0.91},
                {"nombre": "Huevos", "cantidad": 22, "confianza": 0.89},
                {"nombre": "Agua", "cantidad": 30, "confianza": 0.96},
                {"nombre": "Cafe", "cantidad": 15, "confianza": 0.87}
            ]
        },
        {
            "descripcion": "Nevera comercial - Stock bajo",
            "productos": [
                {"nombre": "Yogur", "cantidad": 4, "confianza": 0.83},
                {"nombre": "Queso", "cantidad": 2, "confianza": 0.80},
                {"nombre": "Mantequilla", "cantidad": 3, "confianza": 0.82},
                {"nombre": "Zumo", "cantidad": 5, "confianza": 0.86},
                {"nombre": "Fiambre", "cantidad": 1, "confianza": 0.78}
            ]
        }
    ]
    
    escenario = random.choice(escenarios)
    print(f"Deteccion simulada: {escenario['descripcion']}")
    
    return escenario
