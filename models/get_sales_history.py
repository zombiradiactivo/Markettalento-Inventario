from models import get_product_info

def get_sales_history(product_name, days=20):
    """Obtiene el historial de ventas de un producto"""
    product = get_product_info(product_name)
    if product:
        return product["historial_ventas"][-days:] if days > 0 else product["historial_ventas"]
    return []

