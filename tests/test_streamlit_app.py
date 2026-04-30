"""
Tests para streamlit_app.py - Compatible con VS Code
"""
import pytest
from unittest.mock import patch, MagicMock, call
import sys
import os


def create_mock_streamlit():
    """Crea un mock de streamlit con session_state"""
    mock_st = MagicMock()
    mock_state = MagicMock()
    mock_state.current_db = 'test.db'
    mock_state.db_initialized = True
    mock_st.session_state = mock_state

    class MockColumnContainer:
        def __init__(self):
            pass
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
        def metric(self, *args, **kwargs):
            pass

    def mock_columns(n):
        if isinstance(n, list):
            return [MockColumnContainer() for _ in n]
        return [MockColumnContainer() for _ in range(n)]

    def mock_tabs(names):
        return [MagicMock() for _ in range(len(names))]

    def mock_selectbox(label, options, **kwargs):
        return options[0] if options else None

    def mock_slider(label, min_value=None, max_value=None, value=None, **kwargs):
        return value if value is not None else min_value

    def mock_select_slider(label, options, value=None, **kwargs):
        return value if value else options[0] if options else None

    def mock_button(label, **kwargs):
        return False

    def mock_form(key, **kwargs):
        return MagicMock()

    def mock_form_submit_button(label):
        return False

    mock_st.columns = mock_columns
    mock_st.tabs = mock_tabs
    mock_st.selectbox = mock_selectbox
    mock_st.slider = mock_slider
    mock_st.select_slider = mock_select_slider
    mock_st.button = mock_button
    mock_st.form = mock_form
    mock_st.form_submit_button = mock_form_submit_button
    mock_st.spinner = MagicMock()
    mock_st.success = MagicMock()
    mock_st.error = MagicMock()
    mock_st.info = MagicMock()
    mock_st.dataframe = MagicMock()
    mock_st.markdown = MagicMock()
    mock_st.header = MagicMock()
    mock_st.subheader = MagicMock()

    return mock_st


class TestOpenFileDialog:
    """Tests para open_file_dialog"""

    def test_open_file_dialog_exists(self):
        """Verifica que open_file_dialog existe"""
        sys.modules['tkinter'] = MagicMock()
        sys.modules['tkinter.filedialog'] = MagicMock()
        sys.modules['streamlit'] = MagicMock()

        import interface.base.open_file_dialog as open_file_dialog
        assert callable(open_file_dialog.open_file_dialog)


class TestGetSession:
    """Tests para get_session"""

    def test_get_session_returns_session(self):
        """Verifica que get_session retorna una sesión de DB"""
        sys.modules['tkinter'] = MagicMock()
        sys.modules['tkinter.filedialog'] = MagicMock()
        mock_st = create_mock_streamlit()
        sys.modules['streamlit'] = mock_st
        
        mock_session = MagicMock()
        with patch('interface.base.get_session.db.SessionLocal', return_value=mock_session):
            import interface.base.get_session as streamlit_app_get_session
            result = streamlit_app_get_session.get_session()
            assert result == mock_session


class TestShowHome:
    """Tests para show_home"""

    def test_show_home_exists(self):
        """Verifica que show_home existe"""
        sys.modules['tkinter'] = MagicMock()
        sys.modules['tkinter.filedialog'] = MagicMock()
        sys.modules['streamlit'] = MagicMock()
        
        import interface.base.show_home as streamlit_app_show_home
        assert callable(streamlit_app_show_home.show_home)

    def test_show_home_calls_session(self):
        """Verifica que show_home usa get_session"""
        for mod in list(sys.modules.keys()):
            if 'streamlit_app' in mod or 'tkinter' in mod or 'streamlit' in mod or 'interface.base' in mod:
                del sys.modules[mod]

        sys.modules['tkinter'] = MagicMock()
        sys.modules['tkinter.filedialog'] = MagicMock()
        mock_st = create_mock_streamlit()
        sys.modules['streamlit'] = mock_st

        with patch('interface.base.get_session.get_session') as mock_get_session:
            mock_session = MagicMock()
            mock_query = MagicMock()
            mock_query.count.return_value = 5
            mock_session.query.return_value = mock_query
            mock_get_session.return_value = mock_session

            import interface.base.show_home as streamlit_app_show_home
            streamlit_app_show_home.show_home()

            mock_get_session.assert_called_once()


