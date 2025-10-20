"""
Configuración de pytest y fixtures compartidas.

Este archivo contiene fixtures que pueden ser utilizadas en todos los tests.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base


@pytest.fixture
def db_session():
    """
    Fixture que proporciona una sesión de base de datos en memoria para tests.
    
    TODO: Implementar cuando sea necesario para los tests
    """
    # Crear base de datos en memoria SQLite
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def sample_payload():
    """
    Fixture con un payload de ejemplo válido.
    
    TODO: Ajustar según los tests que se escriban
    """
    return {
        "actividad": "Safari",
        "horario": "10:00",
        "cantidadPersonas": 1,
        "aceptoTerminosYCondiciones": True,
        "personas": [
            {
                "nombre": "Juan Pérez",
                "dni": "12345678",
                "edad": 25
            }
        ]
    }
