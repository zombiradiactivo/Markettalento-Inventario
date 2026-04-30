from models import database as db
SessionLocal = db.SessionLocal

def get_session():
    """Obtiene una nueva sesion de base de datos"""
    return db.SessionLocal()

