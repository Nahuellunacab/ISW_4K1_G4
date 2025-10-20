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

        # === RESULT ===
        print(resultado)
        print("- La prueba para rechazar inscripción por edad insuficiente ha PASADO")


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
            "Se permitió la inscripción fuera del horario permitido"
        )

        self.assertEqual(
            parsed['mensaje'],
            "Inscripción fuera del horario permitido",
            "El mensaje de error no coincide con lo esperado"
        )

        if 'idInscripcion' in parsed:
            self.assertIsNone(
                parsed['idInscripcion'],
                "No debería generarse 'idInscripcion' cuando la inscripción falla"
            )


    def test_inscribirse_dentro_de_horario_parque_y_actividad_abierto_debe_pasar(self):
        """
        Caso de prueba (TDD):
        Verificar que se permite la inscripción a una actividad
        dentro del horario en el que el parque está abierto y la actividad está disponible.
        """
        # === PRECONDICIONES ===
        payload = {
            'actividad': 'Tirolesa',
            'cantidadPersonas': 2,
            'horario': '11:30 GMT-3',  
            'personas': [
                {
                    'nombre': 'Julian',
                    'tallaVestimenta': 'M',
                    'edad': 21,
                    'DNI': '44152639'
                },
                {
                    'nombre': 'Julio',
                    'tallaVestimenta': 'XL',
                    'edad': 22,
                    'DNI': '41152639'
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
            "Se permitió la inscripción fuera del horario permitido"
        )

        self.assertEqual(
            parsed['mensaje'],
            "Inscripción dentro del horario permitido",
            "El mensaje no coincide con lo esperado"
        )

        if 'idInscripcion' in parsed:
            self.assertIsNotNone(
                parsed['idInscripcion'],
                "Se generó 'idInscripcion' en la inscripción"
            )


if __name__ == "__main__":
    unittest.main()
    