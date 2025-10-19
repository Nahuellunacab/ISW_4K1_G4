"""
Módulo para gestionar inscripciones a actividades del parque EcoHarmony Park.

User Story: Inscribirme a actividad
Como visitante QUIERO inscribirme a una actividad PARA reservar mi lugar en la misma.
"""

import json
import sqlite3
from typing import Dict, Any, List

# =============================
# Constantes de configuración
# =============================
ACTIVIDADES_CON_VESTIMENTA = ['Palestra', 'Tirolesa']
TALLES_VALIDOS = ['XS', 'S', 'M', 'L', 'XL', 'XXL']

MSG_ERROR_TERMINOS = "Debe aceptar Términos y Condiciones"
MSG_ERROR_TALLA_REQUERIDA = "La actividad requiere talla de vestimenta"
MSG_ERROR_SIN_CUPO = "No hay cupos disponibles para el horario seleccionado"


# =============================
# Clase Resultado
# =============================
class ResultadoInscripcion:
    """Clase para encapsular el resultado de una inscripción."""

    def __init__(self, exito: bool, mensaje: str, id_inscripcion: str = None):
        self.exito = exito
        self.mensaje = mensaje
        self.id_inscripcion = id_inscripcion

    def to_json(self) -> str:
        """Convierte el resultado a formato JSON."""
        return json.dumps({
            "exito": self.exito,
            "mensaje": self.mensaje,
            "idInscripcion": self.id_inscripcion
        })


# =============================
# Repositorio con SQLite3
# =============================
class RepositorioActividadesSQLite:
    """Capa de acceso a datos para actividades, horarios e inscripciones."""

    def __init__(self, db_path="actividades.db"):
        self.db_path = db_path
        self._crear_tablas()
        self._precargar_datos_iniciales()

    def _crear_tablas(self):
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.executescript("""
                CREATE TABLE IF NOT EXISTS actividades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    requiere_vestimenta INTEGER NOT NULL DEFAULT 0
                );

                CREATE TABLE IF NOT EXISTS horarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    actividad_id INTEGER NOT NULL,
                    hora TEXT NOT NULL,
                    cupos_disponibles INTEGER NOT NULL,
                    FOREIGN KEY (actividad_id) REFERENCES actividades(id)
                );

                CREATE TABLE IF NOT EXISTS inscripciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    actividad_id INTEGER NOT NULL,
                    horario_id INTEGER NOT NULL,
                    nombre_persona TEXT NOT NULL,
                    talla_vestimenta TEXT,
                    edad INTEGER,
                    dni TEXT,
                    FOREIGN KEY (actividad_id) REFERENCES actividades(id),
                    FOREIGN KEY (horario_id) REFERENCES horarios(id)
                );
            """)
            conn.commit()

    def _precargar_datos_iniciales(self):
        """Carga los mismos datos hardcodeados del sistema original."""
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()

            # Actividades base
            cur.executemany(
                "INSERT OR IGNORE INTO actividades (nombre, requiere_vestimenta) VALUES (?, ?)",
                [
                    ('Tirolesa', 1),
                    ('Palestra', 1),
                    ('Safari', 0),
                    ('Jardineria', 0)
                ]
            )

            # Horarios y cupos
            cur.executemany(
                """
                INSERT OR IGNORE INTO horarios (actividad_id, hora, cupos_disponibles)
                VALUES (
                    (SELECT id FROM actividades WHERE nombre = ?),
                    ?, ?
                )
                """,
                [
                    ('Tirolesa', '15:00 GMT-3', 0),
                    ('Tirolesa', '10:00 GMT-3', 5),
                    ('Palestra', '09:30 GMT-3', 2),
                    ('Safari', '14:00 GMT-3', 10)
                ]
            )
            conn.commit()

    # ========================================================
    # Operaciones de consulta y actualización de cupos
    # ========================================================
    def obtener_cupos(self, actividad: str, horario: str) -> int:
        query = """
        SELECT cupos_disponibles
        FROM horarios
        JOIN actividades ON horarios.actividad_id = actividades.id
        WHERE actividades.nombre = ? AND horarios.hora = ?
        """
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(query, (actividad, horario))
            row = cur.fetchone()
            return row[0] if row else 0

    def hay_cupo(self, actividad: str, horario: str, cantidad: int) -> bool:
        cupos = self.obtener_cupos(actividad, horario)
        return cupos >= cantidad

    def descontar_cupo(self, actividad: str, horario: str, cantidad: int):
        query = """
        UPDATE horarios
        SET cupos_disponibles = cupos_disponibles - ?
        WHERE id = (
            SELECT h.id
            FROM horarios h
            JOIN actividades a ON a.id = h.actividad_id
            WHERE a.nombre = ? AND h.hora = ?
        )
        """
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(query, (cantidad, actividad, horario))
            conn.commit()

    def agregar_inscripcion(self, actividad: str, horario: str, persona: Dict[str, Any]):
        query = """
        INSERT INTO inscripciones (actividad_id, horario_id, nombre_persona, talla_vestimenta, edad, dni)
        VALUES (
            (SELECT id FROM actividades WHERE nombre = ?),
            (SELECT h.id FROM horarios h JOIN actividades a ON a.id = h.actividad_id WHERE a.nombre = ? AND h.hora = ?),
            ?, ?, ?, ?
        )
        """
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(query, (
                actividad,
                actividad,
                horario,
                persona["nombre"],
                persona.get("tallaVestimenta"),
                persona.get("edad"),
                persona.get("DNI")
            ))
            conn.commit()


# Instancia global del repositorio (simula la conexión al "sistema")
repositorio = RepositorioActividadesSQLite()


# =============================
# Validaciones
# =============================
def _validar_terminos_condiciones(payload: Dict[str, Any]) -> ResultadoInscripcion:
    if not payload.get('aceptoTerminosYCondiciones', False):
        return ResultadoInscripcion(False, MSG_ERROR_TERMINOS)
    return None


def _validar_talla_vestimenta(payload: Dict[str, Any]) -> ResultadoInscripcion:
    actividad = payload.get('actividad', '')

    if actividad not in ACTIVIDADES_CON_VESTIMENTA:
        return None

    personas = payload.get('personas', [])
    for persona in personas:
        talla = persona.get('tallaVestimenta')
        if not talla:
            return ResultadoInscripcion(False, MSG_ERROR_TALLA_REQUERIDA)
    return None


def _validar_cupo_disponible(payload: Dict[str, Any]) -> ResultadoInscripcion:
    actividad = payload.get('actividad')
    horario = payload.get('horario')
    cantidad = payload.get('cantidadPersonas', 1)

    if not repositorio.hay_cupo(actividad, horario, cantidad):
        return ResultadoInscripcion(False, MSG_ERROR_SIN_CUPO)
    return None


# =============================
# Lógica principal
# =============================
def inscribirse_a_actividad(payload: Dict[str, Any]) -> str:
    """
    Procesa la inscripción a una actividad del parque.
    """
    validaciones = [
        _validar_terminos_condiciones,
        _validar_talla_vestimenta,
        _validar_cupo_disponible
    ]

    for validacion in validaciones:
        error = validacion(payload)
        if error:
            return error.to_json()

    # Registrar inscripción y descontar cupos
    for persona in payload.get("personas", []):
        repositorio.agregar_inscripcion(payload["actividad"], payload["horario"], persona)
    repositorio.descontar_cupo(payload["actividad"], payload["horario"], payload["cantidadPersonas"])

    resultado = ResultadoInscripcion(
        exito=True,
        mensaje="Inscripción exitosa",
        id_inscripcion="INS-001"
    )
    return resultado.to_json()
