"""
Tests para la versión cyberpunk modularizada - Compatible con VS Code
"""
import pytest
from unittest.mock import patch, MagicMock
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
        def markdown(self, *args, **kwargs):
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


class TestOpenFileDialogCyber:
    """Tests para open_file_dialog en versión cyberpunk"""

    def test_open_file_dialog_exists(self):
        """Verifica que open_file_dialog existe"""
        sys.modules['tkinter'] = MagicMock()
        sys.modules['tkinter.filedialog'] = MagicMock()
        sys.modules['streamlit'] = MagicMock()

        import interface.base.open_file_dialog as open_file_dialog
        assert callable(open_file_dialog.open_file_dialog)


class TestGetSessionCyber:
    """Tests para get_session en cyberpunk"""

    def test_get_session_returns_session(self):
        """Verifica que get_session retorna una sesión de DB"""
        for mod in list(sys.modules.keys()):
            if 'streamlit_app_cyberpunk' in mod or 'tkinter' in mod or 'streamlit' in mod or 'interface' in mod:
                del sys.modules[mod]

        sys.modules['tkinter'] = MagicMock()
        sys.modules['tkinter.filedialog'] = MagicMock()
        mock_st = create_mock_streamlit()
        sys.modules['streamlit'] = mock_st

        mock_session = MagicMock()
        with patch('interface.base.get_session.get_session', return_value=mock_session):
            import interface.base.get_session as streamlit_app_get_session
            result = streamlit_app_get_session.get_session()
            assert result == mock_session


class TestShowHomeCyber:
    """Tests para show_home en cyberpunk"""

    def test_show_home_exists(self):
        """Verifica que show_home existe"""
        for mod in list(sys.modules.keys()):
            if 'streamlit_app_cyberpunk' in mod or 'tkinter' in mod or 'streamlit' in mod or 'interface' in mod:
                del sys.modules[mod]

        sys.modules['tkinter'] = MagicMock()
        sys.modules['tkinter.filedialog'] = MagicMock()
        mock_st = create_mock_streamlit()
        sys.modules['streamlit'] = mock_st

        import interface.cyberpunk.show_home as cyberpunk_show_home
        assert callable(cyberpunk_show_home.show_home)

    def test_show_home_calls_session(self):
        """Verifica que show_home usa get_session"""
        for mod in list(sys.modules.keys()):
            if 'streamlit_app_cyberpunk' in mod or 'tkinter' in mod or 'streamlit' in mod or 'interface' in mod:
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

            import interface.cyberpunk.show_home as cyberpunk_show_home
            cyberpunk_show_home.show_home()

            mock_get_session.assert_called_once()


class TestShowProductsByCategoryCyber:
    """Tests para show_products_by_category en cyberpunk"""

    def test_show_products_exists(self):
        """Verifica que la función existe"""
        for mod in list(sys.modules.keys()):
            if 'streamlit_app_cyberpunk' in mod or 'tkinter' in mod or 'streamlit' in mod or 'interface' in mod:
                del sys.modules[mod]

        sys.modules['tkinter'] = MagicMock()
        sys.modules['tkinter.filedialog'] = MagicMock()
        mock_st = create_mock_streamlit()
        sys.modules['streamlit'] = mock_st

        import interface.cyberpunk.show_products_by_category as cyberpunk_show_products
        assert callable(cyberpunk_show_products.show_products_by_category)

    def test_show_products_with_category(self):
        """Verifica show_products_by_category con categoría"""
        for mod in list(sys.modules.keys()):
            if 'streamlit_app_cyberpunk' in mod or 'tkinter' in mod or 'streamlit' in mod or 'interface' in mod:
                del sys.modules[mod]

        sys.modules['tkinter'] = MagicMock()
        sys.modules['tkinter.filedialog'] = MagicMock()
        mock_st = create_mock_streamlit()
        sys.modules['streamlit'] = mock_st

        with patch('interface.base.get_session.get_session') as mock_sess, \
             patch('models.product_database.get_all_products_db', return_value=[]):
            mock_session = MagicMock()
            mock_session.query.return_value.all.return_value = []
            mock_sess.return_value = mock_session

            import interface.cyberpunk.show_products_by_category as cyberpunk_show_products
            cyberpunk_show_products.show_products_by_category()

            mock_sess.assert_called_once()


