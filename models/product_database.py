"""
Módulo de modelos de productos - Base de datos simulada
"""

# Base de datos simulada de productos
product_database = {
    "Leche": {
        "id": "PROD001", "nombre": "Leche", "categoria": "Lácteos",
        "precio": 1.20, "unidad": "litro", "stock_minimo": 5,
        "stock_maximo": 30, "tiempo_reposicion": 2,
        "historial_ventas": [3, 4, 5, 2, 6, 4, 5, 3, 4, 6, 5, 4, 3, 5, 4, 6, 3, 5, 4, 5]
    },
    "Huevos": {
        "id": "PROD002", "nombre": "Huevos", "categoria": "Huevos",
        "precio": 2.50, "unidad": "docena", "stock_minimo": 3,
        "stock_maximo": 20, "tiempo_reposicion": 1,
        "historial_ventas": [2, 3, 2, 4, 3, 2, 3, 4, 2, 3, 4, 2, 3, 2, 4, 3, 2, 3, 2, 4]
    },
    "Pan": {
        "id": "PROD003", "nombre": "Pan", "categoria": "Panadería",
        "precio": 0.90, "unidad": "unidad", "stock_minimo": 10,
        "stock_maximo": 50, "tiempo_reposicion": 1,
        "historial_ventas": [8, 10, 9, 7, 11, 8, 10, 9, 8, 12, 10, 9, 8, 11, 9, 10, 8, 9, 10, 11]
    },
    "Agua": {
        "id": "PROD004", "nombre": "Agua", "categoria": "Bebidas",
        "precio": 0.60, "unidad": "botella", "stock_minimo": 15,
        "stock_maximo": 100, "tiempo_reposicion": 3,
        "historial_ventas": [10, 12, 11, 9, 13, 10, 12, 11, 10, 14, 12, 11, 10, 13, 11, 12, 10, 11, 12, 13]
    },
    "Café": {
        "id": "PROD005", "nombre": "Café", "categoria": "Bebidas",
        "precio": 4.50, "unidad": "paquete", "stock_minimo": 3,
        "stock_maximo": 25, "tiempo_reposicion": 5,
        "historial_ventas": [1, 2, 1, 3, 2, 1, 2, 3, 1, 2, 3, 1, 2, 1, 3, 2, 1, 2, 1, 3]
    },
    "Arroz": {
        "id": "PROD006", "nombre": "Arroz", "categoria": "Alimentos básicos",
        "precio": 1.80, "unidad": "kg", "stock_minimo": 10,
        "stock_maximo": 60, "tiempo_reposicion": 4,
        "historial_ventas": [3, 4, 3, 5, 4, 3, 4, 5, 3, 4, 5, 3, 4, 3, 5, 4, 3, 4, 3, 5]
    },
    "Aceite": {
        "id": "PROD007", "nombre": "Aceite", "categoria": "Aceites",
        "precio": 4.20, "unidad": "litro", "stock_minimo": 8,
        "stock_maximo": 40, "tiempo_reposicion": 4,
        "historial_ventas": [2, 3, 2, 4, 3, 2, 3, 2, 4, 3, 2, 3, 2, 4, 3, 2, 3, 4, 2, 3]
    },
    "Azúcar": {
        "id": "PROD008", "nombre": "Azúcar", "categoria": "Alimentos básicos",
        "precio": 1.50, "unidad": "kg", "stock_minimo": 10,
        "stock_maximo": 50, "tiempo_reposicion": 3,
        "historial_ventas": [4, 5, 4, 6, 5, 4, 5, 6, 4, 5, 6, 4, 5, 4, 6, 5, 4, 5, 4, 6]
    },
    "Harina": {
        "id": "PROD009", "nombre": "Harina", "categoria": "Alimentos básicos",
        "precio": 1.20, "unidad": "kg", "stock_minimo": 10,
        "stock_maximo": 60, "tiempo_reposicion": 3,
        "historial_ventas": [3, 4, 3, 5, 4, 3, 4, 5, 3, 4, 5, 3, 4, 3, 5, 4, 3, 4, 3, 5]
    },
    "Galletas": {
        "id": "PROD010", "nombre": "Galletas", "categoria": "Snacks",
        "precio": 2.30, "unidad": "paquete", "stock_minimo": 12,
        "stock_maximo": 45, "tiempo_reposicion": 2,
        "historial_ventas": [5, 6, 5, 7, 6, 5, 6, 7, 5, 6, 7, 5, 6, 5, 7, 6, 5, 6, 5, 7]
    },
    "Cereal": {
        "id": "PROD011", "nombre": "Cereal", "categoria": "Desayuno",
        "precio": 3.80, "unidad": "caja", "stock_minimo": 6,
        "stock_maximo": 30, "tiempo_reposicion": 5,
        "historial_ventas": [2, 3, 2, 4, 3, 2, 3, 4, 2, 3, 4, 2, 3, 2, 4, 3, 2, 3, 2, 4]
    }
}

