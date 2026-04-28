from models.product_database import get_all_products_db


def get_all_products():
    """Retorna todos los productos en la base de datos"""
    return get_all_products_db()
