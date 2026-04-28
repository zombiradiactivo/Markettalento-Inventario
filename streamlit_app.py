"""
Sistema de Inventario Inteligente - Streamlit App (SQLAlchemy puro)
"""
import streamlit as st
import json
from models.database import SessionLocal, Refrigerados, Conservas, Bebidas, Panaderia, Despensa, CATEGORY_MODELS
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
    return SessionLocal()


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
        menu_option = st.selectbox(
            "Selecciona una opcion",
            ["Inicio", "Ver Productos por Categoría", "Gestionar Productos", "Analizar Inventario", "Recomendaciones"]
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


if __name__ == "__main__":
    main()
