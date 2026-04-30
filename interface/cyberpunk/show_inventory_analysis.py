import streamlit as st

from models.product_database import get_all_products_db
from models.get_sales_history import get_sales_history
from services import detect_products, calculate_inventory_metrics, calculate_inventory_value, predict_stock_outage


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

