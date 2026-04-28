# Análisis de Problemas de Diseño - Código Heredado

**Fecha:** Abril 2024  
**Archivos analizados:**
- `Codigo_Heredado/InventarioAlfa.py` (436 líneas)
- `Codigo_Heredado/EndPoint_Api.py` (498 líneas)

---

## 1. Problemas Críticos de Diseño

### 1.1 Monolito No Estructurado
Ambos archivos son monolíticos que mezclan:
- Base de datos simulada (en memoria)
- Lógica de visión artificial (simulada)
- Lógica de inventario
- Servicio de predicción
- Rutas de API Flask
- Templates HTML embebidos
- Configuración de servidor

**Impacto:** Difícil mantenimiento, testing imposible, violación del principio de responsabilidad única (SRP).

### 1.2 Duplicación de Código (~90%)
`InventarioAlfa.py` y `EndPoint_Api.py` contienen casi el mismo código:
- Misma base de datos (`product_database`)
- Mismas funciones: `get_product_info()`, `get_sales_history()`, `get_all_products()`
- Mismo servicio de visión artificial (`detect_products()`)
- Misma lógica de inventario (`calculate_inventory_metrics()`, etc.)
- Mismo servicio de predicción (`predict_stock_outage()`)

**Líneas duplicadas:** ~400 líneas idénticas entre ambos archivos.

### 1.3 HTML Embebido como String
El template HTML (250+ líneas) está embebido como string en el código Python:
```python
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="es">
...
'''
```

**Problemas:**
- Syntax highlighting inexistente
- Difícil edición y mantenimiento
- Mezcla de capas (presentación vs lógica)
- Imposible usar herramientas de linting HTML/CSS/JS

---

## 2. Problemas de Base de Datos

### 2.1 Base de Datos Simulada en Memoria
```python
product_database = {
    "Leche": { "id": "PROD001", ... },
    ...
}
```

**Problemas:**
- No hay persistencia (se pierde al reiniciar)
- Variable global mutable
- No hay índices ni estructura de consulta
- No hay validación de datos

### 2.2 Error de Indentación en Datos
En ambos archivos, el producto "Aceite" tiene indentación incorrecta:
```python
    "Arroz": { ... },
        "Aceite": {  # <- Indentación extra (4 espacios de más)
        "id": "PROD007",
```

Esto sugiere que el diccionario podría estar mal formado (aunque Python lo acepte).

---

## 3. Problemas de API y Flask

### 3.1 Mezcla de Responsabilidades en Rutas
Las rutas Flask contienen lógica de negocio directamente:
```python
@app.route('/api/analizar-inventario')
def analizar_inventario():
    # 20+ líneas de lógica de negocio aquí
```

### 3.2 Falta de Manejo de Errores
No hay bloques try-except en las rutas:
- Si `detect_products()` falla, la API crashea
- Si hay error en cálculos, no hay respuesta de error controlada

### 3.3 Hardcoded Ports y Configuración
```python
app.run(debug=True, port=5005, host='0.0.0.0')  # InventarioAlfa.py
app.run(debug=True, port=5002, host='0.0.0.0')  # EndPoint_Api.py
```

**Problemas:**
- Puertos hardcodeados (difícil despliegue)
- `debug=True` en producción es riesgo de seguridad
- No hay archivo de configuración externo

### 3.4 Inconsistencia en Endpoints
| InventarioAlfa.py | EndPoint_Api.py |
|-------------------|-----------------|
| `/api/test` | `/api/test` |
| `/api/analizar-inventario` | `/api/analizar-inventario` |
| `/api/productos` | `/api/productos` |
| - | `/api/producto/<nombre>` (nuevo) |
| - | `/api/recomendaciones` (nuevo) |

---

## 4. Problemas de Código y Estilo

### 4.1 Uso de Emojis en Código
```python
print("📸 Analizando imagen...")
return {"status": "success", "message": "✅ API funcionando"}
```

**Problemas:**
- Posibles errores de codificación en diferentes entornos
- Mezcla de propósitos: emojis decorativos vs datos JSON
- Difícil lectura en logs de servidor

### 4.2 Imports No Utilizados
```python
from datetime import datetime, timedelta  # timedelta no se usa
import statistics  # statistics no se usa
```

### 4.3 Mezcla de Idiomas
- Nombres de funciones: inglés (`get_product_info`, `predict_stock_outage`)
- Comentarios y mensajes: español
- Nombres de productos: español
- Variables en rutas: español (`obtener_producto`)

