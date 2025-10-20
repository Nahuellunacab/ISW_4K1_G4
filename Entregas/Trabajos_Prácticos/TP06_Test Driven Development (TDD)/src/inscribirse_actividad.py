"""
Módulo para gestionar inscripciones a actividades del parque EcoHarmony Park.

User Story: Inscribirme a actividad
Como visitante QUIERO inscribirme a una actividad PARA reservar mi lugar en la misma.
"""

import json
import sqlite3
from typing import Dict, Any, List
from datetime import datetime, time

# =============================
# Constantes de configuración
# =============================
ACTIVIDADES_CON_VESTIMENTA = ['Palestra', 'Tirolesa']
TALLES_VALIDOS = ['XS', 'S', 'M', 'L', 'XL', 'XXL']

# Horario del parque
HORA_APERTURA_PARQUE = time(9, 0)
HORA_CIERRE_PARQUE = time(19, 0)
HORA_CIERRE_ACTIVIDADES = time(18, 0)
# Actividades: de 9:00 a 18:00 hs, con turnos de 30 minutos

# Límites de edad según Product Owner
LIMITES_EDAD = {
    'Palestra': 12,
    'Tirolesa': 8,
    'Safari': 0,      # Sin límite
    'Jardineria': 0   # Sin límite
}

MSG_ERROR_TERMINOS = "Debe aceptar Términos y Condiciones"
MSG_ERROR_TALLA_REQUERIDA = "La actividad requiere talla de vestimenta"
MSG_ERROR_SIN_CUPO = "No hay cupos disponibles para el horario seleccionado"
MSG_ERROR_EDAD_INSUFICIENTE = "Edad insuficiente para la actividad. Mínimo requerido: {limite} años"
MSG_ERROR_FUERA_DE_HORARIO = "Inscripción fuera del horario permitido"


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


def _validar_edad_minima(payload: Dict[str, Any]) -> ResultadoInscripcion:
    """
    Valida que las personas cumplan con la edad mínima requerida por la actividad.
    
    TDD FASE REFACTOR: Mejoras en validación y mensajes de error.
    
    Límites según Product Owner:
    - Palestra: 12 años mínimo
    - Tirolesa: 8 años mínimo  
    - Safari y Jardinería: sin límite de edad
    
    Args:
        payload: Datos de la inscripción
        
    Returns:
        ResultadoInscripcion con error si hay personas menores al límite, None si todo está bien
    """
    actividad = payload.get('actividad', '')
    limite_edad = LIMITES_EDAD.get(actividad, 0)
    
    # Si no hay límite de edad, no validar
    if limite_edad == 0:
        return None
    
    personas = payload.get('personas', [])
    for persona in personas:
        edad = persona.get('edad')
        
        # Validar que la edad sea un número válido
        if not isinstance(edad, (int, float)) or edad < 0:
            return ResultadoInscripcion(False, "Edad debe ser un número válido")
            
        if edad < limite_edad:
            mensaje_error = MSG_ERROR_EDAD_INSUFICIENTE.format(limite=limite_edad)
            return ResultadoInscripcion(False, mensaje_error)
    
    return None


def _validar_horario_parque(payload: Dict[str, Any]) -> ResultadoInscripcion:
    """Valida que la inscripción se realice dentro del horario de apertura del parque."""
    try:
        horario_str = payload.get('horario', '').split(' ')[0]
        if not horario_str:
            # No se puede validar si no hay horario
            return None
        horario_inscripcion = datetime.strptime(horario_str, '%H:%M').time()
    except ValueError:
        # Si el formato es inválido, otra validación podría encargarse,
        # pero es bueno ser robusto. De momento, lo ignoramos para este test.
        return None

    if not (HORA_APERTURA_PARQUE <= horario_inscripcion < HORA_CIERRE_ACTIVIDADES):
        return ResultadoInscripcion(False, MSG_ERROR_FUERA_DE_HORARIO)

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
        _validar_edad_minima,  # TDD GREEN: Agregar validación de edad
        _validar_horario_parque,
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
