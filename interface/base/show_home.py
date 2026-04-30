
from interface.base.get_session import get_session
import streamlit as st
from models import database as db

Refrigerados = db.Refrigerados
Conservas = db.Conservas
Bebidas = db.Bebidas
Panaderia = db.Panaderia
Despensa = db.Despensa
CATEGORY_MODELS = db.CATEGORY_MODELS


def show_home():
    """Muestra la página de inicio con estadísticas"""
    st.header("Resumen del Inventario")

    session = get_session()
    try:
        refrigerados_count = session.query(Refrigerados).count()
        conservas_count = session.query(Conservas).count()
        bebidas_count = session.query(Bebidas).count()
        panaderia_count = session.query(Panaderia).count()
        despensa_count = session.query(Despensa).count()
    finally:
        session.close()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Refrigerados", refrigerados_count, "7 productos")
    with col2:
        st.metric("Conservas", conservas_count, "6 productos")
    with col3:
        st.metric("Bebidas", bebidas_count, "5 productos")
    with col4:
        st.metric("Panadería", panaderia_count, "3 productos")
    with col5:
        st.metric("Despensa", despensa_count, "4 productos")

    st.info("Total: 25 productos organizados en 5 tablas separadas")

