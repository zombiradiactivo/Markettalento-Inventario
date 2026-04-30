"""
Sistema de Inventario Inteligente - Streamlit App (SQLAlchemy puro)
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


def get_session():
    """Obtiene una nueva sesion de base de datos"""
    return db.SessionLocal()


def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>Sistema de Inventario Inteligente</h1>
        <p>25 Productos en 5 Categorías</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar - Panel de Control
    with st.sidebar:
        st.header("Panel de Control")

        # Gestión de base de datos
        st.subheader("Base de Datos")
        st.caption(f"Actual: {st.session_state.current_db}")

        # Botón para crear base de datos VACÍA
        if st.button("Crear BD Vacía", use_container_width=True, key="btn_empty_db"):
            if db.engine:
                db.engine.dispose()
            create_new_database()
            st.session_state.current_db = DB_PATH
            st.success("Base de datos vacía creada")
            st.rerun()

        # Botón para crear base de datos CON productos por defecto
        if st.button("Crear BD con Productos", use_container_width=True, key="btn_seed_db"):
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
            uploaded_file = st.file_uploader("Cargar BD (upload)", type=['db'], key="db_uploader")

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
            if st.button("Explorar...", key="btn_browse", use_container_width=True):
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
            "Selecciona una opcion",
            ["Inicio", "Ver Productos por Categoría", "Gestionar Productos", "Analizar Inventario", "Recomendaciones", "Simulación"]
        )

    # Contenido principal
    if menu_option == "Inicio":
        show_home()
    elif menu_option == "Ver Productos por Categoría":
        show_products_by_category()
    elif menu_option == "Gestionar Productos":
        show_manage_products()
    elif menu_option == "Analizar Inventario":
        show_inventory_analysis()
    elif menu_option == "Recomendaciones":
        show_recommendations()
    elif menu_option == "Simulación":
        show_simulation()


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


def show_manage_products():
    """Interfaz para añadir, editar y eliminar productos"""
    st.header("Gestión de Productos")

    tab1, tab2, tab3 = st.tabs(["➕ Añadir Producto", "✏️ Editar Producto", "🗑️ Eliminar Producto"])

    with tab1:
        st.subheader("Añadir Nuevo Producto")
        with st.form("add_product_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                categoria = st.selectbox("Categoría", ["Refrigerados", "Conservas", "Bebidas", "Panadería", "Despensa"])
                nombre = st.text_input("Nombre del Producto")
                precio = st.number_input("Precio (€)", min_value=0.0, step=0.01, format="%.2f")
                unidad = st.selectbox("Unidad", ["litro", "unidad", "pieza", "tarrina", "paquete", "docena", "brik", "botella", "lata", "bote", "kg"])
            with col2:
                stock_min = st.number_input("Stock Mínimo", min_value=0, value=5)
                stock_max = st.number_input("Stock Máximo", min_value=1, value=50)
                tiempo_repo = st.number_input("Tiempo Reposición (días)", min_value=1, value=3)
                id_producto = st.text_input("ID (dejar vacío para auto)")

            st.write("Historial de Ventas (últimos 20 días)")
            historial_str = st.text_input("Ingrese 20 números separados por comas", "3,4,5,2,6,4,5,3,4,6,5,4,3,5,4,6,3,5,4,5")

            submitted = st.form_submit_button("➕ Añadir Producto")

            if submitted:
                if not nombre:
                    st.error("El nombre del producto es obligatorio")
                else:
                    try:
                        historial = [int(x.strip()) for x in historial_str.split(",")]
                        if len(historial) != 20:
                            st.warning("Se requieren 20 valores. Usando valores por defecto.")
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
                        st.success(f"✅ Producto '{nombre}' añadido correctamente")
                    except Exception as e:
                        if "UNIQUE" in str(e):
                            st.error(f"Error: Ya existe un producto con el nombre '{nombre}'")
                        else:
                            st.error(f"Error: {str(e)}")

    with tab2:
        st.subheader("Editar Producto")
        productos = get_all_products_db()
        if productos:
            nombres = [p['nombre'] for p in productos]
            producto_seleccionado = st.selectbox("Seleccionar producto a editar", nombres)

            if producto_seleccionado:
                producto = get_product_by_name(producto_seleccionado)
                if producto:
                    with st.form("edit_product_form"):
                        col1, col2 = st.columns(2)
                        with col1:
                            categoria = st.selectbox("Categoría", ["Refrigerados", "Conservas", "Bebidas", "Panadería", "Despensa"], index=["Refrigerados", "Conservas", "Bebidas", "Panadería", "Despensa"].index(producto['categoria']))
                            nombre = st.text_input("Nombre del Producto", value=producto['nombre'])
                            precio = st.number_input("Precio (€)", min_value=0.0, step=0.01, format="%.2f", value=producto['precio'])
                            unidad = st.selectbox("Unidad", ["litro", "unidad", "pieza", "tarrina", "paquete", "docena", "brik", "botella", "lata", "bote", "kg"], index=["litro", "unidad", "pieza", "tarrina", "paquete", "docena", "brik", "botella", "lata", "bote", "kg"].index(producto['unidad']))
                        with col2:
                            stock_min = st.number_input("Stock Mínimo", min_value=0, value=producto['stock_minimo'])
                            stock_max = st.number_input("Stock Máximo", min_value=1, value=producto['stock_maximo'])
                            tiempo_repo = st.number_input("Tiempo Reposición (días)", min_value=1, value=producto['tiempo_reposicion'])
                            id_producto = st.text_input("ID", value=producto['id'])

                        st.write("Historial de Ventas (últimos 20 días)")
                        historial_actual = json.loads(producto['historial_ventas']) if isinstance(producto['historial_ventas'], str) else producto['historial_ventas']
                        historial_str = st.text_input("Ingrese 20 números separados por comas", ",".join(map(str, historial_actual)))

                        submitted = st.form_submit_button("✏️ Guardar Cambios")

                        if submitted:
                            if not nombre:
                                st.error("El nombre del producto es obligatorio")
                            else:
                                try:
                                    historial = [int(x.strip()) for x in historial_str.split(",")]
                                    if len(historial) != 20:
                                        st.warning("Se requieren 20 valores.")
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
                                    st.success(f"✅ Producto '{nombre}' actualizado correctamente")
                                    st.rerun()
                                except Exception as e:
                                    if "UNIQUE" in str(e):
                                        st.error(f"Error: Ya existe un producto con el nombre '{nombre}'")
                                    else:
                                        st.error(f"Error: {str(e)}")
        else:
            st.warning("No hay productos para editar")

    with tab3:
        st.subheader("Eliminar Producto")
        productos = get_all_products_db()
        if productos:
            for p in productos:
                col1, col2, col3 = st.columns([3,2,1])
                with col1:
                    st.write(f"**{p['nombre']}**")
                with col2:
                    st.write(f"€{p['precio']} - {p['categoria']}")
                with col3:
                    if st.button("🗑️", key=f"del_{p['id']}"):
                        st.session_state[f"confirm_{p['id']}"] = True

                if st.session_state.get(f"confirm_{p['id']}", False):
                    st.warning(f"¿Eliminar '{p['nombre']}'?")
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("✅ Sí", key=f"yes_{p['id']}"):
                            try:
                                delete_product(p['nombre'])
                                st.success(f"✅ Eliminado")
                                st.session_state[f"confirm_{p['id']}"] = False
                                st.rerun()
                            except Exception as e:
                                st.error(f"Error: {e}")
                    with c2:
                        if st.button("❌ No", key=f"no_{p['id']}"):
                            st.session_state[f"confirm_{p['id']}"] = False
                            st.rerun()
        else:
            st.warning("No hay productos")


def show_inventory_analysis():
    """Muestra el análisis de inventario"""
    st.header("Análisis de Inventario")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""<div class="stat-card"><h3>0</h3><p>Productos Analizados</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="stat-card" style="background:linear-gradient(45deg,#dc3545,#ff6b6b);"><h3>0</h3><p>Productos Críticos</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="stat-card" style="background:linear-gradient(45deg,#28a745,#51cf66);"><h3>$0</h3><p>Valor Inventario</p></div>""", unsafe_allow_html=True)

    if st.button("Ejecutar Análisis Completo", type="primary"):
        with st.spinner("Analizando..."):
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

                col1.metric("Productos Analizados", len(productos_analizados))
                col2.metric("Críticos", analisis["resumen"]["productos_criticos"])
                col3.metric("Valor", f"${valor}")

                if productos_analizados:
                    import pandas as pd
                    st.dataframe(pd.DataFrame(productos_analizados), use_container_width=True)
                st.success("Análisis completado!")
            except Exception as e:
                st.error(f"Error: {str(e)}")