class TestShowProductsByCategory:
    """Tests para show_products_by_category"""

    def test_show_products_exists(self):
        """Verifica que la función existe"""
        sys.modules['tkinter'] = MagicMock()
        sys.modules['tkinter.filedialog'] = MagicMock()
        sys.modules['streamlit'] = MagicMock()
        
        import interface.base.show_products_by_category as streamlit_app_show_products_by_category
        assert callable(streamlit_app_show_products_by_category.show_products_by_category)

    def test_show_products_with_category(self):
        """Verifica show_products_by_category con categoría"""
        for mod in list(sys.modules.keys()):
            if 'streamlit_app' in mod or 'tkinter' in mod or 'streamlit' in mod:
                del sys.modules[mod]
        
        sys.modules['tkinter'] = MagicMock()
        sys.modules['tkinter.filedialog'] = MagicMock()
        mock_st = create_mock_streamlit()
        sys.modules['streamlit'] = mock_st
        
        import interface.base.show_products_by_category as streamlit_app_show_products_by_category
        
        with patch('interface.base.get_session.db.SessionLocal') as mock_sess, \
             patch('interface.base.main.CATEGORY_MODELS', {'Refrigerados': MagicMock()}), \
             patch('models.product_database.get_all_products_db', return_value=[]):
            mock_sess.return_value.query.return_value.all.return_value = []
            
            streamlit_app_show_products_by_category.show_products_by_category()
            
            mock_sess.assert_called_once()

    def test_show_products_with_data(self):
        """Verifica show_products_by_category con productos"""
        for mod in list(sys.modules.keys()):
            if 'streamlit_app' in mod or 'tkinter' in mod or 'streamlit' in mod:
                del sys.modules[mod]
        
        sys.modules['tkinter'] = MagicMock()
        sys.modules['tkinter.filedialog'] = MagicMock()
        mock_st = create_mock_streamlit()
        sys.modules['streamlit'] = mock_st
        
        import interface.base.show_products_by_category as streamlit_app_show_products_by_category
        
        class MockProduct:
            def __init__(self, id, nombre, precio, unidad, stock_minimo, stock_maximo, tiempo_reposicion):
                self.id = id
                self.nombre = nombre
                self.precio = precio
                self.unidad = unidad
                self.stock_minimo = stock_minimo
                self.stock_maximo = stock_maximo
                self.tiempo_reposicion = tiempo_reposicion
                self.categoria = 'Refrigerados'
                self.historial_ventas = [3]*20
            
            def to_dict(self):
                return {
                    'id': self.id, 'nombre': self.nombre, 'precio': self.precio,
                    'unidad': self.unidad, 'stock_minimo': self.stock_minimo,
                    'stock_maximo': self.stock_maximo, 'tiempo_reposicion': self.tiempo_reposicion,
                    'categoria': self.categoria, 'historial_ventas': self.historial_ventas
                }
        
        mock_product = MockProduct(1, 'Leche', 1.50, 'litro', 5, 50, 3)
        
        with patch('interface.base.get_session.db.SessionLocal') as mock_sess, \
             patch('interface.base.main.CATEGORY_MODELS', {'Refrigerados': MagicMock()}), \
             patch('models.product_database.get_all_products_db', return_value=[mock_product.to_dict()]):
            mock_sess.return_value.query.return_value.all.return_value = [mock_product]
            
            streamlit_app_show_products_by_category.show_products_by_category()
            
            mock_sess.assert_called_once()


class TestShowManageProducts:
    """Tests para show_manage_products"""

    def test_show_manage_exists(self):
        """Verifica que la función existe"""
        sys.modules['tkinter'] = MagicMock()
        sys.modules['tkinter.filedialog'] = MagicMock()
        sys.modules['streamlit'] = MagicMock()
        
        import interface.base.show_manage_products as streamlit_app_show_manage_products
        assert callable(streamlit_app_show_manage_products.show_manage_products)


