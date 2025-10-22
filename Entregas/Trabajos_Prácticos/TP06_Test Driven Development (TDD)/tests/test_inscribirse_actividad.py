"""
Tests para la funcionalidad de inscripción a actividades.

Implementa los tests para la User Story 'Inscribirme a actividad'
siguiendo metodología TDD.
"""

import json
import os
import sys
import unittest

# Agregar el directorio src al path para importar el módulo
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
)

from inscribirse_actividad import inscribirse_a_actividad
import inscribirse_actividad


class TestInscripcionActividad(unittest.TestCase):
    """Tests para verificar la funcionalidad de inscripción a actividades."""
    
    @classmethod
    def setUpClass(cls):
        """
        Limpia la base de datos antes de ejecutar todos los tests.
        
        Si la BD está bloqueada por otro proceso (ej: backend corriendo),
        simplemente la usa sin limpiarla. Los tests seguirán funcionando
        correctamente gracias a las validaciones y datos de prueba específicos.
        """
        db_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'actividades.db')
        )
        
        # Intentar limpiar la BD
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
                print(f"\n✓ Base de datos limpiada: {db_path}\n")
            except PermissionError:
                print(f"\n⚠️  Base de datos en uso por otro proceso")
                print(f"   Los tests se ejecutarán con la BD existente")
                print(f"   TIP: Cierra el backend antes de ejecutar tests\n")
        
        # Resetear la instancia global del repositorio
        inscribirse_actividad._repositorio_instance = None


    def test_inscribirse_sin_aceptar_terminos_debe_fallar(self):
        """
        Caso de prueba (TDD):
        Verificar que NO se permite la inscripción a una actividad
        si 'aceptoTerminosYCondiciones' es False.
        """
        # === PRECONDICIONES ===
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
            self.skipTest(
                "Implementar 'inscribirse_a_actividad' para correr este test"
            )

        # === ASSERT ===
        self.assertIsInstance(
            resultado, str,
            "La función debe devolver un string con formato JSON"
        )

        try:
            parsed = json.loads(resultado)
        except json.JSONDecodeError:
            self.fail("La respuesta no tiene un formato JSON válido")

        self.assertIn(
            'exito', parsed, "El resultado debe incluir la clave 'exito'"
        )
        self.assertIn(
            'mensaje', parsed, "El resultado debe incluir la clave 'mensaje'"
        )

        self.assertFalse(
            parsed['exito'],
            ("Se permitió la inscripción sin aceptar los Términos y "
             "Condiciones")
        )

        self.assertEqual(
            parsed['mensaje'],
            "Debe aceptar Términos y Condiciones",
            "El mensaje de error no coincide con lo esperado"
        )

        if 'idInscripcion' in parsed:
            self.assertIsNone(
                parsed['idInscripcion'],
                ("No debería generarse 'idInscripcion' cuando la inscripción "
                 "falla")
            )

    def test_inscribirse_sin_talle_requerido(self):
        """
        Caso de prueba (TDD):
        Verificar que NO se permite la inscripción a una actividad que 
        requiere vestimenta (Palestra o Tirolesa) si no se proporciona 
        'tallaVestimenta'.
        """
        # === PRECONDICIONES ===
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
            self.skipTest(
                "Implementar 'inscribirse_a_actividad' para correr este test"
            )

        # === ASSERT ===
        self.assertIsInstance(
            resultado, str,
            "La función debe devolver un string con formato JSON"
        )

        try:
            parsed = json.loads(resultado)
        except json.JSONDecodeError:
            self.fail("La respuesta no tiene un formato JSON válido")

        self.assertIn(
            'exito', parsed, "El resultado debe incluir la clave 'exito'"
        )
        self.assertIn(
            'mensaje', parsed, "El resultado debe incluir la clave 'mensaje'"
        )

        self.assertFalse(
            parsed['exito'],
            ("Se permitió la inscripción sin ingresar talla de vestimenta "
             "requerida")
        )

        self.assertIn(
            "talla de vestimenta",
            parsed['mensaje'].lower(),
            "El mensaje de error debe mencionar la falta de talla de vestimenta"
        )

        if 'idInscripcion' in parsed:
            self.assertIsNone(
                parsed['idInscripcion'],
                ("No debería generarse 'idInscripcion' cuando la inscripción "
                 "falla")
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
                    'DNI': '44652639'
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
            self.skipTest(
                "Implementar 'inscribirse_a_actividad' para correr este test"
            )

        # === ASSERT ===
        self.assertIsInstance(
            resultado, str,
            "La función debe devolver un string con formato JSON"
        )

        try:
            parsed = json.loads(resultado)
        except json.JSONDecodeError:
            self.fail("La respuesta no tiene un formato JSON válido")

        self.assertIn(
            'exito', parsed, "El resultado debe incluir la clave 'exito'"
        )
        self.assertIn(
            'mensaje', parsed, "El resultado debe incluir la clave 'mensaje'"
        )

        # --- Verifica que la inscripción fue rechazada por falta de cupo ---
        self.assertFalse(
            parsed['exito'],
            "Se permitió la inscripción pese a que no había cupo disponible"
        )

    def test_inscribirse_con_edad_menor_al_limite_debe_fallar(self):
        """
        Caso de prueba TDD:
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
            self.skipTest(
                "Implementar 'inscribirse_a_actividad' para correr este test"
            )

        # === ASSERT ===
        self.assertIsInstance(
            resultado, str,
            "La función debe devolver un string con formato JSON"
        )

        try:
            parsed = json.loads(resultado)
        except json.JSONDecodeError:
            self.fail("La respuesta no tiene un formato JSON válido")

        self.assertIn(
            'exito', parsed, "El resultado debe incluir la clave 'exito'"
        )
        self.assertIn(
            'mensaje', parsed, "El resultado debe incluir la clave 'mensaje'"
        )

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
                ("No debería generarse 'idInscripcion' cuando la inscripción "
                 "falla")
            )

    def test_inscribirse_exitosamente_con_todos_los_datos_correctos(self):
        """
        Caso de prueba (TDD):
        Verificar que se permite la inscripción cuando todos los datos
        son válidos y hay cupo disponible.
        """
        # === PRECONDICIONES ===
        payload = {
            'actividad': 'Tirolesa',
            'cantidadPersonas': 1,
            'horario': '10:00 GMT-3',  # Horario con cupos disponibles
            'personas': [
                {
                    'nombre': 'Julian',
                    # Talla proporcionada para actividad que lo requiere
                    'tallaVestimenta': 'M',
                    'edad': 21,  # Mayor a 8 años (límite de Tirolesa)
                    'DNI': '44152639'
                }
            ],
            'aceptoTerminosYCondiciones': True  # Términos aceptados
        }

        # === ACT ===
        try:
            resultado = inscribirse_a_actividad(payload)
        except NotImplementedError:
            self.skipTest(
                "Implementar 'inscribirse_a_actividad' para correr este test"
            )

        # === ASSERT ===
        self.assertIsInstance(
            resultado, str,
            "La función debe devolver un string con formato JSON"
        )

        try:
            parsed = json.loads(resultado)
        except json.JSONDecodeError:
            self.fail("La respuesta no tiene un formato JSON válido")

        self.assertIn(
            'exito', parsed, "El resultado debe incluir la clave 'exito'"
        )
        self.assertIn(
            'mensaje', parsed, "El resultado debe incluir la clave 'mensaje'"
        )

        # --- Verifica que la inscripción fue exitosa ---
        self.assertTrue(
            parsed['exito'],
            (f"La inscripción falló cuando debería haber sido exitosa. "
             f"Mensaje: {parsed.get('mensaje')}")
        )

        self.assertEqual(
            parsed['mensaje'],
            "Inscripción exitosa",
            "El mensaje de éxito no coincide con lo esperado"
        )

        # --- Verifica que se generó un ID de inscripción ---
        self.assertIn(
            'idInscripcion', parsed,
            "Debe incluir 'idInscripcion' cuando la inscripción es exitosa"
        )
        self.assertIsNotNone(
            parsed['idInscripcion'], "El 'idInscripcion' no debe ser None"
        )
        self.assertNotEqual(
            parsed['idInscripcion'], "", "El 'idInscripcion' no debe estar vacío"
        )

    def test_inscribirse_a_actividad_sin_requerir_vestimenta(self):
        """
        Caso de prueba (TDD):
        Verificar que se puede inscribir a actividades que NO requieren
        talla de vestimenta (Safari, Jardinería) sin proporcionar talla.
        """
        # === PRECONDICIONES ===
        payload = {
            'actividad': 'Jardineria',  # NO requiere vestimenta
            'cantidadPersonas': 1,
            'horario': '10:30 GMT-3',  # Horario con cupo disponible
            'personas': [
                {
                    'nombre': 'Maria',
                    # No se proporciona talla (no es necesaria)
                    'tallaVestimenta': None,
                    'edad': 25,
                    'DNI': '40123456'
                }
            ],
            'aceptoTerminosYCondiciones': True
        }

        # === ACT ===
        try:
            resultado = inscribirse_a_actividad(payload)
        except NotImplementedError:
            self.skipTest(
                "Implementar 'inscribirse_a_actividad' para correr este test"
            )

        # === ASSERT ===
        self.assertIsInstance(
            resultado, str,
            "La función debe devolver un string con formato JSON"
        )

        try:
            parsed = json.loads(resultado)
        except json.JSONDecodeError:
            self.fail(f"La respuesta no es un JSON válido: {resultado}")

        self.assertTrue(
            parsed.get('exito'),
            (f"La inscripción debió ser exitosa, pero falló con: "
             f"{parsed.get('mensaje')}")
        )
        self.assertEqual(parsed.get('mensaje'), "Inscripción exitosa")
        self.assertIsNotNone(
            parsed.get('idInscripcion'), "Debe generarse un idInscripcion"
        )

    def test_inscribirse_en_horario_no_disponible_debe_fallar(self):
        """
        Caso de prueba (TDD):
        Verificar que NO se permite la inscripción cuando se selecciona
        un horario en el cual el parque está cerrado o la actividad no 
        está disponible.
        """
        # === PRECONDICIONES ===
        payload = {
            'actividad': 'Tirolesa',
            'cantidadPersonas': 1,
            # Horario fuera del rango disponible (parque cerrado)
            'horario': '22:00 GMT-3',
            'personas': [
                {
                    'nombre': 'Carlos',
                    'tallaVestimenta': 'L',
                    'edad': 30,
                    'DNI': '35987654'
                }
            ],
            'aceptoTerminosYCondiciones': True
        }

        # === ACT ===
        try:
            resultado = inscribirse_a_actividad(payload)
        except NotImplementedError:
            self.skipTest(
                "Implementar 'inscribirse_a_actividad' para correr este test"
            )

        # === ASSERT ===
        self.assertIsInstance(
            resultado, str,
            "La función debe devolver un string con formato JSON"
        )

        try:
            parsed = json.loads(resultado)
        except json.JSONDecodeError:
            self.fail("La respuesta no tiene un formato JSON válido")

        self.assertIn(
            'exito', parsed, "El resultado debe incluir la clave 'exito'"
        )
        self.assertIn(
            'mensaje', parsed, "El resultado debe incluir la clave 'mensaje'"
        )

        # --- Verifica que la inscripción fue rechazada ---
        self.assertFalse(
            parsed['exito'],
            "Se permitió la inscripción en horario no disponible/parque cerrado"
        )

        # El mensaje puede ser sobre falta de cupo o horario no disponible
        mensaje_lower = parsed['mensaje'].lower()
        self.assertTrue(
            ("cupo" in mensaje_lower or "horario" in mensaje_lower or
             "disponible" in mensaje_lower),
            (f"El mensaje '{parsed['mensaje']}' debe mencionar la falta de "
             f"disponibilidad")
        )

        if 'idInscripcion' in parsed:
            self.assertIsNone(
                parsed['idInscripcion'],
                ("No debería generarse 'idInscripcion' cuando la inscripción "
                 "falla")
            )

    def test_inscribirse_con_multiples_personas_validas(self):
        """
        Caso de prueba (TDD):
        Verificar que se puede inscribir múltiples personas cuando todos 
        los datos son válidos y hay cupo suficiente.
        """
        # === PRECONDICIONES ===
        payload = {
            'actividad': 'Safari',  # NO requiere vestimenta y tiene 8 cupos
            'cantidadPersonas': 2,  # Múltiples personas
            'horario': '14:00 GMT-3',  # Horario con cupo disponible
            'personas': [
                {
                    'nombre': 'Julian',
                    'tallaVestimenta': None,  # No requiere talla
                    'edad': 21,
                    'DNI': '30123456'
                },
                {
                    'nombre': 'Angel',
                    'tallaVestimenta': None,  # No requiere talla
                    'edad': 22,
                    'DNI': '31987654'
                }
            ],
            'aceptoTerminosYCondiciones': True
        }

        # === ACT ===
        try:
            resultado = inscribirse_a_actividad(payload)
        except NotImplementedError:
            self.skipTest(
                "Implementar 'inscribirse_a_actividad' para correr este test"
            )

        # === ASSERT ===
        self.assertIsInstance(
            resultado, str,
            "La función debe devolver un string con formato JSON"
        )

        try:
            parsed = json.loads(resultado)
        except json.JSONDecodeError:
            self.fail("La respuesta no tiene un formato JSON válido")

        self.assertIn(
            'exito', parsed, "El resultado debe incluir la clave 'exito'"
        )
        self.assertIn(
            'mensaje', parsed, "El resultado debe incluir la clave 'mensaje'"
        )

        # --- Verifica que la inscripción fue exitosa ---
        self.assertTrue(
            parsed['exito'],
            (f"La inscripción falló cuando debería haber sido "
             f"exitosa. Mensaje: {parsed.get('mensaje')}")
        )

        self.assertEqual(
            parsed['mensaje'],
            "Inscripción exitosa",
            "El mensaje de éxito no coincide con lo esperado"
        )

        # --- Verifica que se generó un ID de inscripción ---
        self.assertIn(
            'idInscripcion', parsed,
            "Debe incluir 'idInscripcion' cuando la inscripción es exitosa"
        )
        self.assertIsNotNone(
            parsed['idInscripcion'], "El 'idInscripcion' no debe ser None"
        )


if __name__ == "__main__":
    unittest.main()