"""
Sistema de Inventario Inteligente - Streamlit App (SQLAlchemy puro)
"""
import streamlit as st
from models import database as db
import os
from interface.base.main import main

# Importar modelos directamente del módulo para que se actualicen dinámicamente
init_db = db.init_db
DB_PATH = db.DB_PATH

# Inicializar session state para la base de datos
if 'db_initialized' not in st.session_state:
    if not os.path.exists("inventario.db"):
        init_db()
    st.session_state.db_initialized = True
    st.session_state.current_db = DB_PATH

# Configuracion de la pagina
st.set_page_config(
    page_title="Sistema de Inventario Inteligente",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(45deg, #667eea, #764ba2);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    .stat-card {
        background: linear-gradient(45deg, #667eea, #764ba2);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
