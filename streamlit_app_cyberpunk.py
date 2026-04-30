"""
Sistema de Inventario Inteligente - Streamlit App (Cyberpunk Edition)
"""
import streamlit as st
import json
from models import database as db
import os
import tkinter as tk
from tkinter import filedialog


def open_file_dialog():
    """Abre el explorador de archivos y retorna la ruta seleccionada"""
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_path = filedialog.askopenfilename(
        title="Seleccionar base de datos",
        filetypes=[("SQLite Database", "*.db"), ("Todos los archivos", "*.*")]
    )
    root.destroy()
    return file_path


# Importar modelos directamente del módulo para que se actualicen dinámicamente
SessionLocal = db.SessionLocal
Refrigerados = db.Refrigerados
Conservas = db.Conservas
Bebidas = db.Bebidas
Panaderia = db.Panaderia
Despensa = db.Despensa
CATEGORY_MODELS = db.CATEGORY_MODELS
init_db = db.init_db
seed_database = db.seed_database
create_new_database = db.create_new_database
switch_database = db.switch_database
get_current_db_path = db.get_current_db_path
DB_PATH = db.DB_PATH

# Inicializar session state para la base de datos
if 'db_initialized' not in st.session_state:
    if not os.path.exists("inventario.db"):
        init_db()
    st.session_state.db_initialized = True
    st.session_state.current_db = DB_PATH
from models.product_database import get_all_products_db, get_product_by_name, add_product, delete_product, update_product
from models.get_sales_history import get_sales_history
from services import detect_products, calculate_inventory_metrics, calculate_inventory_value, predict_stock_outage

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


def get_session():
    """Obtiene una nueva sesion de base de datos"""
    return db.SessionLocal()


