"""
Configuracion de la aplicacion
"""


class Config:
    """Configuracion base"""
    DEBUG = False
    HOST = '0.0.0.0'
    PORT = 5000
    SECRET_KEY = 'inventario-secreto-2024'


class DevelopmentConfig(Config):
    """Configuracion para desarrollo"""
    DEBUG = True
    PORT = 5002


class ProductionConfig(Config):
    """Configuracion para produccion"""
    DEBUG = False
    PORT = 5000


# Mapeo de entornos
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
