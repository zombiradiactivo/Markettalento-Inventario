"""
Servicio de Inventario - Valor
"""

def calculate_inventory_value(detected_products, product_database):
    """
    Calcula el valor total del inventario detectado.
    
    Args:
        detected_products: Lista de productos detectados
        product_database: Base de datos de productos
    
    Returns:
        float: Valor total del inventario
    """
    total_value = 0
    
    for detected in detected_products:
        product_info = product_database.get(detected["nombre"])
        if product_info and "precio" in product_info:
            total_value += detected["cantidad"] * product_info["precio"]
    
    return round(total_value, 2)
