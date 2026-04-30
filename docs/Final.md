# Memoria Final - Refactorización Market Talento Inventario

**Alumno:** Andrés López González  
**Módulo:** 4 · Refactorización, SRP y CI/CD con Python e IA  
**Fecha:** Abril 2026

---

## 1. Análisis del Código Original

### 1.1 Problemas Críticos Identificados

El código heredado de Market Talento consistía en dos archivos monolíticos:

- **InventarioAlfa.py** (436 líneas)
- **EndPoint_Api.py** (498 líneas)

#### Problemas de Diseño

| Problema | Severidad | Descripción |
|----------|-----------|-------------|
| Monolito no estructurado | 🔴 Crítico | Mezcla lógica de negocio, base de datos simulada, visión artificial, rutas API y HTML en un solo archivo |
| Duplicación de código (~90%) | 🔴 Crítico | ~400 líneas idénticas entre ambos archivos |
| Base de datos en memoria | 🟠 Alto | Variable global mutable `product_database` que se pierde al reiniciar |
| HTML embebido (250+ líneas) | 🟠 Alto | Templates como strings en Python, imposible mantener |
| Violación de SRP | 🔴 Crítico | Una clase/función hace múltiples cosas no relacionadas |
| Sin tests | 🟠 Alto | Imposible refactorizar con seguridad |
| Debug=True en producción | 🔴 Crítico | Riesgo de seguridad grave |

#### Comparativa: Antes vs Después

| Aspecto | Código Heredado | Código Refactorizado |
|----------|-----------------|----------------------|
| Estructura | 2 archivos monolíticos (934 líneas) | 15+ módulos organizados por capas |
| Responsabilidades | Todas mezcladas | SRP aplicado: models/, services/, api/ |
| Base de datos | Dict en memoria duplicado | SQLAlchemy ORM con 5 tablas persistentes |
| Tests | 0 tests | 42+ tests (pytest) |
| CI/CD | No existe | GitHub Actions con matriz 3.9-3.12 |
| Duplicación | ~90% | 0% (código unificado) |

---

## 2. Tabla de Módulos y Responsabilidades

| Módulo | Categoría | Responsabilidad Única | Dependencias |
|---------|-----------|---------------------|-------------|
| `models/database.py` | Datos | Configurar SQLAlchemy, definir modelos ORM, crear/sembrar BD | SQLAlchemy |
| `models/product_database.py` | Datos | CRUD de productos (add, delete, update, get) | database.py |
| `models/get_all_products.py` | Datos | Obtener todos los productos | database.py |
| `models/get_product_info.py` | Datos | Obtener producto por nombre | database.py |
| `models/get_sales_history.py` | Datos | Obtener historial de ventas | database.py |
| `services/vision/vision.py` | Lógica | Simular detección de productos (visión artificial) | random |
| `services/prediction/prediction.py` | Lógica | Predecir días hasta agotamiento y estado | Ninguna |
| `services/inventory/metrics.py` | Lógica | Calcular métricas y clasificar productos | recommendations.py |
| `services/inventory/recommendations.py` | Lógica | Generar recomendaciones de reposición | Ninguna |
| `services/inventory/value.py` | Lógica | Calcular valor monetario del inventario | Ninguna |
| `api/routes.py` | Presentación | Endpoints Flask para API REST | services/, models/ |
| `streamlit_app.py` | Presentación | Dashboard interactivo (estilo estándar) | services/, models/ |
| `streamlit_app_cyberpunk.py` | Presentación | Dashboard interactivo (estilo cyberpunk) | services/, models/ |

---

## 3. Inventario de Uso de IA

### 3.1 Commits con Etiqueta [ai]

| Commit | Descripción | Participación de IA |
|--------|---------------|---------------------|
| [ai] Refactorización inicial de código monolítico | Separación en módulos siguiendo SRP | La IA sugirió la estructura de carpetas y responsabilidades |
| [ai] Creación de servicios de inventario | Métricas, recomendaciones y valor | La IA generó la lógica de cálculo y estructura de returns |
| [ai] Implementación de servicios vision y prediction | Simulación y predicción | La IA aportó la lógica de predicción con tendencia |
| [ai] Creación de tests modulares (services) | 11 archivos de test | La IA generó casos de prueba para edge cases |
| [ai] Creación de tests para Streamlit apps | Tests para streamlit_app.py y cyberpunk | La IA diseñó tests usando mocks y AppTest |
| [ai] Configuración de CI/CD con matriz Python | ci.yml con 3.9, 3.10, 3.11, 3.12 | La IA configuró GitHub Actions y flake8 |
| [ai] Creación de documentación técnica | arquitectura.md y Final.md | La IA redactó la documentación siguiendo estándares |
| [ai] Refactorización de base de datos a SQLAlchemy | database.py con 5 categorías | La IA migró de dict en memoria a ORM |

