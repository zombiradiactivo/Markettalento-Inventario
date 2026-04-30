# Arquitectura SRP - Market Talento Inventario

## Principio de Responsabilidad Única (SRP)

El sistema ha sido refactorizado aplicando el Principio de Responsabilidad Única (Single Responsibility Principle), donde cada módulo tiene una única razón para cambiar.

## Estructura de Módulos

```
Markettalento Inventario/
├── models/                    # Capa de datos
│   ├── __init__.py
│   ├── database.py           # Configuración SQLAlchemy y modelos de BD
│   ├── product_database.py    # Operaciones CRUD de productos
│   ├── get_all_products.py   # Consulta de todos los productos
│   ├── get_product_info.py   # Consulta de producto individual
│   └── get_sales_history.py  # Historial de ventas
├── services/                  # Capa de lógica de negocio
│   ├── __init__.py
│   ├── vision/              # Servicio de visión artificial
│   │   ├── __init__.py
│   │   └── vision.py        # Detección simulada de productos
│   ├── prediction/           # Servicio de predicción
│   │   ├── __init__.py
│   │   └── prediction.py    # Predicción de demanda y agotamiento
│   └── inventory/           # Servicios de inventario
│       ├── __init__.py
│       ├── metrics.py        # Cálculo de métricas
│       ├── recommendations.py # Generación de recomendaciones
│       └── value.py          # Cálculo de valor del inventario
├── api/                      # Capa de presentación (API Flask)
│   ├── __init__.py
│   └── routes.py
├── tests/                    # Tests modulares
│   ├── vision/
│   ├── prediction/
│   ├── inventory/
│   └── integration/
├── streamlit_app.py          # Dashboard Streamlit (estilo estándar)
└── streamlit_app_cyberpunk.py  # Dashboard Streamlit (estilo cyberpunk)
```

## Responsabilidades por Módulo

### Models (Capa de Datos)

| Módulo | Responsabilidad | Ubicación |
|---------|-------------------|------------|
| **database.py** | Configuración de SQLAlchemy, definición de modelos ORM para 5 categorías (Refrigerados, Conservas, Bebidas, Panadería, Despensa), creación y sembrado de BD | `models/database.py` |
| **product_database.py** | Operaciones CRUD: add_product, delete_product, update_product, get_all_products_db, get_product_by_name | `models/product_database.py` |
| **get_all_products.py** | Función para obtener todos los productos de la BD | `models/get_all_products.py` |
| **get_product_info.py** | Función para obtener información de un producto específico | `models/get_product_info.py` |
| **get_sales_history.py** | Función para obtener historial de ventas de un producto | `models/get_sales_history.py` |

### Services (Capa de Lógica de Negocio)

| Módulo | Responsabilidad | Ubicación |
|---------|-------------------|------------|
| **vision.py** | Simulación de visión artificial: detecta productos en estanterías/neveras simuladas con niveles de confianza | `services/vision/vision.py` |
| **prediction.py** | Predicción de agotamiento: calcula días hasta agotarse, estado del stock (CRÍTICO, BAJO, MODERADO, ADECUADO) basado en historial de ventas | `services/prediction/prediction.py` |
| **metrics.py** | Cálculo de métricas de inventario: clasifica productos en críticos, bajos y adecuados según stock actual vs mínimo | `services/inventory/metrics.py` |
| **recommendations.py** | Generación de recomendaciones de reposición para productos con stock bajo o agotado | `services/inventory/recommendations.py` |
| **value.py** | Cálculo del valor monetario total del inventario detectado (cantidad × precio) | `services/inventory/value.py` |

### Presentation (Capa de Presentación)

| Módulo | Responsabilidad | Ubicación |
|---------|-------------------|------------|
| **routes.py** | Definición de endpoints Flask: /api/test, /api/analizar-inventario, /api/productos, /api/producto/<nombre>, /api/recomendaciones | `api/routes.py` |
| **streamlit_app.py** | Dashboard interactivo con 6 secciones: Inicio, Ver Productos, Gestionar, Análisis, Recomendaciones, Simulación | `streamlit_app.py` |
| **streamlit_app_cyberpunk.py** | Variante visual cyberpunk del dashboard con CSS personalizado neón | `streamlit_app_cyberpunk.py` |

## Diagrama de Flujo de Datos

```
[Usuario] → [Streamlit App] → [Services Layer]
                                   ↓
                ┌──────────────────┼──────────────────┐
                ↓                  ↓                  ↓
        [Vision Service]    [Prediction]      [Inventory]
        (detecta          (predice           (metrics,
         productos)        agotamiento)      recommendations,
                           ↓                  value)
        [Models Layer] ← [Product Database]
        (SQLAlchemy ORM)
```

## Ventajas de la Arquitectura SRP

1. **Mantenibilidad**: Cada módulo tiene una responsabilidad clara y acotada
2. **Testabilidad**: Los servicios pueden testearse de forma aislada con mocks
3. **Escalabilidad**: Fácil añadir nuevos servicios o categorías sin afectar otros módulos
4. **Reutilización**: Los servicios pueden usarse desde Streamlit, Flask o CLI
5. **Separación de concerns**: Datos, lógica de negocio y presentación están desacoplados
