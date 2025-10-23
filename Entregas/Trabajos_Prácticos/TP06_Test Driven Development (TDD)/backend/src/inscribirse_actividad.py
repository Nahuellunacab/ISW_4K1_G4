"""
Módulo para gestionar inscripciones a actividades del parque EcoHarmony Park.

User Story: Inscribirme a actividad
Como visitante QUIERO inscribirme a una actividad PARA reservar mi lugar en la misma.
"""

import json
import os
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
MSG_ERROR_CANTIDAD_INVALIDA = "La cantidad de personas debe ser al menos 1"
MSG_ERROR_EXCEDE_CUPOS = "La cantidad de personas excede los cupos disponibles"
MSG_ERROR_NOMBRE_INVALIDO = "El nombre solo puede contener letras, espacios y guiones"
MSG_ERROR_DNI_INVALIDO = "El DNI debe contener solo números y tener entre 6 y 10 dígitos"
MSG_ERROR_EDAD_CERO = "La edad debe ser mayor a 0"
MSG_ERROR_EDAD_INSUFICIENTE = (
    "Edad insuficiente para la actividad. Mínimo requerido: {limite} años"
)
MSG_ERROR_EDAD_INVALIDA = "Edad debe ser un número válido"
MSG_ERROR_FUERA_DE_HORARIO = "Inscripción fuera del horario permitido"
MSG_ERROR_HORARIO_NO_EXISTE = (
    "El horario seleccionado no existe para la actividad indicada"
)