### 3.2 Herramientas de IA Utilizadas

- **OpenCode (opencode/hy3-preview-free)**: Copiloto principal para refactorización, generación de tests y documentación
- **Metodología**: La IA propuso soluciones, el desarrollador evaluó, probó y ajustó el código

### 3.3 Código Generado por IA vs Manual

| Tipo | % IA | % Manual |
|------|------|---------|
| Refactorización de servicios | 70% | 30% (ajustes y validación) |
| Tests unitarios | 80% | 20% (correcciones de mocks) |
| Documentación | 90% | 10% (revisión final) |
| CI/CD | 85% | 15% (ajuste de rutas) |
| Streamlit apps (originales) | 0% | 100% (código heredado base) |

---

## 4. Reflexión sobre la Matriz de Versiones Python

### 4.1 ¿Por qué una matriz de versiones?

La configuración de GitHub Actions con `strategy.matrix` permite probar el código en múltiples versiones de Python simultáneamente:

```yaml
strategy:
  matrix:
    python-version: ["3.9", "3.10", "3.11", "3.12"]
```

### 4.2 Beneficios Observados

1. **Compatibilidad hacia atrás**: Asegura que el código funcione en Python 3.9+ (usado en muchos servidores de producción)
2. **Preparación para el futuro**: Valida que no hayamos usado características exclusivas de una versión específica
3. **Detección temprana de problemas**: SQLAlchemy 2.0 muestra warnings de deprecación en 3.14 pero funciona en 3.9-3.12
4. **Confianza en despliegues**: Un pipeline verde en 4 versiones garantiza robustez

### 4.3 Retos Encontrados

- **Python 3.14 en desarrollo local**: El pipeline usa 3.9-3.12, pero localmente se usó 3.14 con warnings de SQLAlchemy
- **Dependencias**: streamlit y flask-sqlalchemy requieren versiones específicas para compatibilidad
- **Tests en CI**: Los tests de Streamlit con mocks pueden comportarse diferente según la versión

### 4.4 Conclusión sobre la Matriz

La matriz de versiones es **esencial** para un proyecto que aspira a ser usado en entornos enterprise donde la actualización de Python no siempre es inmediata. Garantiza que Market Talento pueda desplegar en infraestructuras con Python 3.9 sin sorpresas.

---

## 5. Conclusiones del Proyecto

### 5.1 Logros Alcanzados

✅ Código refactorizado aplicando SRP con 0% de duplicación  
✅ 42 tests pasando con cobertura del 25% (95%+ en services/)  
✅ Pipeline CI/CD con matriz de 4 versiones Python  
✅ Documentación técnica completa en formato Google docstrings  
✅ 2 dashboards Streamlit funcionales (estándar y cyberpunk)  
✅ Base de datos SQLAlchemy con 25 productos en 5 categorías  
✅ Commits semánticos con etiqueta [ai] donde participó la IA  

### 5.2 Aprendizajes

1. **La IA es un copilote, no el piloto**: La IA aceleró la generación de código y tests, pero el criterio humano fue fundamental para ajustar mocks y arquitectura
2. **SRP no es solo dividir archivos**: Requiere pensar en responsabilidades y dependencias entre módulos
3. **Los tests son innegociables**: Sin tests, la refactorización es arriesgada
4. **CI/CD temprano**: Configurar el pipeline al inicio evita sorpresas al final

### 5.3 Trabajo Futuro

- Aumentar cobertura de tests al 80%+ extrayendo lógica pura de Streamlit
- Implementar visión artificial real (no simulada) con OpenCV o TensorFlow
- Añadir autenticación JWT a la API Flask
- Desplegar en contenedor Docker con multi-stage build
- Documentación de API con Swagger/OpenAPI

---

**Firma:** Andrés López González  
**Módulo 4:** Refactorización, SRP y CI/CD con Python e IA
