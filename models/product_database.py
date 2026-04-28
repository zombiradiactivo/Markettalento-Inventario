"""
Módulo de modelos de productos - Tablas separadas por categoria (SQLAlchemy puro)
"""
from models.database import SessionLocal, Refrigerados, Conservas, Bebidas, Panaderia, Despensa, CATEGORY_MODELS
import json


def get_product_by_name(nombre):
    """Obtiene un producto por su nombre buscando en todas las tablas"""
    session = SessionLocal()
    try:
        for model in [Refrigerados, Conservas, Bebidas, Panaderia, Despensa]:
            product = session.query(model).filter_by(nombre=nombre).first()
            if product:
                return product.to_dict()
        return None
    finally:
        session.close()


def get_all_products_db():
    """Obtiene todos los productos de todas las tablas"""
    session = SessionLocal()
    try:
        products = []
        for model in [Refrigerados, Conservas, Bebidas, Panaderia, Despensa]:
            products.extend([p.to_dict() for p in session.query(model).all()])
        return products
    finally:
        session.close()


def get_products_by_category(categoria):
    """Obtiene productos filtrados por categoria"""
    model = CATEGORY_MODELS.get(categoria)
    if model:
        session = SessionLocal()
        try:
            return [p.to_dict() for p in session.query(model).all()]
        finally:
            session.close()
    return []


def add_product(data):
    """Agrega un nuevo producto a la tabla correspondiente"""
    categoria = data.get('categoria')
    model = CATEGORY_MODELS.get(categoria)

    if not model:
        raise ValueError(f"Categoria desconocida: {categoria}")

    session = SessionLocal()
    try:
        product = model(
            id=data['id'],
            nombre=data['nombre'],
            precio=data['precio'],
            unidad=data['unidad'],
            stock_minimo=data['stock_minimo'],
            stock_maximo=data['stock_maximo'],
            tiempo_reposicion=data['tiempo_reposicion'],
            historial_ventas=json.dumps(data['historial_ventas'])
        )
        session.add(product)
        session.commit()
        return product.to_dict()
    finally:
        session.close()


def update_product_sales(nombre, historial_ventas):
    """Actualiza el historial de ventas de un producto"""
    session = SessionLocal()
    try:
        for model in [Refrigerados, Conservas, Bebidas, Panaderia, Despensa]:
            product = session.query(model).filter_by(nombre=nombre).first()
            if product:
                product.historial_ventas = json.dumps(historial_ventas)
                session.commit()
                return product.to_dict()
        return None
    finally:
        session.close()


def get_product_database():
    """Retorna todos los productos como diccionario (para compatibilidad)"""
    products = get_all_products_db()
    result = {}
    for p in products:
        result[p['nombre']] = p
    return result


def update_product(nombre_original, data):
    """Actualiza un producto existente"""
    session = SessionLocal()
    try:
        product = None
        old_model = None
        for model in [Refrigerados, Conservas, Bebidas, Panaderia, Despensa]:
            product = session.query(model).filter_by(nombre=nombre_original).first()
            if product:
                old_model = model
                break

        if not product:
            return None

        old_categoria = None
        for cat, mod in CATEGORY_MODELS.items():
            if mod == old_model:
                old_categoria = cat
                break

        new_categoria = data.get('categoria', old_categoria)

        if new_categoria != old_categoria:
            session.delete(product)
            session.commit()

            new_model = CATEGORY_MODELS.get(new_categoria)
            if not new_model:
                raise ValueError(f"Categoria desconocida: {new_categoria}")

            historial = data.get('historial_ventas', [])
            if isinstance(historial, str):
                historial = json.loads(historial)

            new_product = new_model(
                id=data.get('id', product.id),
                nombre=data['nombre'],
                precio=data['precio'],
                unidad=data['unidad'],
                stock_minimo=data['stock_minimo'],
                stock_maximo=data['stock_maximo'],
                tiempo_reposicion=data['tiempo_reposicion'],
                historial_ventas=json.dumps(historial)
            )
            session.add(new_product)
            session.commit()
            return new_product.to_dict()
        else:
            product.nombre = data['nombre']
            product.precio = data['precio']
            product.unidad = data['unidad']
            product.stock_minimo = data['stock_minimo']
            product.stock_maximo = data['stock_maximo']
            product.tiempo_reposicion = data['tiempo_reposicion']
            if 'historial_ventas' in data:
                historial = data['historial_ventas']
                product.historial_ventas = json.dumps(historial) if isinstance(historial, list) else historial
            session.commit()
            return product.to_dict()
    finally:
        session.close()


def delete_product(nombre):
    """Elimina un producto por su nombre"""
    session = SessionLocal()
    try:
        for model in [Refrigerados, Conservas, Bebidas, Panaderia, Despensa]:
            product = session.query(model).filter_by(nombre=nombre).first()
            if product:
                session.delete(product)
                session.commit()
                return True
        return False
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
