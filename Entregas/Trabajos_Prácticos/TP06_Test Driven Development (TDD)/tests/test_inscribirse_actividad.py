import unittest
from unittest.mock import patch
import json
import sys
import os

# Agregar el directorio src al path para importar el módulo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '')))

from src.inscribirse_actividad import inscribirse_a_actividad

class TestInscripcionActividad(unittest.TestCase):
    def _verificar_inscripcion_fallida(self, payload, mensaje_esperado):
        """
        Método auxiliar para verificar los casos de prueba de inscripciones fallidas.
        """
        # ACT
        try:
            resultado = inscribirse_a_actividad(payload)
        except NotImplementedError:
            self.skipTest("Implementar 'inscribirse_a_actividad' para correr este test")

        # ASSERT
        self.assertIsInstance(
            resultado, str,
            "La función debe devolver un string con formato JSON"
        )

        try:
            parsed = json.loads(resultado)
        except json.JSONDecodeError:
            self.fail(f"La respuesta no es un JSON válido: {resultado}")

        self.assertIn('exito', parsed, "El resultado debe incluir la clave 'exito'")
        self.assertIn('mensaje', parsed, "El resultado debe incluir la clave 'mensaje'")

        self.assertFalse(
            parsed['exito'],
            f"Se esperaba que la inscripción fallara, pero fue exitosa. Mensaje: {parsed.get('mensaje')}"
        )

        self.assertEqual(
            parsed['mensaje'],
            mensaje_esperado,
            "El mensaje de error no coincide con lo esperado"
        )

        if 'idInscripcion' in parsed:
            self.assertIsNone(
                parsed['idInscripcion'],
                "No debería generarse 'idInscripcion' cuando la inscripción falla"
            )

    # ============================================================
    # TEST 1: Sin aceptar Términos y Condiciones (FALLA)
    # ============================================================

    def test_inscribirse_sin_aceptar_terminos_debe_fallar(self):
        """
        Caso de prueba (TDD):
        Verificar que NO se permite la inscripción a una actividad
        si 'aceptoTerminosYCondiciones' es False.
        """
        # === PRECONDICIONES ===
        # TODO - Falta usuario en precondicion
        payload = {
            'actividad': 'Palestra',
            'cantidadPersonas': 1,
            'horario': '09:30 GMT-3',
            'personas': [
                {
                    'nombre': 'Julian',
                    'tallaVestimenta': 'M',
                    'edad': 21,
                    'DNI': '44152639'
                }
            ],
            'aceptoTerminosYCondiciones': False
        }

        # === ACT ===
        try:
            resultado = inscribirse_a_actividad(payload)
        except NotImplementedError:
            self.skipTest("Implementar 'inscribirse_a_actividad' para correr este test")

        # === ASSERT ===
        self.assertIsInstance(
            resultado, str,
            "La función debe devolver un string con formato JSON"
        )

        try:
            parsed = json.loads(resultado)
        except json.JSONDecodeError:
            self.fail("La respuesta no tiene un formato JSON válido")

        self.assertIn('exito', parsed, "El resultado debe incluir la clave 'exito'")
        self.assertIn('mensaje', parsed, "El resultado debe incluir la clave 'mensaje'")

        self.assertFalse(
            parsed['exito'],
            "Se permitió la inscripción sin aceptar los Términos y Condiciones"
        )

        self.assertEqual(
            parsed['mensaje'],
            "Debe aceptar Términos y Condiciones",
            "El mensaje de error no coincide con lo esperado"
        )

        if 'idInscripcion' in parsed:
            self.assertIsNone(
                parsed['idInscripcion'],
                "No debería generarse 'idInscripcion' cuando la inscripción falla"
            )

        

    # ============================================================
    # TEST 2: Sin ingresar talle de vestimenta requerido (FALLA)
    # ============================================================
    # Refactorizado

    def test_inscribirse_sin_talle_requerido(self):
        """
        Caso de prueba (TDD):
        Verificar que NO se permite la inscripción a una actividad que requiere
        vestimenta (Palestra o Tirolesa) si no se proporciona 'tallaVestimenta'.
        """
        # === PRECONDICIONES ===
        # Palestra y Tirolesa requieren talla de vestimenta
        # Safari y Jardinería NO requieren talla de vestimenta
        payload = {
            'actividad': 'Palestra',  # Requiere vestimenta
            'cantidadPersonas': 1,
            'horario': '09:30 GMT-3',
            'personas': [
                {
                    'nombre': 'Julian',
                    'tallaVestimenta': None,  # ¡NO SE PROPORCIONA TALLE!
                    'edad': 21,
                    'DNI': '44152639'
                }
            ],
            'aceptoTerminosYCondiciones': True
        }

        # === ACT ===
        try:
            resultado = inscribirse_a_actividad(payload)
        except NotImplementedError:
            self.skipTest("Implementar 'inscribirse_a_actividad' para correr este test")

        # === ASSERT ===
        self.assertIsInstance(
            resultado, str,
            "La función debe devolver un string con formato JSON"
        )

        try:
            parsed = json.loads(resultado)
        except json.JSONDecodeError:
            self.fail("La respuesta no tiene un formato JSON válido")

        self.assertIn('exito', parsed, "El resultado debe incluir la clave 'exito'")
        self.assertIn('mensaje', parsed, "El resultado debe incluir la clave 'mensaje'")

        self.assertFalse(
            parsed['exito'],
            "Se permitió la inscripción sin ingresar talla de vestimenta requerida"
        )

        self.assertIn(
            "talla de vestimenta",
            parsed['mensaje'].lower(),
            "El mensaje de error debe mencionar la falta de talla de vestimenta"
        )

        if 'idInscripcion' in parsed:
            self.assertIsNone(
                parsed['idInscripcion'],
                "No debería generarse 'idInscripcion' cuando la inscripción falla"
            )


    def test_inscribirse_sin_cupo_en_horario_seleccionado_debe_fallar(self):
        """
        Caso de prueba (TDD):
        Verificar que NO se permite la inscripción a una actividad
        cuando no hay cupo disponible para el horario seleccionado.
        """
        # === PRECONDICIONES ===
        payload = {
            'actividad': 'Tirolesa',
            'cantidadPersonas': 2,
            'horario': '15:00 GMT-3',  # Horario sin cupo disponible
            'personas': [
                {
                    'nombre': 'Julian',
                    'tallaVestimenta': 'M',
                    'edad': 21,
                    'DNI': '44152639'
                },
                {
                    'nombre': 'Fernando',
                    'tallaVestimenta': 'S',
                    'edad': 22,
                    'DNI': '44912833'
                }
            ],
            'aceptoTerminosYCondiciones': True
        }

        # === ACT ===
        try:
            resultado = inscribirse_a_actividad(payload)
        except NotImplementedError:
            self.skipTest("Implementar 'inscribirse_a_actividad' para correr este test")

        # === ASSERT ===
        self.assertIsInstance(
            resultado, str,
            "La función debe devolver un string con formato JSON"
        )

        try:
            parsed = json.loads(resultado)
        except json.JSONDecodeError:
            self.fail("La respuesta no tiene un formato JSON válido")

        self.assertIn('exito', parsed, "El resultado debe incluir la clave 'exito'")
        self.assertIn('mensaje', parsed, "El resultado debe incluir la clave 'mensaje'")

        # --- Verifica que la inscripción fue rechazada por falta de cupo ---
        self.assertFalse(
            parsed['exito'],
            "Se permitió la inscripción pese a que no había cupo disponible"
        )


    # ============================================================
    # TEST 7: Inscripción con edad menor al límite requerido (FALLA) - TDD RED
    # ============================================================
    
    def test_inscribirse_con_edad_menor_al_limite_debe_fallar(self):
        """
        Caso de prueba TDD - FASE RED:
        Verificar que NO se permite la inscripción cuando la edad
        de la persona es menor al límite requerido por la actividad.
        Palestra: 12 años mínimo, Tirolesa: 8 años mínimo
        """
        # === PRECONDICIONES ===
        payload = {
            'actividad': 'Palestra',  # Requiere 12 años mínimo
            'cantidadPersonas': 1,
            'horario': '09:30 GMT-3',
            'personas': [
                {
                    'nombre': 'Niño',
                    'tallaVestimenta': 'S',
                    'edad': 10,  # MENOR AL LÍMITE DE 12 AÑOS
                    'DNI': '99888777'
                }
            ],
            'aceptoTerminosYCondiciones': True
        }

        # === ACT ===
        try:
            resultado = inscribirse_a_actividad(payload)
        except NotImplementedError:
            self.skipTest("Implementar 'inscribirse_a_actividad' para correr este test")

        # === ASSERT ===
        self.assertIsInstance(
            resultado, str,
            "La función debe devolver un string con formato JSON"
        )

        try:
            parsed = json.loads(resultado)
        except json.JSONDecodeError:
            self.fail("La respuesta no tiene un formato JSON válido")

        self.assertIn('exito', parsed, "El resultado debe incluir la clave 'exito'")
        self.assertIn('mensaje', parsed, "El resultado debe incluir la clave 'mensaje'")

        # --- Verifica que la inscripción fue rechazada por edad ---
        self.assertFalse(
            parsed['exito'],
            "Se permitió la inscripción con edad menor al límite requerido"
        )

        self.assertIn(
            "edad",
            parsed['mensaje'].lower(),
            "El mensaje de error debe mencionar el problema de edad"
        )

        if 'idInscripcion' in parsed:
            self.assertIsNone(
                parsed['idInscripcion'],
                "No debería generarse 'idInscripcion' cuando la inscripción falla"
            )


    # ============================================================
    # Probar inscribirse a una actividad seleccionando un horario en el cual 
    # el parque está cerrado o la actividad no está disponible (Falla)
    # ============================================================
    def test_inscribirse_fuera_de_horario_parque_y_actividad_abierto_debe_fallar(self):
        """
        Caso de prueba (TDD):
        Verificar que NO se permite la inscripción a una actividad
        si se intenta fuera del horario en el que el parque está abierto y la actividad no está disponible.
        """
        # === PRECONDICIONES ===
        payload = {
            'actividad': 'Tirolesa',
            'cantidadPersonas': 1,
            'horario': '22:30 GMT-3',
            'personas': [
                {
                    'nombre': 'Julian',
                    'tallaVestimenta': 'M',
                    'edad': 21,
                    'DNI': '44152639'
                }
            ],
            'aceptoTerminosYCondiciones': True
        }
        mensaje_esperado = "Inscripción fuera del horario permitido"

        # === ACT & ASSERT ===
        self._verificar_inscripcion_fallida(payload, mensaje_esperado)


    @patch('src.inscribirse_actividad.repositorio')
    def test_inscribirse_a_una_actividad_debe_pasar(self, mock_repositorio):
        """
        Verifica que una inscripción exitosa funcione correctamente,
        utilizando un mock para simular la base de datos.
        """
        # 1. Arrange: Configure the mock to simulate a successful scenario.
        # We tell the mock to return 'True' when these methods are called.
        mock_repositorio.horario_existe.return_value = True
        mock_repositorio.hay_cupo.return_value = True

        payload = {
            'actividad': 'Tirolesa',
            'cantidadPersonas': 1,
            'horario': '10:00 GMT-3',
            'personas': [{
                'nombre': 'Test User',
                'tallaVestimenta': 'L',
                'edad': 25,
                'DNI': '12345678'
            }],
            'aceptoTerminosYCondiciones': True
        }

        # 2. Act: Call the function. It will now use your mock_repositorio.
        resultado = inscribirse_a_actividad(payload)
        parsed = json.loads(resultado)

        # 3. Assert: Verify the successful result.
        self.assertTrue(parsed['exito'])
        self.assertEqual(parsed['mensaje'], "Inscripción exitosa")
        self.assertIsNotNone(parsed['idInscripcion'])

        # 4. Verify database interactions: Check that the function
        # tried to write to the database as expected.
        mock_repositorio.agregar_inscripcion.assert_called_once()
        mock_repositorio.descontar_cupo.assert_called_once_with(
            'Tirolesa', '10:00 GMT-3', 1
        )


    def test_inscribirse_actividad_horario_no_disponible(self):
        """
        Caso de prueba (TDD):
        Verificar que NO se permite la inscripción a una actividad en un
        horario que no está disponible para la misma.
        """
        # === PRECONDICIONES ===
        payload = {
            'actividad': 'Safari',
            'cantidadPersonas': 1,
            'horario': '11:00 GMT-3',  # Horario NO existente para Safari
            'personas': [
                {
                    'nombre': 'Juan',
                    'edad': 30,
                    'DNI': '30123456'
                }
            ],
            'aceptoTerminosYCondiciones': True
        }
        mensaje_esperado = "El horario seleccionado no existe para la actividad indicada"

        # === ACT & ASSERT ===
        self._verificar_inscripcion_fallida(payload, mensaje_esperado)

if __name__ == "__main__":
    unittest.main()
    