def main():
    # Header cyberpunk
    st.markdown("""
    <div class="main-header">
        <h1>⚡ NEONET INVENTORY SYSTEM // 2077</h1>
        <p>>> 25 PRODUCTOS ACTIVOS EN RED | 5 SECTORES MONITOREADOS <<</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar - Panel de Control
    with st.sidebar:
        st.markdown("""
        <h2 style="font-family: 'Orbitron', sans-serif; color: #00f0ff; text-shadow: 0 0 10px #00f0ff;">
        ⚡ CONTROL PANEL
        </h2>
        <p style="font-family: 'Share Tech Mono', monospace; color: #ff00ff;">
        >> NAVEGACIÓN DEL SISTEMA
        </p>
        """, unsafe_allow_html=True)

        # Gestión de base de datos
        st.markdown("""
        <h3 style="font-family: 'Orbitron', sans-serif; color: #ff00ff; font-size: 14px;">
        >> DATABASE CONTROL
        </h3>
        """, unsafe_allow_html=True)
        st.caption(f"BD Actual: {st.session_state.current_db}")

        # Botón para crear base de datos VACÍA
        if st.button("⚡ BD Vacía", use_container_width=True, key="btn_empty_db_cyber"):
            if db.engine:
                db.engine.dispose()
            create_new_database()
            st.session_state.current_db = DB_PATH
            st.success("Base de datos vacía creada")
            st.rerun()

        # Botón para crear base de datos CON productos
        if st.button("⚡ BD con Productos", use_container_width=True, key="btn_seed_db_cyber"):
            if db.engine:
                db.engine.dispose()
            create_new_database()
            seed_database()
            st.session_state.current_db = DB_PATH
            st.success("Base de datos con productos creada")
            st.rerun()

        # Cargar base de datos existente
        col_upload, col_local = st.columns([2, 1])

        with col_upload:
            uploaded_file = st.file_uploader("Cargar BD (upload)", type=['db'], key="db_uploader_cyber")

            if uploaded_file is not None:
                # 1. Creamos un identificador único para procesar este archivo una sola vez
                file_id = f"processed_{uploaded_file.name}_{uploaded_file.size}"
                
                if st.session_state.get("last_processed_file") != file_id:
                    temp_path = f"temp_{uploaded_file.name}"
                    
                    # Escribir el archivo
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    # 2. Cerrar conexiones anteriores de forma segura
                    if db.engine:
                        db.engine.dispose()

                    # 3. Cambiar base de datos
                    switch_database(temp_path)

                    # 4. Actualizar estados
                    st.session_state.current_db = temp_path
                    # Guardamos que ya procesamos este archivo específico
                    st.session_state.last_processed_file = file_id
                    
                    st.success("BD cargada exitosamente")
                    st.rerun()

        with col_local:
            st.markdown("**Cargar BD Local**")
            if st.button("Explorar...", key="btn_browse_cyber", use_container_width=True):
                selected_path = open_file_dialog()
                if selected_path:
                    if db.engine:
                        db.engine.dispose()
                    switch_database(selected_path)
                    st.session_state.current_db = selected_path
                    st.success("BD local cargada")
                    st.rerun()
                else:
                    st.info("No se seleccionó archivo")

        st.divider()

        menu_option = st.selectbox(
            "Seleccione módulo:",
            ["🏠 Inicio [MAINFRAME]", "📦 Catálogo [DATABASE]", "⚙️ Gestión [CRUD]", "🔍 Análisis [AI-VISION]", "📋 Recomendaciones [SYNC]", "⚡ Simulación [SIM]"]
        )

    # Contenido principal
    if "Inicio" in menu_option:
        show_home()
    elif "Catálogo" in menu_option:
        show_products_by_category()
    elif "Gestión" in menu_option:
        show_manage_products()
    elif "Análisis" in menu_option:
        show_inventory_analysis()
    elif "Recomendaciones" in menu_option:
        show_recommendations()
    elif "Simulación" in menu_option:
        show_simulation()


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


def show_manage_products():
    """Interfaz para añadir, editar y eliminar productos"""
    st.markdown("""
    <h2 style="font-family: 'Orbitron', sans-serif; color: #00f0ff; text-shadow: 0 0 10px #00f0ff;">
    >> CRUD INTERFACE: GESTIÓN DE ACTIVOS
    </h2>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["➕ ADD [NEW]", "✏️ EDIT [UNIT]", "🗑️ DELETE [UNIT]"])

    with tab1:
        st.markdown("""
        <h3 style="font-family: 'Share Tech Mono', monospace; color: #00ff00;">
        >> REGISTRAR NUEVO ACTIVO
        </h3>
        """, unsafe_allow_html=True)

        with st.form("add_product_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                categoria = st.selectbox("Sector:", ["Refrigerados", "Conservas", "Bebidas", "Panadería", "Despensa"])
                nombre = st.text_input("Nombre del activo:")
                precio = st.number_input("Precio (€)", min_value=0.0, step=0.01, format="%.2f")
                unidad = st.selectbox("Unidad:", ["litro", "unidad", "pieza", "tarrina", "paquete", "docena", "brik", "botella", "lata", "bote", "kg"])
            with col2:
                stock_min = st.number_input("Stock Mínimo", min_value=0, value=5)
                stock_max = st.number_input("Stock Máximo", min_value=1, value=50)
                tiempo_repo = st.number_input("Tiempo Reposición (días)", min_value=1, value=3)
                id_producto = st.text_input("ID (auto si vacío):")

            st.write(">> Historial de Ventas (20 ciclos):")
            historial_str = st.text_input("Ingrese 20 valores separados por comas:", "3,4,5,2,6,4,5,3,4,6,5,4,3,5,4,6,3,5,4,5")

            submitted = st.form_submit_button("➕ EJECUTAR REGISTRO")

            if submitted:
                if not nombre:
                    st.error(">> ERROR: NOMBRE REQUERIDO")
                else:
                    try:
                        historial = [int(x.strip()) for x in historial_str.split(",")]
                        if len(historial) != 20:
                            st.warning(">> ADVERTENCIA: 20 VALORES REQUERIDOS. USANDO DEFAULT.")
                            historial = [3,4,5,2,6,4,5,3,4,6,5,4,3,5,4,6,3,5,4,5]
                    except:
                        historial = [3,4,5,2,6,4,5,3,4,6,5,4,3,5,4,6,3,5,4,5]

                    try:
                        if not id_producto:
                            productos = get_all_products_db()
                            existing = [int(p['id']) for p in productos if p['id'].isdigit()]
                            id_producto = str(max(existing) + 1) if existing else "1"

                        nuevo = {
                            'id': id_producto,
                            'nombre': nombre,
                            'categoria': categoria,
                            'precio': precio,
                            'unidad': unidad,
                            'stock_minimo': stock_min,
                            'stock_maximo': stock_max,
                            'tiempo_reposicion': tiempo_repo,
                            'historial_ventas': historial
                        }
                        add_product(nuevo)
                        st.success(f">> ÉXITO: ACTIVO '{nombre}' REGISTRADO")
                    except Exception as e:
                        if "UNIQUE" in str(e):
                            st.error(f">> ERROR: ACTIVO '{nombre}' YA EXISTE")
                        else:
                            st.error(f">> ERROR: {str(e)}")

    with tab2:
        st.markdown("""
        <h3 style="font-family: 'Share Tech Mono', monospace; color: #ffff00;">
        >> MODIFICAR ACTIVO EXISTENTE
        </h3>
        """, unsafe_allow_html=True)

        productos = get_all_products_db()
        if productos:
            nombres = [p['nombre'] for p in productos]
            producto_seleccionado = st.selectbox("Seleccionar activo:", nombres)

            if producto_seleccionado:
                producto = get_product_by_name(producto_seleccionado)
                if producto:
                    with st.form("edit_product_form"):
                        col1, col2 = st.columns(2)
                        with col1:
                            categoria = st.selectbox("Sector:", ["Refrigerados", "Conservas", "Bebidas", "Panadería", "Despensa"], index=["Refrigerados", "Conservas", "Bebidas", "Panadería", "Despensa"].index(producto['categoria']))
                            nombre = st.text_input("Nombre del activo:", value=producto['nombre'])
                            precio = st.number_input("Precio (€)", min_value=0.0, step=0.01, format="%.2f", value=producto['precio'])
                            unidad = st.selectbox("Unidad:", ["litro", "unidad", "pieza", "tarrina", "paquete", "docena", "brik", "botella", "lata", "bote", "kg"], index=["litro", "unidad", "pieza", "tarrina", "paquete", "docena", "brik", "botella", "lata", "bote", "kg"].index(producto['unidad']))
                        with col2:
                            stock_min = st.number_input("Stock Mínimo", min_value=0, value=producto['stock_minimo'])
                            stock_max = st.number_input("Stock Máximo", min_value=1, value=producto['stock_maximo'])
                            tiempo_repo = st.number_input("Tiempo Reposición (días)", min_value=1, value=producto['tiempo_reposicion'])
                            id_producto = st.text_input("ID:", value=producto['id'])

                        st.write(">> Historial de Ventas (20 ciclos):")
                        historial_actual = json.loads(producto['historial_ventas']) if isinstance(producto['historial_ventas'], str) else producto['historial_ventas']
                        historial_str = st.text_input("Ingrese 20 valores:", ",".join(map(str, historial_actual)))

                        submitted = st.form_submit_button("✏️ GUARDAR CAMBIOS")

                        if submitted:
                            if not nombre:
                                st.error(">> ERROR: NOMBRE REQUERIDO")
                            else:
                                try:
                                    historial = [int(x.strip()) for x in historial_str.split(",")]
                                    if len(historial) != 20:
                                        st.warning(">> ADVERTENCIA: 20 VALORES REQUERIDOS")
                                except:
                                    historial = historial_actual

                                try:
                                    datos_actualizados = {
                                        'id': id_producto,
                                        'nombre': nombre,
                                        'categoria': categoria,
                                        'precio': precio,
                                        'unidad': unidad,
                                        'stock_minimo': stock_min,
                                        'stock_maximo': stock_max,
                                        'tiempo_reposicion': tiempo_repo,
                                        'historial_ventas': historial
                                    }
                                    update_product(producto_seleccionado, datos_actualizados)
                                    st.success(f">> ÉXITO: ACTIVO '{nombre}' ACTUALIZADO")
                                    st.rerun()
                                except Exception as e:
                                    if "UNIQUE" in str(e):
                                        st.error(f">> ERROR: ACTIVO '{nombre}' YA EXISTE")
                                    else:
                                        st.error(f">> ERROR: {str(e)}")
        else:
            st.warning(">> NO HAY ACTIVOS PARA EDITAR")

    with tab3:
        st.markdown("""
        <h3 style="font-family: 'Share Tech Mono', monospace; color: #ff0040;">
        >> ELIMINAR ACTIVO
        </h3>
        """, unsafe_allow_html=True)

        productos = get_all_products_db()
        if productos:
            for p in productos:
                col1, col2, col3 = st.columns([3,2,1])
                with col1:
                    st.markdown(f"**{p['nombre']}**")
                with col2:
                    st.write(f"€{p['precio']} - {p['categoria']}")
                with col3:
                    if st.button("🗑️", key=f"del_{p['id']}"):
                        st.session_state[f"confirm_{p['id']}"] = True

                if st.session_state.get(f"confirm_{p['id']}", False):
                    st.error(f">> CONFIRMAR: ¿ELIMINAR '{p['nombre']}'?")
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("✅ SÍ", key=f"yes_{p['id']}"):
                            try:
                                delete_product(p['nombre'])
                                st.success(">> ÉXITO: ELIMINADO")
                                st.session_state[f"confirm_{p['id']}"] = False
                                st.rerun()
                            except Exception as e:
                                st.error(f">> ERROR: {e}")
                    with c2:
                        if st.button("❌ NO", key=f"no_{p['id']}"):
                            st.session_state[f"confirm_{p['id']}"] = False
                            st.rerun()
        else:
            st.warning(">> NO HAY ACTIVOS")


def show_inventory_analysis():
    """Muestra el análisis de inventario"""
    st.markdown("""
    <h2 style="font-family: 'Orbitron', sans-serif; color: #00f0ff; text-shadow: 0 0 10px #00f0ff;">
    >> AI-VISION: ANÁLISIS DE RED
    </h2>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="stat-card">
            <h3>0</h3>
            <p>>> UNIDADES ESCANEADAS</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="stat-card" style="border-color: #ff0040; box-shadow: 0 0 5px #ff0040, inset 0 0 15px rgba(255, 0, 64, 0.05);">
            <h3 style="color: #ff0040; text-shadow: 0 0 10px #ff0040;">0</h3>
            <p style="color: #ff0040; text-shadow: 0 0 5px #ff0040;">>> ESTADO CRÍTICO</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="stat-card" style="border-color: #00ff00; box-shadow: 0 0 5px #00ff00, inset 0 0 15px rgba(0, 255, 0, 0.05);">
            <h3 style="color: #00ff00; text-shadow: 0 0 10px #00ff00;">$0</h3>
            <p style="color: #00ff00; text-shadow: 0 0 5px #00ff00;">>> VALOR TOTAL</p>
        </div>
        """, unsafe_allow_html=True)

    if st.button("⚡ EJECUTAR ESCANEO COMPLETO", type="primary"):
        with st.spinner(">> PROCESANDO... AI-VISION ACTIVADA"):
            try:
                deteccion = detect_products()
                productos_detectados = deteccion.get("productos", [])
                productos_db = {p["nombre"]: p for p in get_all_products_db()}
                productos_analizados = []

                for p_det in productos_detectados:
                    nombre = p_det["nombre"]
                    stock_actual = p_det["cantidad"]
                    p_info = productos_db.get(nombre)
                    if p_info:
                        hist = get_sales_history(nombre, days=30)
                        pred = predict_stock_outage(hist, stock_actual, p_info)
                        productos_analizados.append({
                            "producto": nombre,
                            "stock_actual": stock_actual,
                            "categoria": p_info.get("categoria"),
                            "precio": p_info.get("precio"),
                            "dias_hasta_agotarse": pred.get("dias_hasta_agotarse", "N/A"),
                            "estado": pred.get("estado", "Desconocido")
                        })

                analisis = calculate_inventory_metrics(productos_detectados, productos_db)
                valor = calculate_inventory_value(productos_detectados, productos_db)

                col1.metric(">> ESCANEADOS", len(productos_analizados))
                col2.metric(">> CRÍTICOS", analisis["resumen"]["productos_criticos"])
                col3.metric(">> VALOR", f"${valor}")

                if productos_analizados:
                    import pandas as pd
                    st.dataframe(pd.DataFrame(productos_analizados), use_container_width=True)
                st.success(">> ESCANEO COMPLETADO")
            except Exception as e:
                st.error(f">> ERROR: {str(e)}")


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


def show_simulation():
    """Ejecuta simulación visual con estilo cyberpunk"""
    import random
    import pandas as pd
    import time

    st.markdown("""
    <h2 style="font-family: 'Orbitron', sans-serif; color: #00f0ff; text-shadow: 0 0 10px #00f0ff;">
    >> SIMULATION ENGINE // NEONET v2.0
    </h2>
    <p style="font-family: 'Share Tech Mono', monospace; color: #ff00ff;">
    >> INICIANDO SIMULACIÓN DE NEGOCIO EN CYBERSPACE...
    </p>
    """, unsafe_allow_html=True)

    # Parámetros
    col1, col2 = st.columns(2)
    with col1:
        days = st.slider("Ciclos a simular", 30, 365, 90, key="sim_days_cyber")
    with col2:
        speed = st.select_slider("Velocidad", options=["Lenta", "Normal", "Rápida"], value="Normal", key="sim_speed_cyber")

    if st.button("⚡ INICIAR SIMULACIÓN", key="btn_start_sim_cyber", use_container_width=True):
        with st.spinner("Conectando a base de datos..."):
            products = get_all_products_db()
            if not products:
                st.error(">> ERROR: No hay productos en la base de datos")
                return

        # Preparar estados
        product_states = {}
        for p in products:
            avg_sales = sum(p['historial_ventas']) / len(p['historial_ventas']) if p['historial_ventas'] else 3
            product_states[p['id']] = {
                'name': p['nombre'],
                'category': p['categoria'],
                'stock': p['stock_maximo'],
                'stock_min': p['stock_minimo'],
                'stock_max': p['stock_maximo'],
                'lead_time': p['tiempo_reposicion'],
                'avg_sales': avg_sales,
                'price': p['precio'],
                'historial_ventas': p['historial_ventas'],
                'pending_orders': [],
                'total_sales': 0,
                'total_earnings': 0.0,
                'stockout_days': 0
            }

        # Datos
        sim_days = []
        total_sales_list = []
        daily_earnings_list = []
        total_stock_list = []
        stockout_list = []
        orders_list = []
        last_day_transactions = []

        # Elementos visuales
        progress_bar = st.progress(0)
        status_container = st.empty()
        chart_placeholder = st.empty()
        metrics_placeholder = st.empty()

        sleep_time = {"Lenta": 0.2, "Normal": 0.05, "Rápida": 0.01}[speed]

        for day in range(1, days + 1):
            daily_sales = 0
            daily_earnings = 0.0
            daily_stock = 0
            daily_stockouts = 0
            daily_orders = 0
            day_transactions = []

            # Procesar órdenes
            for pid, state in product_states.items():
                new_pending = []
                for arrival_day, qty in state['pending_orders']:
                    if arrival_day == day:
                        state['stock'] += qty
                        daily_orders += 1
                    else:
                        new_pending.append((arrival_day, qty))
                state['pending_orders'] = new_pending

            # Ventas
            for pid, state in product_states.items():
                if state['historial_ventas']:
                    sales = random.choice(state['historial_ventas'])
                else:
                    sales = max(0, int(random.normalvariate(state['avg_sales'], state['avg_sales'] * 0.3)))
                sales = min(sales, state['stock'])
                if sales < 0:
                    sales = 0
                state['stock'] -= sales
                state['total_sales'] += sales
                daily_sales += sales
                daily_stock += state['stock']

                # Calcular ganancias
                earnings = sales * state['price']
                daily_earnings += earnings
                state['total_earnings'] += earnings

                # Registrar transacción para ticket
                if sales > 0:
                    day_transactions.append({
                        'producto': state['name'],
                        'cantidad': sales,
                        'precio_unitario': state['price'],
                        'subtotal': earnings
                    })

                if state['stock'] < state['stock_min']:
                    state['stockout_days'] += 1
                    daily_stockouts += 1

                # Ordenar si stock bajo
                if state['stock'] < state['stock_min'] and not any(arrival > day for arrival, _ in state['pending_orders']):
                    order_qty = state['stock_max'] - state['stock']
                    arrival = day + state['lead_time']
                    state['pending_orders'].append((arrival, order_qty))

            # Registrar
            sim_days.append(day)
            total_sales_list.append(daily_sales)
            daily_earnings_list.append(daily_earnings)
            total_stock_list.append(daily_stock)
            stockout_list.append(daily_stockouts)
            orders_list.append(daily_orders)
            last_day_transactions = day_transactions

            # Actualizar UI
            progress_bar.progress(day / days)
            status_container.markdown(f"""
            <div style="font-family: 'Share Tech Mono', monospace; color: #00f0ff; border: 1px solid #00f0ff; padding: 10px; border-radius: 5px;">
                <h3>>> CYCLE {day}/{days}</h3>
                <p>VENTAS: {daily_sales} unidades | GANANCIAS: ${daily_earnings:.2f} | STOCK: {daily_stock} | QUIEBRES: {daily_stockouts} | ÓRDENES: {daily_orders}</p>
            </div>
            """, unsafe_allow_html=True)

            if day % 5 == 0 or day == days:
                df_live = pd.DataFrame({
                    'Día': sim_days,
                    'Ventas': total_sales_list,
                    'Stock': total_stock_list
                })
                chart_placeholder.line_chart(df_live.set_index('Día'))

            time.sleep(sleep_time)

        status_container.success(">> SIMULACIÓN COMPLETADA")
        progress_bar.empty()

        # Métricas finales
        st.markdown("""
        <h3 style="font-family: 'Orbitron', sans-serif; color: #ff00ff;">
        >> RESULTADOS FINALES
        </h3>
        """, unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Ventas Totales", sum(total_sales_list))
        with col2:
            st.metric("Ganancias Totales", f"${sum(daily_earnings_list):.2f}")
        with col3:
            st.metric("Stock Promedio", f"{total_stock_list[-1] / len(product_states):.1f}")
        with col4:
            st.metric("Días Quiebre", sum(stockout_list))
        with col5:
            st.metric("Órdenes", sum(orders_list))

        # Gráficos
        df_final = pd.DataFrame({
            'Día': sim_days,
            'Ventas': total_sales_list,
            'Ganancias': daily_earnings_list,
            'Stock': total_stock_list,
            'Quiebres': stockout_list,
            'Órdenes': orders_list
        })

        st.line_chart(df_final.set_index('Día')[['Ventas', 'Ganancias', 'Stock']])
        st.bar_chart(df_final.set_index('Día')['Quiebres'])

        # Gráfico de ganancias
        st.subheader("Ganancias Diarias")
        st.line_chart(df_final.set_index('Día')['Ganancias'])

        # Stats por producto
        st.markdown("""
        <h3 style="font-family: 'Orbitron', sans-serif; color: #ff00ff;">
        >> ESTADÍSTICAS POR PRODUCTO
        </h3>
        """, unsafe_allow_html=True)

        product_stats = []
        for pid, state in product_states.items():
            product_stats.append({
                'PRODUCTO': state['name'],
                'CATEGORÍA': state['category'],
                'VENTAS': state['total_sales'],
                'STOCK FINAL': state['stock'],
                'QUIEBRES': state['stockout_days'],
                'ÓRDENES': len(state['pending_orders'])
            })
        st.dataframe(pd.DataFrame(product_stats), use_container_width=True)

        # Ticket de compra - Vista previa
        st.subheader("Ticket de Compra - Vista Previa (Último Día)")
        if last_day_transactions:
            df_ticket = pd.DataFrame(last_day_transactions)
            total_ticket = df_ticket['subtotal'].sum()
            df_ticket['precio_unitario'] = df_ticket['precio_unitario'].apply(lambda x: f"${x:.2f}")
            df_ticket['subtotal'] = df_ticket['subtotal'].apply(lambda x: f"${x:.2f}")
            st.dataframe(df_ticket[['producto', 'cantidad', 'precio_unitario', 'subtotal']], use_container_width=True)
            st.markdown(f"**Total del Ticket: ${total_ticket:.2f}**")
        else:
            st.info("No hubo ventas el último día")


if __name__ == "__main__":
    main()
