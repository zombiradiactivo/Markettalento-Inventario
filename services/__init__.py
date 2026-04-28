from .vision import detect_products
from .inventory import calculate_inventory_metrics, generate_recommendations, calculate_inventory_value
from .prediction import predict_stock_outage

__all__ = ['detect_products', 'calculate_inventory_metrics', 'generate_recommendations', 'calculate_inventory_value', 'predict_stock_outage']
