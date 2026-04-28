"""
Configuracion de base de datos con SQLAlchemy puro - Tablas separadas por categoria
"""
from sqlalchemy import Column, String, Float, Integer, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

Base = declarative_base()


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

# Engine y Session para uso directo
engine = create_engine('sqlite:///inventario.db', echo=False)
SessionLocal = sessionmaker(bind=engine)


def get_db_session():
    """Obtiene una nueva sesión de base de datos"""
    return SessionLocal()


def init_db():
    """Crea todas las tablas"""
    Base.metadata.create_all(engine)