### 4.4 Falta de Docstrings
Ninguna función tiene documentación:
```python
def calculate_inventory_metrics(detected_products, product_database):
    # No hay docstring explicando qué hace, parámetros, o retorno
```

### 4.5 Variables Globales Mutable
`product_database` es modificable globalmente sin control.

---

## 5. Problemas de Lógica de Negocio

### 5.1 Visión Artificial Simulada con Random
```python
def detect_products(image_path=None):
    escenario = random.choice(escenarios)
```

**Problemas:**
- Resultados no reproducibles
- No hay parámetro real de imagen (se ignora `image_path`)
- Datos simulados hardcodeados

### 5.2 Predicción Simplista
```python
avg_daily_sales = sum(sales_history) / len(sales_history)
```

**Limitaciones:**
- Promedio simple, no considera estacionalidad
- No hay validación de datos anómalos
- `days_until_out` puede dar resultados irreales

### 5.3 Cálculos de Recomendación Arbitrarios
```python
rec = f"📦 Reponer {stock_minimo * 2 - stock_actual} unidades"
```

No hay base matemática sólida para `stock_minimo * 2`.

---

## 6. Problemas de Seguridad

### 6.1 Debug=True en Producción
```python
app.run(debug=True, ...)
```
Expone información sensible y permite ejecución remota de código.

### 6.2 Sin Validación de Entrada
```python
@app.route('/api/producto/<nombre>')
def obtener_producto(nombre):
    producto = get_product_info(nombre)  # Sin validar 'nombre'
```

### 6.3 Sin Autenticación/Autorización
Cualquiera puede acceder a todos los endpoints.

---

## 7. Problemas de Testing

- No hay pruebas unitarias
- No hay pruebas de integración
- El uso de `random` hace imposible tests deterministas
- HTML embebido impide tests de interfaz

---

## 8. Problemas de Frontend

### 8.1 JavaScript Inline y jQuery-style
Uso de `onclick` en HTML y `fetch` sin manejo robusto de errores.

### 8.2 CDN Dependencies
```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css">
```
Sin fallback si no hay internet.

### 8.3 HTML Duplicado
Ambos archivos tienen su propio `HTML_TEMPLATE` con variaciones menores.

---

## 9. Resumen de Problemas por Severidad

| Severidad | Problema | Archivos |
|-----------|----------|---------|
| 🔴 Crítico | Monolito no estructurado | Ambos |
| 🔴 Crítico | 90% código duplicado | Ambos |
| 🔴 Crítico | debug=True en producción | Ambos |
| 🟠 Alto | HTML embebido (250+ líneas) | Ambos |
| 🟠 Alto | Sin manejo de errores | Ambos |
| 🟠 Alto | Base de datos en memoria sin persistencia | Ambos |
| 🟡 Medio | Emojis en código/logs | Ambos |
| 🟡 Medio | Imports no utilizados | Ambos |
| 🟡 Medio | Mezcla de idiomas | Ambos |
| 🟡 Medio | Sin docstrings | Ambos |
| 🟡 Medio | Inconsistencia en endpoints | Diferente |
| 🟢 Bajo | Error de indentación en datos | Ambos |

---

## 10. Recomendaciones de Refactorización

1. **Separar en módulos:**
   - `models.py` - Modelos de datos
   - `database.py` - Capa de datos (usar SQLite/PostgreSQL)
   - `services/vision.py` - Servicio de visión artificial
   - `services/inventory.py` - Lógica de inventario
   - `services/prediction.py` - Servicio de predicción
   - `api/routes.py` - Rutas Flask
   - `templates/` - Templates HTML separados
   - `static/` - CSS/JS separados
   - `config.py` - Configuración
   - `tests/` - Pruebas unitarias

2. **Eliminar duplicación:** Unificar en una sola base de código

3. **Usar Flask Blueprints** para organizar rutas

4. **Usar SQLAlchemy** para ORM y persistencia

5. **Agregar validación** con Pydantic o Marshmallow

6. **Configurar entorno:** Usar `python-dotenv` para configuración

7. **Agregar logging** estructurado en lugar de `print()`

8. **Documentar API** con OpenAPI/Swagger

9. **Agregar tests** con pytest

10. **Usar un motor de templates** real (Jinja2 files separados)
