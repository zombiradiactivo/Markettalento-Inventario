import streamlit as st

from models.product_database import get_all_products_db


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

