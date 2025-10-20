"""
Módulo para gestionar inscripciones a actividades del parque EcoHarmony Park.

User Story: Inscribirme a actividad
Como visitante QUIERO inscribirme a una actividad PARA reservar mi lugar en la misma.

NOTA: Este módulo debe implementarse siguiendo TDD (Test-Driven Development)
      - Primero escribir tests unitarios en tests/test_inscripciones.py
      - Luego implementar el código mínimo para hacer pasar los tests
      - Refactorizar según sea necesario
"""

from typing import Dict, Any
from sqlalchemy.orm import Session


# TODO: Implementar siguiendo TDD
# 1. Crear tests/test_inscripciones.py
# 2. Escribir tests que fallen (Red)
# 3. Implementar código mínimo (Green)
# 4. Refactorizar (Refactor)


def inscribirse_actividad(payload: Dict[str, Any], session: Session) -> Dict[str, Any]:
    """
    Procesa la inscripción a una actividad del parque.
    
    Args:
        payload: Diccionario con los datos de la inscripción
        session: Sesión de SQLAlchemy para operaciones de DB
    
    Returns:
        Dict con resultado de la operación (exito, mensaje, id_inscripcion)
    
    TODO: Implementar siguiendo TDD
    """
    pass