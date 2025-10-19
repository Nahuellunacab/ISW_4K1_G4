"""
Módulo para gestionar inscripciones a actividades del parque EcoHarmony Park.

User Story: Inscribirme a actividad
Como visitante QUIERO inscribirme a una actividad PARA reservar mi lugar en la misma.
"""

import json
from typing import Dict, Any, List

# Constantes de configuración del parque
ACTIVIDADES_CON_VESTIMENTA = ['Palestra', 'Tirolesa']
ACTIVIDADES_SIN_VESTIMENTA = ['Safari', 'Jardineria']
TALLES_VALIDOS = ['XS', 'S', 'M', 'L', 'XL', 'XXL']

# Mensajes de error
MSG_ERROR_TERMINOS = "Debe aceptar Términos y Condiciones"
MSG_ERROR_TALLA_REQUERIDA = "La actividad requiere talla de vestimenta"


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


def _validar_terminos_condiciones(payload: Dict[str, Any]) -> ResultadoInscripcion:
    """
    Valida que se hayan aceptado los términos y condiciones.
    
    Args:
        payload: Datos de inscripción
        
    Returns:
        ResultadoInscripcion con error si no se aceptaron términos, None si es válido
    """
    # Si payload tiene aceptoTerminosYCondiciones, se devuelve su valor que 
    # sería False en el caso de que se retorne algo.
    # Si es False, entonces not False = True, por lo que entraría al blque con el primer return.
    if not payload.get('aceptoTerminosYCondiciones', False):
        return ResultadoInscripcion(False, MSG_ERROR_TERMINOS)
    return None


def _validar_talla_vestimenta(payload: Dict[str, Any]) -> ResultadoInscripcion:
    """
    Valida que se proporcione talla de vestimenta para actividades que la requieren.
    
    Args:
        payload: Datos de inscripción
        
    Returns:
        ResultadoInscripcion con error si falta la talla, None si es válido
    """
    actividad = payload.get('actividad', '')
    
    if actividad not in ACTIVIDADES_CON_VESTIMENTA:
        return None
    
    personas = payload.get('personas', [])
    for persona in personas:
        talla = persona.get('tallaVestimenta')
        if not talla:  # None, '', o cualquier valor falsy
            return ResultadoInscripcion(False, MSG_ERROR_TALLA_REQUERIDA)
    
    return None


# Cupos simulados por horario y actividad (esto sería una BD en un sistema real)
CUPOS_POR_HORARIO = {
    'Tirolesa': {
        '15:00 GMT-3': 0,   # sin cupos
        '10:00 GMT-3': 5,   # con cupos disponibles
    },
    'Palestra': {
        '09:30 GMT-3': 2,
    },
    'Safari': {
        '14:00 GMT-3': 10,
    }
}

MSG_ERROR_SIN_CUPO = "No hay cupos disponibles para el horario seleccionado"


def _validar_cupo_disponible(payload: Dict[str, Any]) -> ResultadoInscripcion:
    """
    Valida que haya cupos disponibles para el horario seleccionado.
    """
    actividad = payload.get('actividad')
    horario = payload.get('horario')
    cantidad = payload.get('cantidadPersonas', 1)

    cupos_actividad = CUPOS_POR_HORARIO.get(actividad, {})
    cupos_disponibles = cupos_actividad.get(horario, 0)

    # Si no hay cupos suficientes, devolver error
    if cupos_disponibles < cantidad:
        return ResultadoInscripcion(False, MSG_ERROR_SIN_CUPO)

    return None


def inscribirse_a_actividad(payload: Dict[str, Any]) -> str:
    """
    Procesa la inscripción a una actividad del parque.
    
    Args:
        payload: Diccionario con los datos de inscripción:
            - actividad (str): Nombre de la actividad
            - cantidadPersonas (int): Cantidad de personas
            - horario (str): Horario seleccionado
            - personas (list): Lista de diccionarios con datos de cada persona
            - aceptoTerminosYCondiciones (bool): Aceptación de términos
        
    Returns:
        JSON string con el resultado de la operación:
            - exito (bool): Si la inscripción fue exitosa
            - mensaje (str): Mensaje descriptivo del resultado
            - idInscripcion (str|None): ID de inscripción si fue exitosa
    """
    # Ejecutar validaciones en orden de prioridad
    validaciones = [
        _validar_terminos_condiciones,
        _validar_talla_vestimenta,
        _validar_cupo_disponible
    ]
    
    for validacion in validaciones:
        error = validacion(payload)
        if error:
            return error.to_json()
    
    # Si todas las validaciones pasan, la inscripción es exitosa
    resultado = ResultadoInscripcion(
        exito=True,
        mensaje="Inscripción exitosa",
        id_inscripcion="INS-001"  # En producción sería generado dinámicamente
    )
    
    return resultado.to_json()



