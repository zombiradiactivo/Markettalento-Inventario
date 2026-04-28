"""
Sistema de Inventario Inteligente
Aplicacion principal - Punto de entrada (SQLAlchemy puro)
"""
from flask import Flask
from config import Config
from models.database import init_db, SessionLocal, Refrigerados, Conservas, Bebidas, Panaderia, Despensa
import json


def create_app(config_class=Config):
    """Factory pattern para crear la aplicacion Flask"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Crear tablas e inicializar datos
    init_db()
    seed_database()

    # Importar y registrar rutas
    from api.routes import register_routes
    register_routes(app)

    return app


def seed_database():
    """Pobla la base de datos con los 25 productos exactos"""
    session = SessionLocal()
    try:
        # Verificar si ya hay datos
        if session.query(Refrigerados).count() > 0:
            print("Base de datos ya contiene datos.")
            return

        # Datos de historial de ventas genericos (20 dias)
        hist_ventas = [3, 4, 5, 2, 6, 4, 5, 3, 4, 6, 5, 4, 3, 5, 4, 6, 3, 5, 4, 5]

        # 4.1 — Categoria: Refrigerados (frio)
        refrigerados = [
            Refrigerados(id='1', nombre='Leche Entera', precio=1.20, unidad='litro', stock_minimo=5, stock_maximo=30, tiempo_reposicion=2, historial_ventas=json.dumps(hist_ventas)),
            Refrigerados(id='2', nombre='Yogur Natural', precio=0.55, unidad='unidad', stock_minimo=8, stock_maximo=60, tiempo_reposicion=2, historial_ventas=json.dumps(hist_ventas)),
            Refrigerados(id='3', nombre='Queso Fresco', precio=2.80, unidad='pieza', stock_minimo=4, stock_maximo=20, tiempo_reposicion=3, historial_ventas=json.dumps(hist_ventas)),
            Refrigerados(id='4', nombre='Mantequilla', precio=1.95, unidad='tarrina', stock_minimo=4, stock_maximo=25, tiempo_reposicion=4, historial_ventas=json.dumps(hist_ventas)),
            Refrigerados(id='5', nombre='Fiambre Pavo', precio=3.50, unidad='paquete', stock_minimo=3, stock_maximo=18, tiempo_reposicion=2, historial_ventas=json.dumps(hist_ventas)),
            Refrigerados(id='6', nombre='Crema de Leche', precio=0.90, unidad='brik', stock_minimo=5, stock_maximo=35, tiempo_reposicion=3, historial_ventas=json.dumps(hist_ventas)),
            Refrigerados(id='7', nombre='Huevos M', precio=2.50, unidad='docena', stock_minimo=3, stock_maximo=20, tiempo_reposicion=1, historial_ventas=json.dumps(hist_ventas))
        ]

        # 4.2 — Categoria: Conservas
        conservas = [
            Conservas(id='8', nombre='Atun en Aceite', precio=1.60, unidad='lata', stock_minimo=10, stock_maximo=80, tiempo_reposicion=7, historial_ventas=json.dumps(hist_ventas)),
            Conservas(id='9', nombre='Tomate Triturado', precio=0.75, unidad='bote', stock_minimo=12, stock_maximo=100, tiempo_reposicion=7, historial_ventas=json.dumps(hist_ventas)),
            Conservas(id='10', nombre='Judias Blancas', precio=1.10, unidad='bote', stock_minimo=8, stock_maximo=60, tiempo_reposicion=7, historial_ventas=json.dumps(hist_ventas)),
            Conservas(id='11', nombre='Aceitunas Verdes', precio=1.40, unidad='bote', stock_minimo=6, stock_maximo=50, tiempo_reposicion=10, historial_ventas=json.dumps(hist_ventas)),
            Conservas(id='12', nombre='Sardinas en Aceite', precio=1.80, unidad='lata', stock_minimo=8, stock_maximo=60, tiempo_reposicion=7, historial_ventas=json.dumps(hist_ventas)),
            Conservas(id='13', nombre='Maiz Dulce', precio=0.95, unidad='lata', stock_minimo=6, stock_maximo=50, tiempo_reposicion=7, historial_ventas=json.dumps(hist_ventas))
        ]

        # 4.3 — Categoria: Bebidas
        bebidas = [
            Bebidas(id='14', nombre='Agua Mineral', precio=0.60, unidad='botella', stock_minimo=15, stock_maximo=100, tiempo_reposicion=3, historial_ventas=json.dumps(hist_ventas)),
            Bebidas(id='15', nombre='Cafe Molido', precio=4.50, unidad='paquete', stock_minimo=3, stock_maximo=25, tiempo_reposicion=5, historial_ventas=json.dumps(hist_ventas)),
            Bebidas(id='16', nombre='Zumo de Naranja UHT', precio=1.35, unidad='brik', stock_minimo=8, stock_maximo=60, tiempo_reposicion=5, historial_ventas=json.dumps(hist_ventas)),
            Bebidas(id='17', nombre='Refresco Cola', precio=1.20, unidad='lata', stock_minimo=10, stock_maximo=80, tiempo_reposicion=4, historial_ventas=json.dumps(hist_ventas)),
            Bebidas(id='18', nombre='Cerveza 1905', precio=1.10, unidad='botella', stock_minimo=6, stock_maximo=50, tiempo_reposicion=5, historial_ventas=json.dumps(hist_ventas))
        ]

        # 4.4 — Categoria: Panaderia
        panaderia = [
            Panaderia(id='19', nombre='Pan de Molde', precio=1.40, unidad='paquete', stock_minimo=10, stock_maximo=50, tiempo_reposicion=1, historial_ventas=json.dumps(hist_ventas)),
            Panaderia(id='20', nombre='Baguette', precio=0.90, unidad='unidad', stock_minimo=12, stock_maximo=60, tiempo_reposicion=1, historial_ventas=json.dumps(hist_ventas)),
            Panaderia(id='21', nombre='Croissant', precio=0.75, unidad='unidad', stock_minimo=8, stock_maximo=40, tiempo_reposicion=1, historial_ventas=json.dumps(hist_ventas))
        ]

        # 4.5 — Categoria: Despensa
        despensa = [
            Despensa(id='22', nombre='Arroz', precio=1.80, unidad='kg', stock_minimo=10, stock_maximo=60, tiempo_reposicion=4, historial_ventas=json.dumps(hist_ventas)),
            Despensa(id='23', nombre='Aceite de Oliva', precio=4.20, unidad='litro', stock_minimo=8, stock_maximo=40, tiempo_reposicion=4, historial_ventas=json.dumps(hist_ventas)),
            Despensa(id='24', nombre='Azucar', precio=1.50, unidad='kg', stock_minimo=10, stock_maximo=50, tiempo_reposicion=3, historial_ventas=json.dumps(hist_ventas)),
            Despensa(id='25', nombre='Harina de Trigo', precio=1.20, unidad='kg', stock_minimo=10, stock_maximo=60, tiempo_reposicion=3, historial_ventas=json.dumps(hist_ventas))
        ]

        # Insertar todos los productos
        for producto in refrigerados + conservas + bebidas + panaderia + despensa:
            session.add(producto)

        session.commit()
        print("Base de datos inicializada con 25 productos en 5 tablas.")
    except Exception as e:
        session.rollback()
        print(f"Error al inicializar BD: {e}")
        raise
    finally:
        session.close()


app = create_app()

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
