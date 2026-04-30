
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
    st.markdown("""
    <h2 style="font-family: 'Orbitron', sans-serif; color: #00f0ff; text-shadow: 0 0 10px #00f0ff;">
    >> MAINFRAME STATUS
    </h2>
    """, unsafe_allow_html=True)

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
        st.markdown(f"""
        <div class="stat-card">
            <h3>{refrigerados_count}</h3>
            <p>>> REFRIGERADOS</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <h3>{conservas_count}</h3>
            <p>>> CONSERVAS</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <h3>{bebidas_count}</h3>
            <p>>> BEBIDAS</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <h3>{panaderia_count}</h3>
            <p>>> PANADERÍA</p>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="stat-card">
            <h3>{despensa_count}</h3>
            <p>>> DESPENSA</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="margin-top: 20px; padding: 15px; border: 1px solid #00f0ff; background: rgba(0, 240, 255, 0.05);">
        <p style="font-family: 'Share Tech Mono', monospace; color: #00f0ff; margin: 0;">
        >> SYSTEM STATUS: <span style="color: #00ff00;">ONLINE</span> | TOTAL: 25 PRODUCTOS EN 5 SECTORES
        </p>
    </div>
    """, unsafe_allow_html=True)

