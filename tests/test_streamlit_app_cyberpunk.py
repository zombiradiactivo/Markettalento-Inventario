"""
Tests para streamlit_app_cyberpunk.py - Corregido para Python 3.10+
"""
import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Configuración de mocks globales
def setup_module_mocks():
    """Configura mocks de tkinter y streamlit antes de importar"""
    sys.modules['tkinter'] = MagicMock()
    sys.modules['tkinter.filedialog'] = MagicMock()
    
    mock_st = MagicMock()
    mock_state = MagicMock()
    mock_state.db_initialized = True
    mock_state.current_db = 'inventario.db'
    mock_st.session_state = mock_state
    mock_st.columns.return_value = [MagicMock() for _ in range(5)]
    mock_st.tabs.return_value = [MagicMock() for _ in range(3)]
    mock_st.selectbox.return_value = "Inicio"
    mock_st.button.return_value = False
    mock_st.form_submit_button.return_value = False
    mock_st.slider.return_value = 30
    mock_st.select_slider.return_value = "Normal"
    sys.modules['streamlit'] = mock_st
    return mock_st


class TestOpenFileDialogCyber:
    """Tests para open_file_dialog en versión cyberpunk"""

    def test_open_file_dialog_exists(self):
        """Verifica que la función existe"""
        setup_module_mocks()
        from streamlit_app_cyberpunk import open_file_dialog
        assert callable(open_file_dialog)

    def test_open_file_dialog_returns_path(self):
        """Verifica que retorna una ruta válida"""
        setup_module_mocks()
        with patch('tkinter.Tk') as mock_tk, \
             patch('tkinter.filedialog.askopenfilename', return_value="/path/to/db.db"):
            mock_root = MagicMock()
            mock_tk.return_value = mock_root
            from streamlit_app_cyberpunk import open_file_dialog
            result = open_file_dialog()
            assert result == "/path/to/db.db"
            mock_root.withdraw.assert_called_once()


class TestGetSessionCyber:
    """Tests para get_session en cyberpunk"""

    def test_get_session_exists(self):
        """Verifica que la función existe"""
        setup_module_mocks()
        from streamlit_app_cyberpunk import get_session
        assert callable(get_session)

    def test_get_session_returns_session(self):
        """Verifica que retorna una sesión"""
        mock_st = setup_module_mocks()
        mock_session = MagicMock()
        with patch('streamlit_app_cyberpunk.db.SessionLocal', return_value=mock_session):
            from streamlit_app_cyberpunk import get_session
            result = get_session()
            assert result == mock_session


class TestShowHomeCyber:
    """Tests para show_home en cyberpunk"""

    def test_show_home_exists(self):
        """Verifica que la función existe"""
        setup_module_mocks()
        from streamlit_app_cyberpunk import show_home
        assert callable(show_home)


class TestShowProductsByCategoryCyber:
    """Tests para show_products_by_category en cyberpunk"""

    def test_show_products_exists(self):
        """Verifica que la función existe"""
        setup_module_mocks()
        from streamlit_app_cyberpunk import show_products_by_category
        assert callable(show_products_by_category)


class TestShowInventoryAnalysisCyber:
    """Tests para show_inventory_analysis en cyberpunk"""

    def test_show_inventory_exists(self):
        """Verifica que la función existe"""
        setup_module_mocks()
        from streamlit_app_cyberpunk import show_inventory_analysis
        assert callable(show_inventory_analysis)

    def test_show_inventory_calls_services(self):
        """Verifica que usa servicios de análisis"""
        mock_st = setup_module_mocks()
        mock_st.button.return_value = True
        
        mock_detection = {"productos": [{"nombre": "Leche", "cantidad": 10}]}
        mock_products_db = [{"nombre": "Leche", "categoria": "Refrigerados", "precio": 2.5}]
        
        with patch('streamlit_app_cyberpunk.detect_products', return_value=mock_detection), \
             patch('streamlit_app_cyberpunk.get_all_products_db', return_value=mock_products_db), \
             patch('streamlit_app_cyberpunk.get_sales_history', return_value=[3,4,5]), \
             patch('streamlit_app_cyberpunk.predict_stock_outage', return_value={"estado": "Normal", "dias_hasta_agotarse": 10}), \
             patch('streamlit_app_cyberpunk.calculate_inventory_metrics', return_value={"resumen": {"productos_criticos": 0}}), \
             patch('streamlit_app_cyberpunk.calculate_inventory_value', return_value=100):
            from streamlit_app_cyberpunk import show_inventory_analysis
            show_inventory_analysis()
            from streamlit_app_cyberpunk import detect_products
            detect_products.assert_called_once()


class TestMainFunctionCyber:
    """Tests para main en cyberpunk"""

    def test_main_exists(self):
        """Verifica que main existe"""
        setup_module_mocks()
        from streamlit_app_cyberpunk import main
        assert callable(main)


class TestCSS:
    """Tests para verificar el CSS cyberpunk"""

    def test_css_has_neon_colors(self):
        """Verifica que el CSS tiene colores neón"""
        with open("streamlit_app_cyberpunk.py", "r", encoding="utf-8") as f:
            content = f.read()
        assert "#00f0ff" in content
        assert "#ff00ff" in content

    def test_css_has_cyberpunk_fonts(self):
        """Verifica que el CSS usa fuentes cyberpunk"""
        with open("streamlit_app_cyberpunk.py", "r", encoding="utf-8") as f:
            content = f.read()
        assert "Orbitron" in content
        assert "Share Tech Mono" in content
