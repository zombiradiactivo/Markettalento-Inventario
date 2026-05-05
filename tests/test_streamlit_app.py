"""
Tests para streamlit_app.py - Corregido para Python 3.10+
"""
import pytest
from unittest.mock import patch, MagicMock, call
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


class TestOpenFileDialog:
    """Tests para open_file_dialog"""

    def test_open_file_dialog_exists(self):
        """Verifica que la función existe"""
        setup_module_mocks()
        from streamlit_app import open_file_dialog
        assert callable(open_file_dialog)

    def test_open_file_dialog_returns_path(self):
        """Verifica que retorna una ruta válida"""
        setup_module_mocks()
        with patch('tkinter.Tk') as mock_tk, \
             patch('tkinter.filedialog.askopenfilename', return_value="/path/to/db.db"):
            mock_root = MagicMock()
            mock_tk.return_value = mock_root
            from streamlit_app import open_file_dialog
            result = open_file_dialog()
            assert result == "/path/to/db.db"
            mock_root.withdraw.assert_called_once()


class TestGetSession:
    """Tests para get_session"""

    def test_get_session_exists(self):
        """Verifica que la función existe"""
        setup_module_mocks()
        from streamlit_app import get_session
        assert callable(get_session)

    def test_get_session_returns_session(self):
        """Verifica que retorna una sesión"""
        mock_st = setup_module_mocks()
        mock_session = MagicMock()
        with patch('streamlit_app.db.SessionLocal', return_value=mock_session):
            from streamlit_app import get_session
            result = get_session()
            assert result == mock_session


class TestShowHome:
    """Tests para show_home"""

    def test_show_home_exists(self):
        """Verifica que la función existe"""
        setup_module_mocks()
        from streamlit_app import show_home
        assert callable(show_home)

    def test_show_home_calls_session(self):
        """Verifica que show_home usa get_session"""
        mock_st = setup_module_mocks()
        mock_session = MagicMock()
        mock_query = MagicMock()
        mock_query.count.return_value = 5
        mock_session.query.return_value = mock_query
        
        with patch('streamlit_app.db.SessionLocal', return_value=mock_session), \
             patch('streamlit_app.Refrigerados'), \
             patch('streamlit_app.Conservas'), \
             patch('streamlit_app.Bebidas'), \
             patch('streamlit_app.Panaderia'), \
             patch('streamlit_app.Despensa'):
            from streamlit_app import show_home
            show_home()
            mock_session.query.assert_called()


class TestShowProductsByCategory:
    """Tests para show_products_by_category"""

    def test_show_products_exists(self):
        """Verifica que la función existe"""
        setup_module_mocks()
        from streamlit_app import show_products_by_category
        assert callable(show_products_by_category)

    def test_show_products_with_category(self):
        """Verifica que usa session y modelos"""
        mock_st = setup_module_mocks()
        mock_session = MagicMock()
        mock_model = MagicMock()
        mock_product = MagicMock()
        mock_product.to_dict.return_value = {"nombre": "Leche"}
        mock_session.query.return_value.all.return_value = [mock_product]
        
        with patch('streamlit_app.db.SessionLocal', return_value=mock_session), \
             patch('streamlit_app.CATEGORY_MODELS', {"Refrigerados": mock_model}), \
             patch('streamlit_app.get_all_products_db', return_value=[]):
            from streamlit_app import show_products_by_category
            show_products_by_category()
            mock_session.query.assert_called_once()


class TestShowManageProducts:
    """Tests para show_manage_products"""

    def test_show_manage_exists(self):
        """Verifica que la función existe"""
        setup_module_mocks()
        from streamlit_app import show_manage_products
        assert callable(show_manage_products)


class TestShowInventoryAnalysis:
    """Tests para show_inventory_analysis"""

    def test_show_inventory_exists(self):
        """Verifica que la función existe"""
        setup_module_mocks()
        from streamlit_app import show_inventory_analysis
        assert callable(show_inventory_analysis)

    def test_show_inventory_calls_services(self):
        """Verifica que usa servicios de análisis"""
        mock_st = setup_module_mocks()
        mock_st.button.return_value = True
        
        mock_detection = {"productos": [{"nombre": "Leche", "cantidad": 10}]}
        mock_products_db = [{"nombre": "Leche", "categoria": "Refrigerados", "precio": 2.5}]
        
        with patch('streamlit_app.detect_products', return_value=mock_detection), \
             patch('streamlit_app.get_all_products_db', return_value=mock_products_db), \
             patch('streamlit_app.get_sales_history', return_value=[3,4,5]), \
             patch('streamlit_app.predict_stock_outage', return_value={"estado": "Normal", "dias_hasta_agotarse": 10}), \
             patch('streamlit_app.calculate_inventory_metrics', return_value={"resumen": {"productos_criticos": 0}}), \
             patch('streamlit_app.calculate_inventory_value', return_value=100):
            from streamlit_app import show_inventory_analysis
            show_inventory_analysis()
            # Verificar que se llamaron los servicios
            from streamlit_app import detect_products
            detect_products.assert_called_once()


class TestShowRecommendations:
    """Tests para show_recommendations"""

    def test_show_recommendations_exists(self):
        """Verifica que la función existe"""
        setup_module_mocks()
        from streamlit_app import show_recommendations
        assert callable(show_recommendations)


class TestMainFunction:
    """Tests para main"""

    def test_main_exists(self):
        """Verifica que main existe"""
        setup_module_mocks()
        from streamlit_app import main
        assert callable(main)

    def test_main_calls_show_home(self):
        """Verifica que main llama a show_home"""
        mock_st = setup_module_mocks()
        mock_st.selectbox.return_value = "Inicio"
        
        with patch('streamlit_app.show_home') as mock_home:
            from streamlit_app import main
            main()
            mock_home.assert_called_once()