MSG_ERROR_DNI_CONFLICTO = (
    "El/los DNI(s) {dnis} ya están inscriptos en ese mismo horario. "
    "Una persona no puede inscribirse más de una vez en el mismo horario."
)

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

    def __init__(self, db_path=None):
        """
        Inicializa el repositorio con una ruta de base de datos.
        
        Args:
            db_path: Ruta a la base de datos. Si es None, usa una ubicación
                     centralizada en el directorio raíz del proyecto.
        """
        if db_path is None:
            # Usar ruta absoluta al directorio raíz del proyecto
            project_root = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..')
            )
            db_path = os.path.join(project_root, 'actividades.db')
        
        self.db_path = db_path
        self._inicializar_base_datos()

    def _inicializar_base_datos(self):
        """Inicializa la base de datos creando tablas y datos iniciales."""
        self._crear_tablas()
        self._precargar_datos_iniciales()

    def _crear_tablas(self):
        """Crea las tablas si no existen."""
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
                    cupos_iniciales INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY (actividad_id) REFERENCES actividades(id),
                    UNIQUE(actividad_id, hora)
                );

                CREATE TABLE IF NOT EXISTS inscripciones (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    actividad_id INTEGER NOT NULL,
                    horario_id INTEGER NOT NULL,
                    nombre_persona TEXT NOT NULL,
                    talla_vestimenta TEXT,
                    edad INTEGER,
                    dni TEXT,
                    fecha_inscripcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (actividad_id) REFERENCES actividades(id),
                    FOREIGN KEY (horario_id) REFERENCES horarios(id)
                );
            """)
            conn.commit()

    def _precargar_datos_iniciales(self):
        """
        Carga los datos iniciales del sistema solo si no existen.
        
        Este método solo inserta datos si no están presentes,
        sin resetear ni modificar datos existentes.
        """
    with sqlite3.connect(self.db_path) as conn:
        cur = conn.cursor()

        # Actividades base - Solo insertar si no existen
        actividades = [
            ('Tirolesa', 1),
            ('Palestra', 1),
            ('Safari', 0),
            ('Jardineria', 0)
        ]
        
        for nombre, requiere in actividades:
            cur.execute(
                "INSERT OR IGNORE INTO actividades (nombre, requiere_vestimenta) VALUES (?, ?)",
                (nombre, requiere)
            )

        # Horarios con cupos iniciales - Solo insertar si no existen
        horarios_iniciales = [
            # Tirolesa (actividad_id = 1, cupos_iniciales = 10)
            ('Tirolesa', '09:00 GMT-3', 10),
            ('Tirolesa', '09:30 GMT-3', 10),
            ('Tirolesa', '10:00 GMT-3', 10),
            ('Tirolesa', '10:30 GMT-3', 10),
            ('Tirolesa', '11:00 GMT-3', 10),
            ('Tirolesa', '11:30 GMT-3', 10),
            ('Tirolesa', '12:00 GMT-3', 10),
            ('Tirolesa', '12:30 GMT-3', 10),
            ('Tirolesa', '13:00 GMT-3', 10),
            ('Tirolesa', '13:30 GMT-3', 10),
            ('Tirolesa', '14:00 GMT-3', 10),
            ('Tirolesa', '14:30 GMT-3', 10),
            ('Tirolesa', '15:00 GMT-3', 10),
            ('Tirolesa', '15:30 GMT-3', 10),
            ('Tirolesa', '16:00 GMT-3', 10),
            ('Tirolesa', '16:30 GMT-3', 10),
            ('Tirolesa', '17:00 GMT-3', 10),
            ('Tirolesa', '17:30 GMT-3', 10),

            # Palestra (actividad_id = 2, cupos_iniciales = 12)
            ('Palestra', '09:00 GMT-3', 12),
            ('Palestra', '09:30 GMT-3', 12),
            ('Palestra', '10:00 GMT-3', 12),
            ('Palestra', '10:30 GMT-3', 12),
            ('Palestra', '11:00 GMT-3', 12),
            ('Palestra', '11:30 GMT-3', 12),
            ('Palestra', '12:00 GMT-3', 12),
            ('Palestra', '12:30 GMT-3', 12),
            ('Palestra', '13:00 GMT-3', 12),
            ('Palestra', '13:30 GMT-3', 12),
            ('Palestra', '14:00 GMT-3', 12),
            ('Palestra', '14:30 GMT-3', 12),
            ('Palestra', '15:00 GMT-3', 12),
            ('Palestra', '15:30 GMT-3', 12),
            ('Palestra', '16:00 GMT-3', 12),
            ('Palestra', '16:30 GMT-3', 12),
            ('Palestra', '17:00 GMT-3', 12),
            ('Palestra', '17:30 GMT-3', 12),

            # Safari (actividad_id = 3, cupos_iniciales = 8)
            ('Safari', '09:00 GMT-3', 8),
            ('Safari', '09:30 GMT-3', 8),
            ('Safari', '10:00 GMT-3', 8),
            ('Safari', '10:30 GMT-3', 8),
            ('Safari', '11:00 GMT-3', 8),
            ('Safari', '11:30 GMT-3', 8),
            ('Safari', '12:00 GMT-3', 8),
            ('Safari', '12:30 GMT-3', 8),
            ('Safari', '13:00 GMT-3', 8),
            ('Safari', '13:30 GMT-3', 8),
            ('Safari', '14:00 GMT-3', 8),
            ('Safari', '14:30 GMT-3', 8),
            ('Safari', '15:00 GMT-3', 8),
            ('Safari', '15:30 GMT-3', 8),
            ('Safari', '16:00 GMT-3', 8),
            ('Safari', '16:30 GMT-3', 8),
            ('Safari', '17:00 GMT-3', 8),
            ('Safari', '17:30 GMT-3', 8),

            # Jardinería (actividad_id = 4, cupos_iniciales = 12)
            ('Jardineria', '09:00 GMT-3', 12),
            ('Jardineria', '09:30 GMT-3', 12),
            ('Jardineria', '10:00 GMT-3', 12),
            ('Jardineria', '10:30 GMT-3', 12),
            ('Jardineria', '11:00 GMT-3', 12),
            ('Jardineria', '11:30 GMT-3', 12),
            ('Jardineria', '12:00 GMT-3', 12),
            ('Jardineria', '12:30 GMT-3', 12),
            ('Jardineria', '13:00 GMT-3', 12),
            ('Jardineria', '13:30 GMT-3', 12),
            ('Jardineria', '14:00 GMT-3', 12),
            ('Jardineria', '14:30 GMT-3', 12),
            ('Jardineria', '15:00 GMT-3', 12),
            ('Jardineria', '15:30 GMT-3', 12),
            ('Jardineria', '16:00 GMT-3', 12),
            ('Jardineria', '16:30 GMT-3', 12),
            ('Jardineria', '17:00 GMT-3', 12),
            ('Jardineria', '17:30 GMT-3', 12),
        ]
        
        for actividad_nombre, hora, cupos in horarios_iniciales:
            # Insertar solo si no existe (gracias a UNIQUE constraint)
            cur.execute(
                """
                INSERT OR IGNORE INTO horarios (actividad_id, hora, cupos_disponibles, cupos_iniciales)
                VALUES (
                    (SELECT id FROM actividades WHERE nombre = ?),
                    ?, ?, ?
                )
                """,
                (actividad_nombre, hora, cupos, cupos)
            )
        
        conn.commit()


    # Función para verificar si un horario existe para una actividad
    # -> Test inscribirse horario no disponible
    def horario_existe(self, actividad: str, horario: str) -> bool:
        """Verifica si un horario específico existe para una actividad."""
        query = """
        SELECT 1
        FROM horarios
        JOIN actividades ON horarios.actividad_id = actividades.id
        WHERE actividades.nombre = ? AND horarios.hora = ?
        """
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(query, (actividad, horario))
            return cur.fetchone() is not None

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

    def agregar_inscripcion(
        self, actividad: str, horario: str, persona: Dict[str, Any]
    ) -> int:
        """
        Agrega una inscripción a la base de datos.
        
        Returns:
            ID de la inscripción creada
        """
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
            return cur.lastrowid

    def obtener_todas_actividades(self) -> List[Dict[str, Any]]:
        """
        Obtiene todas las actividades disponibles.

        Returns:
            Lista de actividades con sus propiedades
        """
        query = """
        SELECT nombre, requiere_vestimenta
        FROM actividades
        """
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            return [
                {
                    'nombre': row[0],
                    'requiereVestimenta': bool(row[1])
                }
                for row in rows
            ]

    def obtener_horarios_actividad(self, actividad: str) -> List[Dict[str, Any]]:
        """
        Obtiene todos los horarios disponibles para una actividad.

        Args:
            actividad: Nombre de la actividad

        Returns:
            Lista de horarios con cupos disponibles
        """
        query = """
        SELECT h.hora, h.cupos_disponibles
        FROM horarios h
        JOIN actividades a ON h.actividad_id = a.id
        WHERE a.nombre = ?
        """
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(query, (actividad,))
            rows = cur.fetchall()
            return [
                {
                    'horario': row[0],
                    'cuposDisponibles': row[1]
                }
                for row in rows
            ]

    def existe_inscripcion_dni_en_horario(self, dni: str, horario: str) -> bool:
        """
        Devuelve True si existe una inscripción con el DNI en el mismo horario
        (independiente de la actividad).
        """
        query = """
        SELECT 1
        FROM inscripciones i
        JOIN horarios h ON i.horario_id = h.id
        WHERE i.dni = ? AND h.hora = ?
        LIMIT 1
        """
        with sqlite3.connect(self.db_path) as conn:
            cur = conn.cursor()
            cur.execute(query, (dni, horario))
            return cur.fetchone() is not None

# Instancia global del repositorio (inicialización lazy para evitar problemas con tests)
_repositorio_instance = None

def get_repositorio():
    """
    Obtiene la instancia del repositorio usando patrón Singleton lazy.
    
    Esto permite que los tests limpien la base de datos antes de que
    se inicialice el repositorio.
    """
    global _repositorio_instance
    if _repositorio_instance is None:
        _repositorio_instance = RepositorioActividadesSQLite()
    return _repositorio_instance


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

# funcion para validar si el horario existe para la actividad
# -> test inscribirse horario no disponible


def _validar_horario_existente(payload: Dict[str, Any]) -> ResultadoInscripcion:
    actividad = payload.get('actividad')
    horario = payload.get('horario')
    repo = get_repositorio()
    if not repo.horario_existe(actividad, horario):
        return ResultadoInscripcion(False, MSG_ERROR_HORARIO_NO_EXISTE)
    return None


def _validar_cantidad_personas(payload: Dict[str, Any]) -> ResultadoInscripcion:
    """
    Valida que la cantidad de personas sea válida (mayor a 0).
    """
    cantidad = payload.get('cantidadPersonas', 0)
    
    if not isinstance(cantidad, int) or cantidad < 1:
        return ResultadoInscripcion(False, MSG_ERROR_CANTIDAD_INVALIDA)
    
    return None


def _validar_cupo_disponible(payload: Dict[str, Any]) -> ResultadoInscripcion:
    actividad = payload.get('actividad')
    horario = payload.get('horario')
    cantidad = payload.get('cantidadPersonas', 1)

    repo = get_repositorio()
    cupos_disponibles = repo.obtener_cupos(actividad, horario)
    
    if cantidad > cupos_disponibles:
        return ResultadoInscripcion(
            False, 
            f"{MSG_ERROR_EXCEDE_CUPOS}. Disponibles: {cupos_disponibles}"
        )
    
    if not repo.hay_cupo(actividad, horario, cantidad):
        return ResultadoInscripcion(False, MSG_ERROR_SIN_CUPO)
    return None


def _validar_datos_personas(payload: Dict[str, Any]) -> ResultadoInscripcion:
    """
    Valida que los datos de las personas sean correctos:
    - Nombre: solo letras, espacios y guiones
    - DNI: solo números, entre 6 y 10 dígitos
    - Edad: mayor a 0
    """
    import re
    
    personas = payload.get('personas', [])
    
    for persona in personas:
        # Validar nombre (solo letras, espacios, guiones y acentos)
        nombre = persona.get('nombre', '')
        if not nombre or not re.match(r'^[A-Za-zÀ-ÿ\s\-\']+$', nombre):
            return ResultadoInscripcion(False, MSG_ERROR_NOMBRE_INVALIDO)
        
        # Validar DNI (solo números, entre 6 y 10 dígitos)
        dni = str(persona.get('DNI', ''))
        if not dni or not re.match(r'^\d{6,10}$', dni):
            return ResultadoInscripcion(False, MSG_ERROR_DNI_INVALIDO)
        
        # Validar edad (mayor a 0)
        edad = persona.get('edad')
        if not isinstance(edad, (int, float)):
            return ResultadoInscripcion(False, MSG_ERROR_EDAD_INVALIDA)
        
        if edad <= 0:
            return ResultadoInscripcion(False, MSG_ERROR_EDAD_CERO)
    
    return None


def _validar_edad_minima(payload: Dict[str, Any]) -> ResultadoInscripcion:
    """
    Valida que las personas cumplan con la edad mínima requerida.

    TDD FASE REFACTOR: Mejoras en validación y mensajes de error.

    Límites según Product Owner:
    - Palestra: 12 años mínimo
    - Tirolesa: 8 años mínimo
    - Safari y Jardinería: sin límite de edad

    Args:
        payload: Datos de la inscripción

    Returns:
        ResultadoInscripcion con error si hay personas menores al límite,
        None si todo está bien
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
            return ResultadoInscripcion(False, MSG_ERROR_EDAD_INVALIDA)

        if edad < limite_edad:
            mensaje_error = MSG_ERROR_EDAD_INSUFICIENTE.format(
                limite=limite_edad
            )
            return ResultadoInscripcion(False, mensaje_error)

    return None


