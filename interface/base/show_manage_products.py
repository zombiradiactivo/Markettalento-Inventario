import streamlit as st
import json

from models.product_database import get_all_products_db, get_product_by_name, add_product, delete_product, update_product


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

