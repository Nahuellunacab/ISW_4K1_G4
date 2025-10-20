import unittest
import json
import sys
import os

# Agregar el directorio src al path para importar el módulo
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
)

from inscribirse_actividad import inscribirse_a_actividad

class TestInscripcionActividad(unittest.TestCase):

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

        self.assertIn('exito', parsed, "El resultado debe incluir la clave 'exito'")
        self.assertIn('mensaje', parsed, "El resultado debe incluir la clave 'mensaje'")

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
                "No debería generarse 'idInscripcion' cuando la inscripción falla"
            )

    # ============================================================
    # TEST 2: Sin ingresar talle de vestimenta requerido (FALLA)
    # ============================================================

    def test_inscribirse_sin_talle_requerido(self):
        """
        Caso de prueba (TDD):
        Verificar que NO se permite la inscripción a una actividad que requiere
        vestimenta (Palestra o Tirolesa) si no se proporciona 'tallaVestimenta'.
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

    # ============================================================
    # TEST 3: Sin cupo disponible (FALLA)
    # ============================================================

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
    # TEST 4: Inscripción con edad menor al límite requerido (FALLA) - TDD
    # ============================================================
    
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
    # TEST 5: Inscripción exitosa con todos los datos correctos (PASA)
    # ============================================================
    
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
            'horario': '11:00 GMT-3',  # Horario con cupos disponibles
            'personas': [
                {
                    'nombre': 'Julian',
                    'tallaVestimenta': 'M',  # Talla proporcionada para actividad que lo requiere
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

        # --- Verifica que la inscripción fue exitosa ---
        self.assertTrue(
            parsed['exito'],
            f"La inscripción falló cuando debería haber sido exitosa. Mensaje: {parsed.get('mensaje')}"
        )

        self.assertEqual(
            parsed['mensaje'],
            "Inscripción exitosa",
            "El mensaje de éxito no coincide con lo esperado"
        )

        # --- Verifica que se generó un ID de inscripción ---
        self.assertIn('idInscripcion', parsed, "Debe incluir 'idInscripcion' cuando la inscripción es exitosa")
        self.assertIsNotNone(parsed['idInscripcion'], "El 'idInscripcion' no debe ser None")
        self.assertNotEqual(parsed['idInscripcion'], "", "El 'idInscripcion' no debe estar vacío")

    # ============================================================
    # TEST 6: Inscripción a actividad que NO requiere vestimenta (PASA)
    # ============================================================
    
    def test_inscribirse_a_actividad_sin_requerir_vestimenta(self):
        """
        Caso de prueba (TDD):
        Verificar que se puede inscribir a actividades que NO requieren
        talla de vestimenta (Safari, Jardinería) sin proporcionar talla.
        """
        # === PRECONDICIONES ===
        payload = {
            'actividad': 'Safari',  # NO requiere vestimenta
            'cantidadPersonas': 1,
            'horario': '14:00 GMT-3',  # Horario con cupo disponible
            'personas': [
                {
                    'nombre': 'Maria',
                    'tallaVestimenta': None,  # No se proporciona talla (no es necesaria)
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
            self.skipTest("Implementar 'inscribirse_a_actividad' para correr este test")

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
            f"La inscripción debió ser exitosa, pero falló con: {parsed.get('mensaje')}"
        )
        self.assertEqual(parsed.get('mensaje'), "Inscripción exitosa")
        self.assertIsNotNone(parsed.get('idInscripcion'), "Debe generarse un idInscripcion")

    # ============================================================
    # TEST 7: Inscripción en horario no disponible/parque cerrado (FALLA)
    # ============================================================
    
    def test_inscribirse_en_horario_no_disponible_debe_fallar(self):
        """
        Caso de prueba (TDD):
        Verificar que NO se permite la inscripción cuando se selecciona
        un horario en el cual el parque está cerrado o la actividad no está disponible.
        """
        # === PRECONDICIONES ===
        payload = {
            'actividad': 'Tirolesa',
            'cantidadPersonas': 1,
            'horario': '22:00 GMT-3',  # Horario fuera del rango disponible (parque cerrado)
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

        # --- Verifica que la inscripción fue rechazada ---
        self.assertFalse(
            parsed['exito'],
            "Se permitió la inscripción en horario no disponible/parque cerrado"
        )

        # El mensaje puede ser sobre falta de cupo o horario no disponible
        mensaje_lower = parsed['mensaje'].lower()
        self.assertTrue(
            "cupo" in mensaje_lower or "horario" in mensaje_lower or "disponible" in mensaje_lower,
            f"El mensaje '{parsed['mensaje']}' debe mencionar la falta de disponibilidad"
        )

        if 'idInscripcion' in parsed:
            self.assertIsNone(
                parsed['idInscripcion'],
                "No debería generarse 'idInscripcion' cuando la inscripción falla"
            )

    # ============================================================
    # TEST 8: Inscripción con múltiples personas válidas (PASA)
    # ============================================================
    
    def test_inscribirse_con_multiples_personas_validas(self):
        """
        Caso de prueba (TDD):
        Verificar que se puede inscribir múltiples personas cuando todos 
        los datos son válidos y hay cupo suficiente.
        """
        # === PRECONDICIONES ===
        payload = {
            'actividad': 'Tirolesa',  # Requiere vestimenta y edad mínima 8 años
            'cantidadPersonas': 2,
            'horario': '10:00 GMT-3',  # Horario con cupo disponible
            'personas': [
                {
                    'nombre': 'Ana',
                    'tallaVestimenta': 'M',
                    'edad': 25,
                    'DNI': '30123456'
                },
                {
                    'nombre': 'Pedro',
                    'tallaVestimenta': 'L', 
                    'edad': 18,
                    'DNI': '31987654'
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

        # --- Verifica que la inscripción fue exitosa ---
        self.assertTrue(
            parsed['exito'],
            f"La inscripción múltiple falló cuando debería haber sido exitosa. Mensaje: {parsed.get('mensaje')}"
        )

        self.assertEqual(
            parsed['mensaje'],
            "Inscripción exitosa",
            "El mensaje de éxito no coincide con lo esperado"
        )

        # --- Verifica que se generó un ID de inscripción ---
        self.assertIn('idInscripcion', parsed, "Debe incluir 'idInscripcion' cuando la inscripción es exitosa")
        self.assertIsNotNone(parsed['idInscripcion'], "El 'idInscripcion' no debe ser None")


if __name__ == "__main__":
    unittest.main()