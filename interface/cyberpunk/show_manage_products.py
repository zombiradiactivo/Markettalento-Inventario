import streamlit as st
import json

from models.product_database import get_all_products_db, get_product_by_name, add_product, delete_product, update_product


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

