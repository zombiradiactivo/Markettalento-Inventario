from models import product_database

def get_product_info(product_name):
    """Obtiene la información de un producto por su nombre"""
    return product_database.get(product_name, None)