def _validar_horario_parque(payload: Dict[str, Any]) -> ResultadoInscripcion:
    """
    Valida que la inscripción se realice dentro del horario de apertura.
    """
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

    if not (HORA_APERTURA_PARQUE <= horario_inscripcion <
            HORA_CIERRE_ACTIVIDADES):
        return ResultadoInscripcion(False, MSG_ERROR_FUERA_DE_HORARIO)

    return None

def _validar_conflicto_dni_horario(payload: Dict[str, Any]) -> ResultadoInscripcion:
    """
    Valida que ninguno de los DNI en la nueva inscripción ya esté
    inscripto en otra actividad en el mismo horario.
    """
    repo = get_repositorio()
    actividad = payload.get('actividad', '')
    horario = payload.get('horario', '')
    personas = payload.get('personas', [])

    conflictos = set()
    for persona in personas:
        dni = str(persona.get('DNI', '')).strip()
        if not dni:
            continue
        if repo.existe_inscripcion_dni_en_horario(dni, horario):
            conflictos.add(dni)

    if conflictos:
        dnis_str = ','.join(sorted(conflictos))
        return ResultadoInscripcion(False, MSG_ERROR_DNI_CONFLICTO.format(dnis=dnis_str))
    return None


# =============================
# Lógica principal
# =============================
def inscribirse_a_actividad(payload: Dict[str, Any]) -> str:
    """
    Procesa la inscripción a una actividad del parque.
    
    Returns:
        JSON string con el resultado de la inscripción
    """
    validaciones = [
         _validar_terminos_condiciones,
         _validar_datos_personas,
         _validar_talla_vestimenta,
         _validar_edad_minima,
         _validar_horario_parque,
         _validar_horario_existente,
        _validar_conflicto_dni_horario,
         _validar_cantidad_personas,
         _validar_cupo_disponible
    ]

    for validacion in validaciones:
        error = validacion(payload)
        if error:
            return error.to_json()

    # Obtener instancia del repositorio
    repo = get_repositorio()

    # Registrar inscripciones y obtener IDs
    ids_inscripciones = []
    for persona in payload.get("personas", []):
        id_inscripcion = repo.agregar_inscripcion(
            payload["actividad"], payload["horario"], persona
        )
        ids_inscripciones.append(id_inscripcion)
    
    # Descontar cupos
    repo.descontar_cupo(
        payload["actividad"], payload["horario"], payload["cantidadPersonas"]
    )

    # Generar ID de inscripción basado en el primer ID
    id_principal = f"INS-{ids_inscripciones[0]:05d}" if ids_inscripciones else "INS-00001"
    
    resultado = ResultadoInscripcion(
        exito=True,
        mensaje="Inscripción exitosa",
        id_inscripcion=id_principal
    )
    return resultado.to_json()