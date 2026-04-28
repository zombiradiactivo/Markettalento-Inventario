"""
Rutas de la API Flask
"""
from flask import jsonify, render_template
from datetime import datetime

from models.get_product_info import get_product_info 
from models.get_all_products import get_all_products
from models.get_sales_history import get_sales_history
from services import detect_products, calculate_inventory_metrics, calculate_inventory_value, predict_stock_outage


def register_routes(app):
    """Registra todas las rutas en la aplicación Flask"""
    
    @app.route('/')
    def home():
        """Página principal - Dashboard de inventario"""
        return render_template('index.html')
    
    @app.route('/endpoint')
    def home_endpoint():
        """Dashboard de endpoints de la API"""
        return render_template('endpoint.html')
    
    @app.route('/api/test')
    def test_api():
        """Endpoint de prueba para verificar el estado de la API"""
        return jsonify({
            "status": "success",
            "message": "API de Inventario Inteligente funcionando",
            "version": "1.0",
            "timestamp": datetime.now().isoformat(),
            "servicios": ["vision", "database", "prediction", "inventory"]
        })
    
    @app.route('/api/analizar-inventario')
    def analizar_inventario():
        """Analiza el inventario usando visión artificial y predicción"""
        print("\nINICIANDO ANALISIS DE INVENTARIO")
        
        deteccion = detect_products()
        productos_detectados = deteccion.get("productos", [])
        
        productos_analizados = []
        from models.product_database import get_product_database
        product_database = get_product_database()
        
        for producto_detectado in productos_detectados:
            nombre = producto_detectado["nombre"]
            stock_actual = producto_detectado["cantidad"]
            producto_info = get_product_info(nombre)
            
            if producto_info:
                historial_ventas = get_sales_history(nombre, days=30)
                prediccion = predict_stock_outage(historial_ventas, stock_actual, producto_info)
                productos_analizados.append({
                    "producto": nombre,
                    "stock_actual": stock_actual,
                    "informacion": {
                        "categoria": producto_info.get("categoria"),
                        "precio": producto_info.get("precio")
                    },
                    "prediccion": prediccion
                })
            else:
                productos_analizados.append({
                    "producto": nombre,
                    "stock_actual": stock_actual,
                    "informacion": None,
                    "prediccion": {"dias_hasta_agotarse": "N/A", "estado": "NO ENCONTRADO EN BD"}
                })
        
        analisis = calculate_inventory_metrics(productos_detectados, product_database)
        valor_inventario = calculate_inventory_value(productos_detectados, product_database)
        
        return jsonify({
            "status": "success",
            "timestamp": datetime.now().isoformat(),
            "deteccion": deteccion,
            "productos": productos_analizados,
            "analisis": analisis,
            "valor_inventario": valor_inventario,
            "resumen": {
                "total_productos": len(productos_analizados),
                "productos_criticos": analisis["resumen"]["productos_criticos"],
                "valor_total": valor_inventario
            }
        })
    
    @app.route('/api/productos')
    def obtener_productos():
        """Obtiene el catálogo completo de productos"""
        return jsonify({
            "status": "success",
            "total": len(get_all_products()),
            "productos": get_all_products()
        })
    
    @app.route('/api/producto/<nombre>')
    def obtener_producto(nombre):
        """Obtiene información detallada de un producto específico"""
        producto = get_product_info(nombre)
        if producto:
            return jsonify({"status": "success", "producto": producto})
        else:
            return jsonify({
                "status": "error",
                "message": f"Producto '{nombre}' no encontrado"
            }), 404
    
    @app.route('/api/recomendaciones')
    def obtener_recomendaciones():
        """Obtiene recomendaciones de reposición de stock"""
        productos = get_all_products()
        recomendaciones = []
        
        for producto in productos[:5]:
            recomendaciones.append({
                "producto": producto["nombre"],
                "accion": "REVISAR STOCK",
                "prioridad": "MEDIA",
                "motivo": f"Producto con historial de {len(producto['historial_ventas'])} dias"
            })
        
        return jsonify({
            "status": "success",
            "recomendaciones": recomendaciones,
            "total": len(recomendaciones)
        })
