from models import product_database

def get_all_products():
    """Retorna todos los productos en la base de datos"""
    return list(product_database.values())
