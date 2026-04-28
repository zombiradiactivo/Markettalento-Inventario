"""
Sistema de Inventario Inteligente
Aplicacion principal - Punto de entrada
"""
from flask import Flask
from config import Config

# Crear instancia de la aplicacion Flask
app = Flask(__name__)
app.config.from_object(Config)

# Importar y registrar rutas
from api.routes import register_routes
register_routes(app)

if __name__ == '__main__':
    print("=" * 60)
    print("SISTEMA DE INVENTARIO INTELIGENTE")
    print("=" * 60)
    print(f"Servidor disponible en: http://{Config.HOST}:{Config.PORT}")
    print("Endpoints disponibles:")
    print("   GET /")
    print("   GET /endpoint")
    print("   GET /api/test")
    print("   GET /api/analizar-inventario")
    print("   GET /api/productos")
    print("   GET /api/producto/<nombre>")
    print("   GET /api/recomendaciones")
    print("=" * 60)
    print("Presiona Ctrl+C para detener")
    print("=" * 60)
    
    app.run(
        debug=Config.DEBUG,
        port=Config.PORT,
        host=Config.HOST
    )
