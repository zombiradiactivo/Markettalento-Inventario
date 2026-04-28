from models.product_database import get_product_by_name


def get_product_info(product_name):
    """Obtiene la información de un producto por su nombre"""
    return get_product_by_name(product_name)
