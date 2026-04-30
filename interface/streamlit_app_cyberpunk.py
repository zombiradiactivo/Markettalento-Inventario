"""
Sistema de Inventario Inteligente - Streamlit App (Cyberpunk Edition)
"""
import streamlit as st
from models import database as db
import os
from interface.cyberpunk.main import main

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
    page_title="NEONET Inventory System // 2077",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS Cyberpunk
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

    /* Fondo principal con patrón de cuadrícula */
    .stApp {
        background-color: #0a0a0a;
        background-image:
            linear-gradient(rgba(0, 255, 255, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 255, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
    }

    /* Header principal cyberpunk */
    .main-header {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a0033 50%, #0a0a0a 100%);
        border: 2px solid #00f0ff;
        border-radius: 0px;
        padding: 30px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow:
            0 0 10px #00f0ff,
            0 0 20px #00f0ff,
            inset 0 0 30px rgba(0, 240, 255, 0.1);
        position: relative;
        overflow: hidden;
    }

    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #00f0ff, transparent);
        animation: scan 3s linear infinite;
    }

    .main-header h1 {
        font-family: 'Orbitron', sans-serif;
        color: #00f0ff;
        font-size: 2.5em;
        font-weight: 900;
        text-shadow:
            0 0 10px #00f0ff,
            0 0 20px #00f0ff,
            0 0 40px #00f0ff;
        letter-spacing: 3px;
        margin: 0;
    }

    .main-header p {
        font-family: 'Share Tech Mono', monospace;
        color: #ff00ff;
        font-size: 1.1em;
        text-shadow: 0 0 10px #ff00ff;
        margin-top: 10px;
    }

    /* Tarjetas de estadísticas neon */
    .stat-card {
        background: rgba(10, 10, 10, 0.9);
        border: 1px solid #00f0ff;
        border-radius: 0px;
        padding: 20px;
        text-align: center;
        box-shadow:
            0 0 5px #00f0ff,
            inset 0 0 15px rgba(0, 240, 255, 0.05);
        transition: all 0.3s ease;
    }

    .stat-card:hover {
        box-shadow:
            0 0 15px #00f0ff,
            0 0 30px #00f0ff,
            inset 0 0 20px rgba(0, 240, 255, 0.1);
        transform: translateY(-2px);
    }

    .stat-card h3 {
        font-family: 'Orbitron', sans-serif;
        color: #00f0ff;
        font-size: 2em;
        margin: 0;
        text-shadow: 0 0 10px #00f0ff;
    }

    .stat-card p {
        font-family: 'Share Tech Mono', monospace;
        color: #ff00ff;
        margin: 5px 0 0 0;
        text-shadow: 0 0 5px #ff00ff;
    }

    /* Estilo para métricas de Streamlit */
    div[data-testid="metric-container"] {
        background: rgba(10, 10, 10, 0.9);
        border: 1px solid #00f0ff;
        padding: 15px;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
    }

    div[data-testid="metric-container"] label {
        font-family: 'Share Tech Mono', monospace !important;
        color: #ff00ff !important;
    }

    div[data-testid="metric-container"] div[data-testid="metric-value"] {
        font-family: 'Orbitron', sans-serif !important;
        color: #00f0ff !important;
        text-shadow: 0 0 10px #00f0ff;
    }

    /* Sidebar cyberpunk */
    section[data-testid="stSidebar"] {
        background-color: #0a0a0a;
        border-right: 2px solid #00f0ff;
        box-shadow: 5px 0 15px rgba(0, 240, 255, 0.2);
    }

    section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
        font-family: 'Orbitron', sans-serif;
        color: #00f0ff;
        text-shadow: 0 0 10px #00f0ff;
    }

    /* Botones cyberpunk */
    .stButton > button {
        background: transparent;
        color: #00f0ff;
        border: 1px solid #00f0ff;
        font-family: 'Share Tech Mono', monospace;
        text-shadow: 0 0 5px #00f0ff;
        box-shadow: 0 0 10px rgba(0, 240, 255, 0.3);
        transition: all 0.3s ease;
        border-radius: 0px;
    }

    .stButton > button:hover {
        background: rgba(0, 240, 255, 0.1);
        box-shadow:
            0 0 20px #00f0ff,
            0 0 40px #00f0ff;
        transform: translateY(-1px);
    }

    .stButton > button[kind="primary"] {
        background: rgba(0, 240, 255, 0.2);
        border: 2px solid #00f0ff;
        font-weight: bold;
    }

    /* Selectbox y inputs */
    .stSelectbox > div > div,
    .stTextInput > div > div,
    .stNumberInput > div > div,
    .stTextArea > div > div {
        background: rgba(10, 10, 10, 0.9) !important;
        border: 1px solid #00f0ff !important;
        color: #00f0ff !important;
        border-radius: 0px !important;
    }

    .stSelectbox label, .stTextInput label, .stNumberInput label {
        font-family: 'Share Tech Mono', monospace !important;
        color: #ff00ff !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(10, 10, 10, 0.9);
        border-bottom: 2px solid #00f0ff;
    }

    .stTabs [data-baseweb="tab"] {
        font-family: 'Share Tech Mono', monospace;
        color: #666;
        border-radius: 0px;
    }

    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #00f0ff;
        border-bottom: 2px solid #00f0ff;
        text-shadow: 0 0 10px #00f0ff;
    }

    /* Dataframe */
    .stDataFrame {
        border: 1px solid #00f0ff;
    }

    .stDataFrame table {
        background: rgba(10, 10, 10, 0.9) !important;
    }

    .stDataFrame th {
        background: rgba(0, 240, 255, 0.1) !important;
        color: #00f0ff !important;
        font-family: 'Share Tech Mono', monospace;
        border-bottom: 2px solid #00f0ff !important;
    }

    .stDataFrame td {
        color: #fff !important;
        border-bottom: 1px solid rgba(0, 240, 255, 0.2) !important;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(10, 10, 10, 0.9) !important;
        border: 1px solid #00f0ff !important;
        color: #00f0ff !important;
        font-family: 'Share Tech Mono', monospace;
    }

    /* Mensajes de estado */
    .stSuccess {
        background: rgba(0, 255, 0, 0.1) !important;
        border: 1px solid #00ff00 !important;
        color: #00ff00 !important;
    }

    .stError {
        background: rgba(255, 0, 0, 0.1) !important;
        border: 1px solid #ff0040 !important;
        color: #ff0040 !important;
    }

    .stWarning {
        background: rgba(255, 255, 0, 0.1) !important;
        border: 1px solid #ffff00 !important;
        color: #ffff00 !important;
    }

    .stInfo {
        background: rgba(0, 240, 255, 0.1) !important;
        border: 1px solid #00f0ff !important;
        color: #00f0ff !important;
    }

    /* Spinner */
    .stSpinner > div {
        border-top-color: #00f0ff !important;
    }

    /* Animación de escaneo */
    @keyframes scan {
        0% { left: -100%; }
        100% { left: 100%; }
    }

    /* Estilo glitch para texto */
    .glitch {
        font-family: 'Orbitron', sans-serif;
        color: #00f0ff;
        text-shadow:
            0.05em 0 0 rgba(255, 0, 255, 0.75),
            -0.025em -0.05em 0 rgba(0, 255, 0, 0.75),
            0.025em 0.05em 0 rgba(0, 0, 255, 0.75);
        animation: glitch 500ms infinite;
    }

    @keyframes glitch {
        0% { text-shadow: 0.05em 0 0 rgba(255, 0, 255, 0.75), -0.05em -0.025em 0 rgba(0, 255, 0, 0.75), -0.025em 0.05em 0 rgba(0, 0, 255, 0.75); }
        14% { text-shadow: 0.05em 0 0 rgba(255, 0, 255, 0.75), -0.05em -0.025em 0 rgba(0, 255, 0, 0.75), -0.025em 0.05em 0 rgba(0, 0, 255, 0.75); }
        15% { text-shadow: -0.05em -0.025em 0 rgba(255, 0, 255, 0.75), 0.025em 0.025em 0 rgba(0, 255, 0, 0.75), -0.05em -0.05em 0 rgba(0, 0, 255, 0.75); }
        49% { text-shadow: -0.05em -0.025em 0 rgba(255, 0, 255, 0.75), 0.025em 0.025em 0 rgba(0, 255, 0, 0.75), -0.05em -0.05em 0 rgba(0, 0, 255, 0.75); }
        50% { text-shadow: 0.025em 0.05em 0 rgba(255, 0, 255, 0.75), 0.05em 0 0 rgba(0, 255, 0, 0.75), 0 -0.05em 0 rgba(0, 0, 255, 0.75); }
        99% { text-shadow: 0.025em 0.05em 0 rgba(255, 0, 255, 0.75), 0.05em 0 0 rgba(0, 255, 0, 0.75), 0 -0.05em 0 rgba(0, 0, 255, 0.75); }
        100% { text-shadow: -0.025em 0 0 rgba(255, 0, 255, 0.75), -0.025em -0.025em 0 rgba(0, 255, 0, 0.75), -0.025em -0.05em 0 rgba(0, 0, 255, 0.75); }
    }

    /* Terminal text style */
    .terminal-text {
        font-family: 'Share Tech Mono', monospace;
        color: #00ff00;
        text-shadow: 0 0 5px #00ff00;
        font-size: 0.9em;
    }

    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        background: #0a0a0a;
    }

    ::-webkit-scrollbar-thumb {
        background: #00f0ff;
        box-shadow: 0 0 10px #00f0ff;
    }
</style>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