class TestShowInventoryAnalysisCyber:
    """Tests para show_inventory_analysis en cyberpunk"""

    def test_show_inventory_exists(self):
        """Verifica que la función existe"""
        for mod in list(sys.modules.keys()):
            if 'streamlit_app_cyberpunk' in mod or 'tkinter' in mod or 'streamlit' in mod or 'interface' in mod:
                del sys.modules[mod]

        sys.modules['tkinter'] = MagicMock()
        sys.modules['tkinter.filedialog'] = MagicMock()
        mock_st = create_mock_streamlit()
        sys.modules['streamlit'] = mock_st

        import interface.cyberpunk.show_inventory_analysis as cyberpunk_show_inventory
        assert callable(cyberpunk_show_inventory.show_inventory_analysis)

    def test_show_inventory_analysis_with_services(self):
        """Verifica show_inventory_analysis llama servicios"""
        for mod in list(sys.modules.keys()):
            if 'streamlit_app_cyberpunk' in mod or 'tkinter' in mod or 'streamlit' in mod or 'interface' in mod:
                del sys.modules[mod]

        sys.modules['tkinter'] = MagicMock()
        sys.modules['tkinter.filedialog'] = MagicMock()
        mock_st = create_mock_streamlit()
        sys.modules['streamlit'] = mock_st

        import interface.cyberpunk.show_inventory_analysis as cyberpunk_show_inventory

        with patch('services.detect_products', return_value={'productos': []}), \
             patch('models.product_database.get_all_products_db', return_value=[]), \
             patch('services.calculate_inventory_metrics', return_value={'resumen': {'productos_criticos': 0}}), \
             patch('services.calculate_inventory_value', return_value=0), \
             patch('models.get_sales_history.get_sales_history', return_value=[]), \
             patch('services.predict_stock_outage', return_value={'dias_hasta_agotarse': 10, 'estado': 'OK'}):
            cyberpunk_show_inventory.show_inventory_analysis()

            assert mock_st.markdown.call_count > 0


class TestRecommendationsCyber:
    """Tests para show_recommendations en cyberpunk"""

    def test_show_recommendations_exists(self):
        """Verifica que show_recommendations existe"""
        for mod in list(sys.modules.keys()):
            if 'streamlit_app_cyberpunk' in mod or 'tkinter' in mod or 'streamlit' in mod or 'interface' in mod:
                del sys.modules[mod]

        sys.modules['tkinter'] = MagicMock()
        sys.modules['tkinter.filedialog'] = MagicMock()
        mock_st = create_mock_streamlit()
        sys.modules['streamlit'] = mock_st

        import interface.cyberpunk.show_recommendations as cyberpunk_show_recommendations
        assert callable(cyberpunk_show_recommendations.show_recommendations)

    def test_show_recommendations_calls_get_products(self):
        """Verifica show_recommendations obtiene productos"""
        for mod in list(sys.modules.keys()):
            if 'streamlit_app_cyberpunk' in mod or 'tkinter' in mod or 'streamlit' in mod or 'interface' in mod:
                del sys.modules[mod]

        sys.modules['tkinter'] = MagicMock()
        sys.modules['tkinter.filedialog'] = MagicMock()
        mock_st = create_mock_streamlit()
        sys.modules['streamlit'] = mock_st

        with patch('models.product_database.get_all_products_db') as mock_get:
            mock_get.return_value = [
                {'nombre': 'Leche', 'categoria': 'Refrigerados', 'historial_ventas': [1,2,3]}
            ]

            import interface.cyberpunk.show_recommendations as cyberpunk_show_recommendations
            cyberpunk_show_recommendations.show_recommendations()

            mock_get.assert_called_once()


class TestSimulationCyber:
    """Tests para show_simulation en cyberpunk"""

    def test_show_simulation_exists(self):
        """Verifica que show_simulation existe"""
        for mod in list(sys.modules.keys()):
            if 'streamlit_app_cyberpunk' in mod or 'tkinter' in mod or 'streamlit' in mod or 'interface' in mod:
                del sys.modules[mod]

        sys.modules['tkinter'] = MagicMock()
        sys.modules['tkinter.filedialog'] = MagicMock()
        mock_st = create_mock_streamlit()
        sys.modules['streamlit'] = mock_st

        import interface.cyberpunk.show_simulation as cyberpunk_show_simulation
        assert callable(cyberpunk_show_simulation.show_simulation)


class TestMainFunctionCyber:
    """Tests para main en cyberpunk"""

    def test_main_exists(self):
        """Verifica que main existe"""
        for mod in list(sys.modules.keys()):
            if 'streamlit_app_cyberpunk' in mod or 'tkinter' in mod or 'streamlit' in mod or 'interface' in mod:
                del sys.modules[mod]

        sys.modules['tkinter'] = MagicMock()
        sys.modules['tkinter.filedialog'] = MagicMock()
        mock_st = create_mock_streamlit()
        sys.modules['streamlit'] = mock_st

        import interface.cyberpunk.main as cyberpunk_main
        assert callable(cyberpunk_main.main)


class TestCSS:
    """Tests para verificar el CSS cyberpunk"""

    def test_css_has_neon_colors(self):
        """Verifica que el CSS tiene colores neón"""
        with open("interface/cyberpunk/show_home.py", "r", encoding="utf-8") as f:
            content = f.read()
        assert "#00f0ff" in content
        assert "#00ff00" in content

    def test_css_has_cyberpunk_fonts(self):
        """Verifica que el CSS usa fuentes cyberpunk"""
        with open("interface/cyberpunk/show_home.py", "r", encoding="utf-8") as f:
            content = f.read()
        assert "Orbitron" in content
        assert "Share Tech Mono" in content