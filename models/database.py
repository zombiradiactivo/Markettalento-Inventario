"""
Configuracion de base de datos con SQLAlchemy puro - Tablas separadas por categoria
"""
from sqlalchemy import Column, String, Float, Integer, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json
import os

Base = declarative_base()
def get_latest_db_path(base_name='inventario.db'):
    """
    Busca la base de datos con el número más alto existente.
    Si no existe ninguna, retorna el nombre base.
    """
    if not os.path.exists(base_name):
        return base_name
    
    name, ext = os.path.splitext(base_name)
    counter = 1
    last_found = base_name
    
    while True:
        current_test = f"{name}_{counter}{ext}"
        if os.path.exists(current_test):
            last_found = current_test
            counter += 1
        else:
            break
            
    return last_found

def get_next_new_path(base_name='inventario.db'):
    """
    Calcula el siguiente nombre que NO existe para crear una nueva.
    """
    if not os.path.exists(base_name):
        return base_name
    
    name, ext = os.path.splitext(base_name)
    counter = 1
    while os.path.exists(f"{name}_{counter}{ext}"):
        counter += 1
    return f"{name}_{counter}{ext}"

# Base de datos por defecto
DB_PATH = get_latest_db_path('inventario.db')
engine = None
SessionLocal = None


def init_engine(db_path=None):
    global engine, SessionLocal, DB_PATH
    if db_path:
        DB_PATH = db_path
    
    db_url = f'sqlite:///{DB_PATH}'
    # El pool_pre_ping ayuda a manejar conexiones en Streamlit
    engine = create_engine(db_url, echo=False, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(bind=engine)


class Refrigerados(Base):
    """Productos refrigerados (frío)"""
    __tablename__ = 'refrigerados'

    id = Column(String(50), primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    precio = Column(Float, nullable=False)
    unidad = Column(String(20), nullable=False)
    stock_minimo = Column(Integer, nullable=False)
    stock_maximo = Column(Integer, nullable=False)
    tiempo_reposicion = Column(Integer, nullable=False)
    historial_ventas = Column(Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'categoria': 'Refrigerados',
            'precio': self.precio,
            'unidad': self.unidad,
            'stock_minimo': self.stock_minimo,
            'stock_maximo': self.stock_maximo,
            'tiempo_reposicion': self.tiempo_reposicion,
            'historial_ventas': json.loads(self.historial_ventas)
        }


class Conservas(Base):
    """Productos en conserva"""
    __tablename__ = 'conservas'

    id = Column(String(50), primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    precio = Column(Float, nullable=False)
    unidad = Column(String(20), nullable=False)
    stock_minimo = Column(Integer, nullable=False)
    stock_maximo = Column(Integer, nullable=False)
    tiempo_reposicion = Column(Integer, nullable=False)
    historial_ventas = Column(Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'categoria': 'Conservas',
            'precio': self.precio,
            'unidad': self.unidad,
            'stock_minimo': self.stock_minimo,
            'stock_maximo': self.stock_maximo,
            'tiempo_reposicion': self.tiempo_reposicion,
            'historial_ventas': json.loads(self.historial_ventas)
        }


class Bebidas(Base):
    """Bebidas"""
    __tablename__ = 'bebidas'

    id = Column(String(50), primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    precio = Column(Float, nullable=False)
    unidad = Column(String(20), nullable=False)
    stock_minimo = Column(Integer, nullable=False)
    stock_maximo = Column(Integer, nullable=False)
    tiempo_reposicion = Column(Integer, nullable=False)
    historial_ventas = Column(Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'categoria': 'Bebidas',
            'precio': self.precio,
            'unidad': self.unidad,
            'stock_minimo': self.stock_minimo,
            'stock_maximo': self.stock_maximo,
            'tiempo_reposicion': self.tiempo_reposicion,
            'historial_ventas': json.loads(self.historial_ventas)
        }


class Panaderia(Base):
    """Productos de panadería"""
    __tablename__ = 'panaderia'

    id = Column(String(50), primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    precio = Column(Float, nullable=False)
    unidad = Column(String(20), nullable=False)
    stock_minimo = Column(Integer, nullable=False)
    stock_maximo = Column(Integer, nullable=False)
    tiempo_reposicion = Column(Integer, nullable=False)
    historial_ventas = Column(Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'categoria': 'Panadería',
            'precio': self.precio,
            'unidad': self.unidad,
            'stock_minimo': self.stock_minimo,
            'stock_maximo': self.stock_maximo,
            'tiempo_reposicion': self.tiempo_reposicion,
            'historial_ventas': json.loads(self.historial_ventas)
        }


class Despensa(Base):
    """Productos de despensa"""
    __tablename__ = 'despensa'

    id = Column(String(50), primary_key=True)
    nombre = Column(String(100), nullable=False, unique=True)
    precio = Column(Float, nullable=False)
    unidad = Column(String(20), nullable=False)
    stock_minimo = Column(Integer, nullable=False)
    stock_maximo = Column(Integer, nullable=False)
    tiempo_reposicion = Column(Integer, nullable=False)
    historial_ventas = Column(Text, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'categoria': 'Despensa',
            'precio': self.precio,
            'unidad': self.unidad,
            'stock_minimo': self.stock_minimo,
            'stock_maximo': self.stock_maximo,
            'tiempo_reposicion': self.tiempo_reposicion,
            'historial_ventas': json.loads(self.historial_ventas)
        }


# Mapeo de categorías a modelos
CATEGORY_MODELS = {
    'Refrigerados': Refrigerados,
    'Conservas': Conservas,
    'Bebidas': Bebidas,
    'Panadería': Panaderia,
    'Despensa': Despensa
}

# # Inicializar engine por defecto
# init_engine()


def get_db_session():
    """Obtiene una nueva sesión de base de datos"""
    return SessionLocal()


def init_db():
    """Crea todas las tablas"""
    Base.metadata.create_all(engine)


def seed_database():
    """Pobla la base de datos con los 25 productos por defecto"""
    from sqlalchemy.orm import Session
    session = SessionLocal()
    try:
        # Verificar si ya hay datos
        if session.query(Refrigerados).count() > 0:
            return False

        # Datos de historial de ventas genericos (20 dias)
        hist_ventas = [3, 4, 5, 2, 6, 4, 5, 3, 4, 6, 5, 4, 3, 5, 4, 6, 3, 5, 4, 5]
        import json

        # Refrigerados
        refrigerados = [
            Refrigerados(id='1', nombre='Leche Entera', precio=1.20, unidad='litro', stock_minimo=5, stock_maximo=30, tiempo_reposicion=2, historial_ventas=json.dumps(hist_ventas)),
            Refrigerados(id='2', nombre='Yogur Natural', precio=0.55, unidad='unidad', stock_minimo=8, stock_maximo=60, tiempo_reposicion=2, historial_ventas=json.dumps(hist_ventas)),
            Refrigerados(id='3', nombre='Queso Fresco', precio=2.80, unidad='pieza', stock_minimo=4, stock_maximo=20, tiempo_reposicion=3, historial_ventas=json.dumps(hist_ventas)),
            Refrigerados(id='4', nombre='Mantequilla', precio=1.95, unidad='tarrina', stock_minimo=4, stock_maximo=25, tiempo_reposicion=4, historial_ventas=json.dumps(hist_ventas)),
            Refrigerados(id='5', nombre='Fiambre Pavo', precio=3.50, unidad='paquete', stock_minimo=3, stock_maximo=18, tiempo_reposicion=2, historial_ventas=json.dumps(hist_ventas)),
            Refrigerados(id='6', nombre='Crema de Leche', precio=0.90, unidad='brik', stock_minimo=5, stock_maximo=35, tiempo_reposicion=3, historial_ventas=json.dumps(hist_ventas)),
            Refrigerados(id='7', nombre='Huevos M', precio=2.50, unidad='docena', stock_minimo=3, stock_maximo=20, tiempo_reposicion=1, historial_ventas=json.dumps(hist_ventas))
        ]

        # Conservas
        conservas = [
            Conservas(id='8', nombre='Atun en Aceite', precio=1.60, unidad='lata', stock_minimo=10, stock_maximo=80, tiempo_reposicion=7, historial_ventas=json.dumps(hist_ventas)),
            Conservas(id='9', nombre='Tomate Triturado', precio=0.75, unidad='bote', stock_minimo=12, stock_maximo=100, tiempo_reposicion=7, historial_ventas=json.dumps(hist_ventas)),
            Conservas(id='10', nombre='Judias Blancas', precio=1.10, unidad='bote', stock_minimo=8, stock_maximo=60, tiempo_reposicion=7, historial_ventas=json.dumps(hist_ventas)),
            Conservas(id='11', nombre='Aceitunas Verdes', precio=1.40, unidad='bote', stock_minimo=6, stock_maximo=50, tiempo_reposicion=10, historial_ventas=json.dumps(hist_ventas)),
            Conservas(id='12', nombre='Sardinas en Aceite', precio=1.80, unidad='lata', stock_minimo=8, stock_maximo=60, tiempo_reposicion=7, historial_ventas=json.dumps(hist_ventas)),
            Conservas(id='13', nombre='Maiz Dulce', precio=0.95, unidad='lata', stock_minimo=6, stock_maximo=50, tiempo_reposicion=7, historial_ventas=json.dumps(hist_ventas))
        ]

        # Bebidas
        bebidas = [
            Bebidas(id='14', nombre='Agua Mineral', precio=0.60, unidad='botella', stock_minimo=15, stock_maximo=100, tiempo_reposicion=3, historial_ventas=json.dumps(hist_ventas)),
            Bebidas(id='15', nombre='Cafe Molido', precio=4.50, unidad='paquete', stock_minimo=3, stock_maximo=25, tiempo_reposicion=5, historial_ventas=json.dumps(hist_ventas)),
            Bebidas(id='16', nombre='Zumo de Naranja UHT', precio=1.35, unidad='brik', stock_minimo=8, stock_maximo=60, tiempo_reposicion=5, historial_ventas=json.dumps(hist_ventas)),
            Bebidas(id='17', nombre='Refresco Cola', precio=1.20, unidad='lata', stock_minimo=10, stock_maximo=80, tiempo_reposicion=4, historial_ventas=json.dumps(hist_ventas)),
            Bebidas(id='18', nombre='Cerveza 1905', precio=1.10, unidad='botella', stock_minimo=6, stock_maximo=50, tiempo_reposicion=5, historial_ventas=json.dumps(hist_ventas))
        ]

        # Panaderia
        panaderia = [
            Panaderia(id='19', nombre='Pan de Molde', precio=1.40, unidad='paquete', stock_minimo=10, stock_maximo=50, tiempo_reposicion=1, historial_ventas=json.dumps(hist_ventas)),
            Panaderia(id='20', nombre='Baguette', precio=0.90, unidad='unidad', stock_minimo=12, stock_maximo=60, tiempo_reposicion=1, historial_ventas=json.dumps(hist_ventas)),
            Panaderia(id='21', nombre='Croissant', precio=0.75, unidad='unidad', stock_minimo=8, stock_maximo=40, tiempo_reposicion=1, historial_ventas=json.dumps(hist_ventas))
        ]

        # Despensa
        despensa = [
            Despensa(id='22', nombre='Arroz', precio=1.80, unidad='kg', stock_minimo=10, stock_maximo=60, tiempo_reposicion=4, historial_ventas=json.dumps(hist_ventas)),
            Despensa(id='23', nombre='Aceite de Oliva', precio=4.20, unidad='litro', stock_minimo=8, stock_maximo=40, tiempo_reposicion=4, historial_ventas=json.dumps(hist_ventas)),
            Despensa(id='24', nombre='Azucar', precio=1.50, unidad='kg', stock_minimo=10, stock_maximo=50, tiempo_reposicion=3, historial_ventas=json.dumps(hist_ventas)),
            Despensa(id='25', nombre='Sal', precio=0.65, unidad='paquete', stock_minimo=5, stock_maximo=30, tiempo_reposicion=3, historial_ventas=json.dumps(hist_ventas))
        ]

        for item in refrigerados + conservas + bebidas + panaderia + despensa:
            session.add(item)
        session.commit()
        return True
    except:
        session.rollback()
        raise
    finally:
        session.close()


def switch_database(db_path=None):
    """
    Cambia la base de datos actual. 
    """
    global DB_PATH, engine
    
    if engine:
        engine.dispose()

    DB_PATH = db_path

    init_engine(DB_PATH)

    return DB_PATH


def get_current_db_path():
    """Retorna la ruta de la base de datos actual"""
    return DB_PATH


def create_new_database():
    """
    Llama a esto solo cuando quieras empezar una DB desde cero (exponencial)
    """
    global DB_PATH, engine
    if engine:
        engine.dispose()
    
    DB_PATH = get_next_new_path('inventario.db')
    
    init_engine(DB_PATH)
    init_db()
    return DB_PATH


# Inicialización automática al cargar el script
init_engine(DB_PATH)