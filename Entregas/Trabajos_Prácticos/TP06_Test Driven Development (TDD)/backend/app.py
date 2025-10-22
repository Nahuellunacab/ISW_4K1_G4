"""
API REST para el sistema de inscripción a actividades de EcoHarmony Park.

Este módulo implementa los endpoints necesarios para:
- Listar actividades disponibles
- Obtener horarios de cada actividad
- Procesar inscripciones
"""

import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Agregar src al path
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
)

from src.inscribirse_actividad import (
    inscribirse_a_actividad,
    get_repositorio
)

# Inicializar Flask
app = Flask(__name__)
CORS(app)


def obtener_repositorio():
    """
    Obtiene la instancia del repositorio para el backend.
    
    Usa la función get_repositorio() que maneja la inicialización lazy.
    """
    return get_repositorio()


@app.route('/api/actividades', methods=['GET'])
def obtener_actividades():
    """
    Endpoint para obtener todas las actividades disponibles.

    Returns:
        JSON con lista de actividades
    """
    try:
        repo = obtener_repositorio()
        actividades = repo.obtener_todas_actividades()
        return jsonify({
            'exito': True,
            'actividades': actividades
        }), 200
    except Exception as e:
        return jsonify({
            'exito': False,
            'mensaje': f'Error al obtener actividades: {str(e)}'
        }), 500


@app.route('/api/actividades/<nombre_actividad>/horarios', methods=['GET'])
def obtener_horarios(nombre_actividad):
    """
    Endpoint para obtener los horarios de una actividad específica.

    Args:
        nombre_actividad: Nombre de la actividad

    Returns:
        JSON con lista de horarios disponibles
    """
    try:
        repo = obtener_repositorio()
        horarios = repo.obtener_horarios_actividad(nombre_actividad)
        return jsonify({
            'exito': True,
            'horarios': horarios
        }), 200
    except Exception as e:
        return jsonify({
            'exito': False,
            'mensaje': f'Error al obtener horarios: {str(e)}'
        }), 500


@app.route('/api/inscripciones', methods=['POST'])
def crear_inscripcion():
    """
    Endpoint para crear una nueva inscripción.

    Recibe en el body:
    {
        "actividad": "Nombre de la actividad",
        "cantidadPersonas": 2,
        "horario": "10:00 GMT-3",
        "personas": [
            {
                "nombre": "Juan",
                "tallaVestimenta": "M",
                "edad": 25,
                "DNI": "12345678"
            }
        ],
        "aceptoTerminosYCondiciones": true
    }

    Returns:
        JSON con el resultado de la inscripción
    """
    try:
        datos = request.get_json()

        if not datos:
            return jsonify({
                'exito': False,
                'mensaje': 'No se recibieron datos'
            }), 400

        # Procesar inscripción
        resultado_str = inscribirse_a_actividad(datos)
        resultado = json.loads(resultado_str)

        status_code = 200 if resultado.get('exito') else 400

        return jsonify(resultado), status_code

    except json.JSONDecodeError:
        return jsonify({
            'exito': False,
            'mensaje': 'Error al procesar JSON'
        }), 400
    except Exception as e:
        return jsonify({
            'exito': False,
            'mensaje': f'Error interno: {str(e)}'
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint para verificar el estado del servidor."""
    return jsonify({
        'status': 'OK',
        'mensaje': 'API funcionando correctamente'
    }), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
