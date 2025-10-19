"""
Módulo para gestionar inscripciones a actividades del parque EcoHarmony Park.

User Story: Inscribirme a actividad
Como visitante QUIERO inscribirme a una actividad PARA reservar mi lugar en la misma.
"""

import json

# Actividades que requieren talla de vestimenta
ACTIVIDADES_CON_VESTIMENTA = ['Palestra', 'Tirolesa']

def inscribirse_a_actividad(payload):
    """
    Procesa la inscripción a una actividad del parque.
    
    Args:
        payload (dict): Diccionario con los datos de inscripción:
            - actividad (str): Nombre de la actividad
            - cantidadPersonas (int): Cantidad de personas
            - horario (str): Horario seleccionado
            - personas (list): Lista de diccionarios con datos de cada persona
            - aceptoTerminosYCondiciones (bool): Aceptación de términos
        
    Returns:
        str: JSON con el resultado de la operación
            - exito (bool): Si la inscripción fue exitosa
            - mensaje (str): Mensaje descriptivo del resultado
            - idInscripcion (str|None): ID de inscripción si fue exitosa
    """
    resultado = {
        "exito": False,
        "mensaje": "",
        "idInscripcion": None
    }
    
    # Validación 1: Verificar que se aceptaron los términos y condiciones
    if not payload.get('aceptoTerminosYCondiciones', False):
        resultado['mensaje'] = "Debe aceptar Términos y Condiciones"
        return json.dumps(resultado)
    
    # Validación 2: Verificar talla de vestimenta para actividades que la requieren
    actividad = payload.get('actividad', '')
    if actividad in ACTIVIDADES_CON_VESTIMENTA:
        personas = payload.get('personas', [])
        for persona in personas:
            talla = persona.get('tallaVestimenta')
            if talla is None or talla == '':
                resultado['mensaje'] = "La actividad requiere talla de vestimenta"
                return json.dumps(resultado)
    
    # Si pasa todas las validaciones
    resultado['exito'] = True
    resultado['mensaje'] = "Inscripción exitosa"
    resultado['idInscripcion'] = "INS-001"  # ID hardcodeado para GREEN phase
    
    return json.dumps(resultado)
