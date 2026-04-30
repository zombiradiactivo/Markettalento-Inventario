import streamlit as st
import json
from interface.base.open_file_dialog import open_file_dialog
from interface.base.show_home import show_home
from interface.base.show_inventory_analysis import show_inventory_analysis
from interface.base.show_manage_products import show_manage_products
from interface.base.show_products_by_category import show_products_by_category
from interface.base.show_recommendations import show_recommendations
from interface.base.show_simulation import show_simulation
from models import database as db
import os
import tkinter as tk
from tkinter import filedialog

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

