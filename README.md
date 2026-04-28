# Sistema de Markettalento Inventario Inteligente

Sistema de analisis de inventario que utiliza Vision Artificial (simulada) y Prediccion de Demanda.

## Estructura del Proyecto

```
Markettalento Inventario/
├── app.py                      # Aplicacion principal
├── config.py                   # Configuracion
├── requirements.txt            # Dependencias
├── models/
│   ├── __init__.py
│   └── product.py              # Modelos y base de datos
├── services/
│   ├── __init__.py
│   ├── vision.py               # Servicio de vision artificial
│   ├── prediction.py           # Servicio de prediccion
│   └── inventory               # Servicio de inventario
│       ├── metrics.py
│       ├── recommendations.py
│       └── value.py
├── api/
│   ├── __init__.py
│   └── routes.py               # Rutas de la API
├── templates/
│   ├── index.html              # Dashboard principal
│   └── endpoint.html           # Dashboard de endpoints
├── docs/
│   └── Codigo_Heredado/        # Documentacion del codigo original
└── Codigo_Heredado/            # Archivos originales monolíticos
```

## Instalacion

```bash
pip install -r requirements.txt
```

## Ejecucion

```bash
python app.py
```

O con entorno especifico:

```bash
FLASK_ENV=development python app.py
```

## Endpoints Disponibles

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | / | Dashboard principal |
| GET | /endpoint | Dashboard de endpoints |
| GET | /api/test | Prueba de conexion |
| GET | /api/analizar-inventario | Analisis completo de inventario |
| GET | /api/productos | Catalogo de productos |
| GET | /api/producto/<nombre> | Detalle de producto |
| GET | /api/recomendaciones | Recomendaciones de stock |

## Principios de Diseno

Este proyecto sigue el principio SRP (Single Responsibility Principle):
- **models/**: Gestion de datos y acceso a base de datos
- **services/**: Logica de negocio separada por dominio
- **api/**: Capa de presentacion y rutas HTTP
- **templates/**: Interfaz de usuario separada del codigo Python