def show_recommendations():
    """Muestra recomendaciones"""
    st.header("Recomendaciones")
    productos = get_all_products_db()
    for producto in productos[:5]:
        with st.expander(f"{producto['nombre']} ({producto['categoria']}) - MEDIA"):
            st.write("**Acción:** REVISAR STOCK")
            st.write(f"**Motivo:** Historial de {len(producto['historial_ventas'])} días")


def show_simulation():
    """Ejecuta una simulación visual del negocio"""
    import random
    import pandas as pd
    import time

    st.header("Simulación de Negocio")
    st.write("Simulación visual de ventas e inventario a lo largo del tiempo.")

    # Parámetros de simulación
    col1, col2 = st.columns(2)
    with col1:
        days = st.slider("Días a simular", 30, 365, 90, key="sim_days")
    with col2:
        speed = st.select_slider("Velocidad", options=["Lenta", "Normal", "Rápida"], value="Normal")

    if st.button("Iniciar Simulación", key="btn_start_sim", use_container_width=True):
        with st.spinner("Cargando productos..."):
            products = get_all_products_db()
            if not products:
                st.warning("No hay productos en la base de datos. Crea una base de datos con productos primero.")
                return

        # Preparar estados iniciales de productos
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
                'total_earnings': 0,
                'stockout_days': 0
            }

        # Datos de simulación
        sim_days = []
        total_sales_list = []
        daily_earnings_list = []
        total_stock_list = []
        stockout_list = []
        orders_list = []
        last_day_transactions = []

        # Elementos visuales
        progress_bar = st.progress(0)
        status_text = st.empty()
        chart_placeholder = st.empty()
        metrics_placeholder = st.empty()

        # Velocidad
        sleep_time = {"Lenta": 0.2, "Normal": 0.05, "Rápida": 0.01}[speed]

        for day in range(1, days + 1):
            daily_sales = 0
            daily_earnings = 0.0
            daily_stock = 0
            daily_stockouts = 0
            daily_orders = 0
            day_transactions = []

            # Procesar órdenes que llegan hoy
            for pid, state in product_states.items():
                new_pending = []
                for arrival_day, qty in state['pending_orders']:
                    if arrival_day == day:
                        state['stock'] += qty
                        daily_orders += 1
                    else:
                        new_pending.append((arrival_day, qty))
                state['pending_orders'] = new_pending

            # Simular ventas
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

                # Generar orden si stock bajo
                if state['stock'] < state['stock_min'] and not any(arrival > day for arrival, _ in state['pending_orders']):
                    order_qty = state['stock_max'] - state['stock']
                    arrival = day + state['lead_time']
                    state['pending_orders'].append((arrival, order_qty))

            # Registrar datos
            sim_days.append(day)
            total_sales_list.append(daily_sales)
            daily_earnings_list.append(daily_earnings)
            total_stock_list.append(daily_stock)
            stockout_list.append(daily_stockouts)
            orders_list.append(daily_orders)
            last_day_transactions = day_transactions

            # Actualizar visualización
            progress_bar.progress(day / days)
            status_text.markdown(f"""
            **Día {day}/{days}**
            - Ventas hoy: {daily_sales}
            - Ganancias: ${daily_earnings:.2f}
            - Stock total: {daily_stock}
            - Quiebres: {daily_stockouts}
            - Órdenes recibidas: {daily_orders}
            """)

            # Actualizar gráfico en vivo
            if day % 5 == 0 or day == days:
                df_live = pd.DataFrame({
                    'Día': sim_days,
                    'Ventas': total_sales_list,
                    'Stock': total_stock_list
                })
                chart_placeholder.line_chart(df_live.set_index('Día'))

            time.sleep(sleep_time)

        status_text.success("¡Simulación completada!")
        progress_bar.empty()

        # Métricas finales
        st.subheader("Resultados Finales")
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Ventas Totales", sum(total_sales_list))
        with col2:
            st.metric("Ganancias Totales", f"${sum(daily_earnings_list):.2f}")
        with col3:
            st.metric("Stock Final Promedio", f"{total_stock_list[-1] / len(product_states):.1f}")
        with col4:
            st.metric("Días con Quiebre", sum(stockout_list))
        with col5:
            st.metric("Órdenes Realizadas", sum(orders_list))

        # Gráficos completos
        st.subheader("Gráficos de la Simulación")
        df_final = pd.DataFrame({
            'Día': sim_days,
            'Ventas Diarias': total_sales_list,
            'Ganancias Diarias': daily_earnings_list,
            'Stock Total': total_stock_list,
            'Quiebres': stockout_list,
            'Órdenes': orders_list
        })

        st.line_chart(df_final.set_index('Día')[['Ventas Diarias', 'Ganancias Diarias', 'Stock Total']])
        st.bar_chart(df_final.set_index('Día')['Quiebres'])

        # Gráfico de ganancias
        st.subheader("Ganancias Diarias")
        st.line_chart(df_final.set_index('Día')['Ganancias Diarias'])

        # Estadísticas por producto
        st.subheader("Estadísticas por Producto")
        product_stats = []
        for pid, state in product_states.items():
            product_stats.append({
                'Producto': state['name'],
                'Categoría': state['category'],
                'Ventas Totales': state['total_sales'],
                'Stock Final': state['stock'],
                'Días con Quiebre': state['stockout_days'],
                'Órdenes Pendientes': len(state['pending_orders'])
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
