"""
Tests para la funcionalidad de inscripción a actividades.

Implementa los tests para la User Story 'Inscribirme a actividad'
siguiendo metodología TDD y utilizando Mocks para aislar la base de datos.
"""

import json
import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Agregar el directorio src al path para importar el módulo
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
)

from src.inscribirse_actividad import inscribirse_a_actividad

class TestInscripcionActividad(unittest.TestCase):
    """
    Tests para verificar la funcionalidad de inscripción a actividades.
    Estos tests utilizan mocks para no interactuar con la base de datos real.
    """

    # El método setUpClass que borraba la BD se ha eliminado.
    # Ya no es necesario porque los tests no tocarán la BD.

    def test_inscribirse_sin_aceptar_terminos_debe_fallar(self):
        """
        Verificar que NO se permite la inscripción a una actividad
        si 'aceptoTerminosYCondiciones' es False.
        Este test no necesita mock porque la validación ocurre antes
        de cualquier llamada a la base de datos.
        """
        # === PRECONDICIONES ===
        payload = {
            'actividad': 'Palestra',
            'cantidadPersonas': 1,
            'horario': '09:30 GMT-3',
            'personas': [{'nombre': 'Julian', 'tallaVestimenta': 'M', 'edad': 21, 'DNI': '44152639'}],
            'aceptoTerminosYCondiciones': False
        }

        # === ACT ===
        resultado = inscribirse_a_actividad(payload)

        # === ASSERT ===
        parsed = json.loads(resultado)
        self.assertFalse(parsed['exito'])
        self.assertEqual(parsed['mensaje'], "Debe aceptar Términos y Condiciones")
        self.assertIsNone(parsed.get('idInscripcion'))

    def test_inscribirse_sin_talle_requerido(self):
        """
        Verificar que NO se permite la inscripción a una actividad que
        requiere vestimenta si no se proporciona 'tallaVestimenta'.
        Este test tampoco necesita mock.
        """
        # === PRECONDICIONES ===
        payload = {
            'actividad': 'Palestra',
            'cantidadPersonas': 1,
            'horario': '09:30 GMT-3',
            'personas': [{'nombre': 'Julian', 'tallaVestimenta': None, 'edad': 21, 'DNI': '44152639'}],
            'aceptoTerminosYCondiciones': True
        }

        # === ACT ===
        resultado = inscribirse_a_actividad(payload)

        # === ASSERT ===
        parsed = json.loads(resultado)
        self.assertFalse(parsed['exito'])
        self.assertIn("talla de vestimenta", parsed['mensaje'].lower())

    @patch('inscribirse_actividad.get_repositorio')
    def test_inscribirse_sin_cupo_en_horario_seleccionado_debe_fallar(self, mock_get_repositorio):
        """
        Verificar que NO se permite la inscripción cuando no hay cupo.
        Se mockea el repositorio para simular falta de cupo.
        """
        # === CONFIGURACIÓN DEL MOCK ===
        # 1. Crear un mock para la instancia del repositorio
        mock_repo_instance = MagicMock()

        # 2. Configurar el comportamiento de los métodos del mock
        mock_repo_instance.horario_existe.return_value = True
        mock_repo_instance.existe_inscripcion_dni_en_horario.return_value = False
        # Simulamos que solo queda 1 cupo disponible
        mock_repo_instance.obtener_cupos.return_value = 1
        # Simulamos que `hay_cupo` devuelve False porque se piden 2
        mock_repo_instance.hay_cupo.return_value = False

        # 3. Hacer que get_repositorio() devuelva nuestra instancia mockeada
        mock_get_repositorio.return_value = mock_repo_instance

        # === PRECONDICIONES ===
        payload = {
            'actividad': 'Tirolesa',
            'cantidadPersonas': 2, # Se piden 2, pero solo hay 1
            'horario': '15:00 GMT-3',
            'personas': [
                {'nombre': 'Julian', 'tallaVestimenta': 'M', 'edad': 21, 'DNI': '44652639'},
                {'nombre': 'Fernando', 'tallaVestimenta': 'S', 'edad': 22, 'DNI': '44912833'}
            ],
            'aceptoTerminosYCondiciones': True
        }

        # === ACT ===
        resultado = inscribirse_a_actividad(payload)

        # === ASSERT ===
        parsed = json.loads(resultado)
        self.assertFalse(parsed['exito'], "Se permitió la inscripción pese a que no había cupo")
        self.assertIn("cupo", parsed['mensaje'].lower())
        
        # Verificamos que las funciones de escritura NUNCA fueron llamadas
        mock_repo_instance.agregar_inscripcion.assert_not_called()
        mock_repo_instance.descontar_cupo.assert_not_called()

    def test_inscribirse_con_edad_menor_al_limite_debe_fallar(self):
        """
        Verificar que NO se permite la inscripción con edad menor al límite.
        No requiere mock ya que la validación es previa a la BD.
        """
        # === PRECONDICIONES ===
        payload = {
            'actividad': 'Palestra',  # Requiere 12 años mínimo
            'cantidadPersonas': 1,
            'horario': '09:30 GMT-3',
            'personas': [{'nombre': 'Niño', 'tallaVestimenta': 'S', 'edad': 10, 'DNI': '99888777'}],
            'aceptoTerminosYCondiciones': True
        }

        # === ACT ===
        resultado = inscribirse_a_actividad(payload)

        # === ASSERT ===
        parsed = json.loads(resultado)
        self.assertFalse(parsed['exito'])
        self.assertIn("edad insuficiente", parsed['mensaje'].lower())

    @patch('inscribirse_actividad.get_repositorio')
    def test_inscribirse_exitosamente_con_todos_los_datos_correctos(self, mock_get_repositorio):
        """
        Verificar que la inscripción es exitosa con datos válidos.
        Se mockea el repositorio para simular que hay cupo y la inserción es exitosa.
        ¡ESTE TEST YA NO ESCRIBE EN LA BASE DE DATOS!
        """
        # === CONFIGURACIÓN DEL MOCK ===
        mock_repo_instance = MagicMock()
        mock_repo_instance.horario_existe.return_value = True
        mock_repo_instance.existe_inscripcion_dni_en_horario.return_value = False
        mock_repo_instance.obtener_cupos.return_value = 10  # Hay cupo de sobra
        mock_repo_instance.hay_cupo.return_value = True
        # Simulamos que la inserción en la BD devuelve el ID 123
        mock_repo_instance.agregar_inscripcion.return_value = 123
        mock_get_repositorio.return_value = mock_repo_instance

        # === PRECONDICIONES ===
        payload = {
            'actividad': 'Tirolesa',
            'cantidadPersonas': 1,
            'horario': '10:00 GMT-3',
            'personas': [{'nombre': 'Julian', 'tallaVestimenta': 'M', 'edad': 21, 'DNI': '44152639'}],
            'aceptoTerminosYCondiciones': True
        }

        # === ACT ===
        resultado = inscribirse_a_actividad(payload)

        # === ASSERT ===
        parsed = json.loads(resultado)
        self.assertTrue(parsed['exito'], f"La inscripción falló: {parsed.get('mensaje')}")
        self.assertEqual(parsed['mensaje'], "Inscripción exitosa")
        self.assertIsNotNone(parsed['idInscripcion'])
        self.assertEqual(parsed['idInscripcion'], "INS-00123") # Verifica que usa el ID del mock

        # === VERIFICACIÓN DEL MOCK ===
        # Verificar que los métodos de escritura SÍ fueron llamados
        mock_repo_instance.agregar_inscripcion.assert_called_once_with(
            'Tirolesa', '10:00 GMT-3', payload['personas'][0]
        )
        mock_repo_instance.descontar_cupo.assert_called_once_with(
            'Tirolesa', '10:00 GMT-3', 1
        )

    @patch('inscribirse_actividad.get_repositorio')
    def test_inscribirse_a_actividad_sin_requerir_vestimenta(self, mock_get_repositorio):
        """
        Verificar inscripción exitosa en actividad sin requerimiento de vestimenta.
        """
        # === CONFIGURACIÓN DEL MOCK ===
        mock_repo_instance = MagicMock()
        mock_repo_instance.horario_existe.return_value = True
        mock_repo_instance.existe_inscripcion_dni_en_horario.return_value = False
        mock_repo_instance.obtener_cupos.return_value = 15
        mock_repo_instance.hay_cupo.return_value = True
        mock_repo_instance.agregar_inscripcion.return_value = 124
        mock_get_repositorio.return_value = mock_repo_instance
        
        # === PRECONDICIONES ===
        payload = {
            'actividad': 'Jardineria',
            'cantidadPersonas': 1,
            'horario': '10:30 GMT-3',
            'personas': [{'nombre': 'Maria', 'tallaVestimenta': None, 'edad': 25, 'DNI': '40123456'}],
            'aceptoTerminosYCondiciones': True
        }

        # === ACT ===
        resultado = inscribirse_a_actividad(payload)

        # === ASSERT ===
        parsed = json.loads(resultado)
        self.assertTrue(parsed.get('exito'), f"La inscripción debió ser exitosa: {parsed.get('mensaje')}")
        self.assertEqual(parsed.get('mensaje'), "Inscripción exitosa")
        self.assertIsNotNone(parsed.get('idInscripcion'))
        
        # === VERIFICACIÓN DEL MOCK ===
        mock_repo_instance.agregar_inscripcion.assert_called_once()
        mock_repo_instance.descontar_cupo.assert_called_once()

    @patch('inscribirse_actividad.get_repositorio')
    def test_inscribirse_en_horario_no_disponible_debe_fallar(self, mock_get_repositorio):
        """
        Verificar que la inscripción falla si el horario no existe en el repositorio.
        """
        # === CONFIGURACIÓN DEL MOCK ===
        mock_repo_instance = MagicMock()
        # Simulamos que el horario NO existe para esta actividad
        mock_repo_instance.horario_existe.return_value = False
        mock_get_repositorio.return_value = mock_repo_instance

        # === PRECONDICIONES ===
        payload = {
            'actividad': 'Tirolesa',
            'cantidadPersonas': 1,
            'horario': '22:00 GMT-3', # Horario inválido
            'personas': [{'nombre': 'Carlos', 'tallaVestimenta': 'L', 'edad': 30, 'DNI': '35987654'}],
            'aceptoTerminosYCondiciones': True
        }

        # === ACT ===
        resultado = inscribirse_a_actividad(payload)

        # === ASSERT ===
        parsed = json.loads(resultado)
        self.assertFalse(parsed['exito'])
        self.assertIn("inscripción fuera del horario permitido", parsed['mensaje'].lower())
        
        # === VERIFICACIÓN DEL MOCK ===
        mock_repo_instance.agregar_inscripcion.assert_not_called()

    @patch('inscribirse_actividad.get_repositorio')
    def test_inscribirse_con_multiples_personas_validas(self, mock_get_repositorio):
        """
        Verificar que se puede inscribir múltiples personas válidas.
        """
        # === CONFIGURACIÓN DEL MOCK ===
        mock_repo_instance = MagicMock()
        mock_repo_instance.horario_existe.return_value = True
        mock_repo_instance.existe_inscripcion_dni_en_horario.return_value = False
        mock_repo_instance.obtener_cupos.return_value = 8
        mock_repo_instance.hay_cupo.return_value = True
        # Hacemos que `agregar_inscripcion` devuelva IDs diferentes en cada llamada
        mock_repo_instance.agregar_inscripcion.side_effect = [125, 126]
        mock_get_repositorio.return_value = mock_repo_instance

        # === PRECONDICIONES ===
        payload = {
            'actividad': 'Safari',
            'cantidadPersonas': 2,
            'horario': '14:00 GMT-3',
            'personas': [
                {'nombre': 'Julian', 'tallaVestimenta': None, 'edad': 21, 'DNI': '30123456'},
                {'nombre': 'Angel', 'tallaVestimenta': None, 'edad': 22, 'DNI': '31987654'}
            ],
            'aceptoTerminosYCondiciones': True
        }

        # === ACT ===
        resultado = inscribirse_a_actividad(payload)

        # === ASSERT ===
        parsed = json.loads(resultado)
        self.assertTrue(parsed['exito'], f"La inscripción falló: {parsed.get('mensaje')}")
        self.assertEqual(parsed['mensaje'], "Inscripción exitosa")
        self.assertEqual(parsed['idInscripcion'], "INS-00125") # Basado en el primer ID de side_effect

        # === VERIFICACIÓN DEL MOCK ===
        self.assertEqual(mock_repo_instance.agregar_inscripcion.call_count, 2)
        mock_repo_instance.descontar_cupo.assert_called_once_with('Safari', '14:00 GMT-3', 2)


if __name__ == "__main__":
    unittest.main()