class TestShowInventoryAnalysis:
    """Tests para show_inventory_analysis"""

    def test_show_inventory_exists(self):
        """Verifica que la función existe"""
        sys.modules['tkinter'] = MagicMock()
        sys.modules['tkinter.filedialog'] = MagicMock()
        sys.modules['streamlit'] = MagicMock()
        
        import interface.base.show_inventory_analysis as streamlit_app_show_inventory_analysis
        assert callable(streamlit_app_show_inventory_analysis.show_inventory_analysis)

    def test_show_inventory_analysis_with_services(self):
        """Verifica show_inventory_analysis llama servicios"""
        for mod in list(sys.modules.keys()):
            if 'streamlit_app' in mod or 'tkinter' in mod or 'streamlit' in mod or 'interface.base' in mod:
                del sys.modules[mod]

        sys.modules['tkinter'] = MagicMock()
        sys.modules['tkinter.filedialog'] = MagicMock()
        mock_st = create_mock_streamlit()
        sys.modules['streamlit'] = mock_st

        import interface.base.show_inventory_analysis as streamlit_app_show_inventory_analysis

        with patch('services.detect_products', return_value={'productos': []}), \
             patch('models.product_database.get_all_products_db', return_value=[]), \
             patch('services.calculate_inventory_metrics', return_value={'resumen': {'productos_criticos': 0}}), \
             patch('services.calculate_inventory_value', return_value=0), \
             patch('models.get_sales_history.get_sales_history', return_value=[]), \
             patch('services.predict_stock_outage', return_value={'dias_hasta_agotarse': 10, 'estado': 'OK'}):
            streamlit_app_show_inventory_analysis.show_inventory_analysis()

            assert mock_st.markdown.call_count > 0


class TestRecommendations:
    """Tests para show_recommendations"""

    def test_show_recommendations_exists(self):
        """Verifica que show_recommendations existe"""
        sys.modules['tkinter'] = MagicMock()
        sys.modules['tkinter.filedialog'] = MagicMock()
        sys.modules['streamlit'] = MagicMock()
        
        import interface.base.show_recommendations as  streamlit_app_show_recommendations
        assert callable(streamlit_app_show_recommendations.show_recommendations)

    def test_show_recommendations_calls_get_products(self):
        """Verifica show_recommendations obtiene productos"""
        for mod in list(sys.modules.keys()):
            if 'streamlit_app' in mod or 'tkinter' in mod or 'streamlit' in mod:
                del sys.modules[mod]
        
        sys.modules['tkinter'] = MagicMock()
        sys.modules['tkinter.filedialog'] = MagicMock()
        mock_st = create_mock_streamlit()
        sys.modules['streamlit'] = mock_st
        
        import interface.base.show_recommendations as  streamlit_app_show_recommendations
        
        with patch('interface.base.show_recommendations.get_all_products_db') as mock_get:
            mock_get.return_value = [
                {'nombre': 'Leche', 'categoria': 'Refrigerados', 'historial_ventas': [1,2,3]}
            ]
            
            streamlit_app_show_recommendations.show_recommendations()
            
            mock_get.assert_called_once()


class TestSimulation:
    """Tests para show_simulation"""

    def test_show_simulation_exists(self):
        """Verifica que show_simulation existe"""
        sys.modules['tkinter'] = MagicMock()
        sys.modules['tkinter.filedialog'] = MagicMock()
        sys.modules['streamlit'] = MagicMock()
        
        import interface.base.show_simulation as streamlit_app_show_simulation
        assert callable(streamlit_app_show_simulation.show_simulation)


class TestMainFunction:
    """Tests para main"""

    def test_main_exists(self):
        """Verifica que main existe"""
        sys.modules['tkinter'] = MagicMock()
        sys.modules['tkinter.filedialog'] = MagicMock()
        sys.modules['streamlit'] = MagicMock()
        
        import interface.base.main as streamlit_app_main
        assert callable(streamlit_app_main.main)
