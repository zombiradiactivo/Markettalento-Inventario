import streamlit as st

from models.product_database import get_all_products_db


def show_recommendations():
    """Muestra recomendaciones"""
    st.header("Recomendaciones")
    productos = get_all_products_db()
    for producto in productos[:5]:
        with st.expander(f"{producto['nombre']} ({producto['categoria']}) - MEDIA"):
            st.write("**Acción:** REVISAR STOCK")
            st.write(f"**Motivo:** Historial de {len(producto['historial_ventas'])} días")

