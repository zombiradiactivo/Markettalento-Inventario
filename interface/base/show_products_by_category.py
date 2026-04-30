from interface.base.get_session import get_session
import streamlit as st
from models import database as db

CATEGORY_MODELS = db.CATEGORY_MODELS

from models.product_database import get_all_products_db

def show_products_by_category():
    """Muestra productos filtrados por categoría"""
    st.header("Catálogo de Productos por Categoría")

    categoria = st.selectbox(
        "Selecciona una categoría",
        ["Todas", "Refrigerados", "Conservas", "Bebidas", "Panadería", "Despensa"]
    )

    session = get_session()
    try:
        if categoria == "Todas":
            productos = get_all_products_db()
        else:
            model = CATEGORY_MODELS.get(categoria)
            productos = [p.to_dict() for p in session.query(model).all()] if model else []
    finally:
        session.close()

    if productos:
        import pandas as pd
        df = pd.DataFrame(productos)
        st.dataframe(df[["id", "nombre", "precio", "unidad", "stock_minimo", "stock_maximo", "tiempo_reposicion"]],
                    use_container_width=True)

        st.subheader("Detalle de Producto")
        nombres = [p["nombre"] for p in productos]
        seleccionado = st.selectbox("Selecciona un producto", nombres)

        if seleccionado:
            producto = next((p for p in productos if p["nombre"] == seleccionado), None)
            if producto:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Precio", f"${producto['precio']}")
                with col2:
                    st.metric("Stock Mínimo", producto['stock_minimo'])
                with col3:
                    st.metric("Stock Máximo", producto['stock_maximo'])

                st.subheader("Historial de Ventas (últimos 20 días)")
                st.line_chart(producto["historial_ventas"])
    else:
        st.warning("No hay productos para mostrar")

