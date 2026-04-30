from interface.base.get_session import get_session
import streamlit as st
from models import database as db

CATEGORY_MODELS = db.CATEGORY_MODELS

from models.product_database import get_all_products_db


def show_products_by_category():
    """Muestra productos filtrados por categoría"""
    st.markdown("""
    <h2 style="font-family: 'Orbitron', sans-serif; color: #00f0ff; text-shadow: 0 0 10px #00f0ff;">
    >> DATABASE ACCESS: CATÁLOGO
    </h2>
    """, unsafe_allow_html=True)

    categoria = st.selectbox(
        "Seleccione sector:",
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

        st.markdown("""
        <h3 style="font-family: 'Orbitron', sans-serif; color: #ff00ff; text-shadow: 0 0 10px #ff00ff;">
        >> PRODUCT DETAIL
        </h3>
        """, unsafe_allow_html=True)

        nombres = [p["nombre"] for p in productos]
        seleccionado = st.selectbox("Seleccione unidad:", nombres)

        if seleccionado:
            producto = next((p for p in productos if p["nombre"] == seleccionado), None)
            if producto:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(">> PRECIO", f"${producto['precio']}")
                with col2:
                    st.metric(">> STOCK MIN", producto['stock_minimo'])
                with col3:
                    st.metric(">> STOCK MAX", producto['stock_maximo'])

                st.markdown("""
                <h4 style="font-family: 'Share Tech Mono', monospace; color: #00ff00; text-shadow: 0 0 5px #00ff00;">
                >> SALES LOG (LAST 20 CYCLES)
                </h4>
                """, unsafe_allow_html=True)
                st.line_chart(producto["historial_ventas"])
    else:
        st.warning(">> NO DATA FOUND IN SECTOR")

