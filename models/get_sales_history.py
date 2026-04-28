from models import get_product_info
import json


def get_sales_history(product_name, days=20):
    """Obtiene el historial de ventas de un producto"""
    product = get_product_info(product_name)
    if product:
        historial = product["historial_ventas"]
        return historial[-days:] if days > 0 else historial
    return []
