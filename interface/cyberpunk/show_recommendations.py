import streamlit as st

from models.product_database import get_all_products_db


def show_recommendations():
    """Muestra recomendaciones"""
    st.markdown("""
    <h2 style="font-family: 'Orbitron', sans-serif; color: #00f0ff; text-shadow: 0 0 10px #00f0ff;">
    >> SYNC: RECOMENDACIONES DEL SISTEMA
    </h2>
    """, unsafe_allow_html=True)

    productos = get_all_products_db()
    for producto in productos[:5]:
        with st.expander(f"{producto['nombre']} ({producto['categoria']}) - MEDIA"):
            st.markdown("""
            <p style="font-family: 'Share Tech Mono', monospace; color: #ffff00;">
            <strong>>> ACCIÓN:</strong> REVISAR STOCK
            </p>
            """, unsafe_allow_html=True)
            st.write(f">> MOTIVO: Historial de {len(producto['historial_ventas'])} ciclos")

