import unittest
import json
import sys
import os

# Agregar el directorio src al path para importar el módulo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

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

        # === RESULT ===
        print(resultado)
        print("- La prueba para rechazar la inscripción a la actividad por no aceptar términos y condiciones ha PASADO")
        

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

if __name__ == "__main__":
    unittest.main()
    
