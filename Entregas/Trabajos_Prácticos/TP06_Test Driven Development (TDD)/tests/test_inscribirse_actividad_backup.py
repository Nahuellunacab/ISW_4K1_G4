import unittest
import json
import sys
import os

# Agregar el directorio src al path para importar el módulo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from inscribirse_actividad import inscribirse_a_actividad

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
    # TEST 3: Sin ingresar talle de vestimenta requerido (FALLA)
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
        mensaje_esperado = "No hay cupos disponibles para el horario seleccionado"

        # === ACT & ASSERT ===
        self._verificar_inscripcion_fallida(payload, mensaje_esperado)


    # ============================================================
    # TEST 4: Inscripción con edad menor al límite requerido (FALLA) - TDD RED
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
    # TEST 4: Inscripción exitosa con todos los datos correctos (PASA)
    # ============================================================
    
    def test_inscribirse_exitosamente_con_todos_los_datos_correctos(self):
        """
        Caso de prueba (TDD):
        Verificar que se permite la inscripción cuando todos los datos
        son válidos y hay cupo disponible.
        Cubre: "Probar inscribirse a una actividad del listado que poseen cupos disponibles,
        seleccionando un horario, ingresando los datos del visitante y aceptando términos (pasa)"
        """
        # === PRECONDICIONES ===
        payload = {
            'actividad': 'Tirolesa',  
            'cantidadPersonas': 1,
            'horario': '11:00 GMT-3',  # Nuevo horario con 15 cupos disponibles
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
            "La inscripción falló cuando debería haber sido exitosa"
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

        # === RESULT ===
        print(resultado)
        print("- La prueba de inscripción exitosa ha PASADO")


    # ============================================================
    # TEST 5: Inscripción a actividad que NO requiere vestimenta (PASA)
    # ============================================================
    
    def test_inscribirse_a_actividad_sin_requerir_vestimenta(self):
        """
        Caso de prueba (TDD):
        Verificar que se puede inscribir a actividades que NO requieren
        talla de vestimenta (Safari, Jardinería) sin proporcionar talla.
        Cubre: "Probar inscribirse a una actividad sin ingresar talle de vestimenta 
        porque la actividad no lo requiere (pasa)"
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


    @patch('src.inscribirse_actividad.repositorio')
    def test_inscribirse_a_una_actividad_en_horario_disponible_debe_pasar(self, mock_repositorio):
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
    # TEST 7: Inscripción con múltiples personas válidas (PASA)
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
            'horario': '10:00 GMT-3',  # Horario con cupo disponible (ahora 10 cupos)
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
            "La inscripción múltiple falló cuando debería haber sido exitosa"
        )

        self.assertEqual(
            parsed['mensaje'],
            "Inscripción exitosa",
            "El mensaje de éxito no coincide con lo esperado"
        )

        # --- Verifica que se generó un ID de inscripción ---
        self.assertIn('idInscripcion', parsed, "Debe incluir 'idInscripcion' cuando la inscripción es exitosa")
        self.assertIsNotNone(parsed['idInscripcion'], "El 'idInscripcion' no debe ser None")

        # === RESULT ===
        print(resultado)
        print("- La prueba de inscripción múltiple exitosa ha PASADO")


    @patch('src.inscribirse_actividad.repositorio')
    def test_inscribirse_con_cupo_y_horario_validos_debe_pasar(self, mock_repositorio):
        """
        Caso de prueba (Unitario):
        Verificar que se permite la inscripción a una actividad
        cuando el repositorio confirma que hay cupo y el horario es válido.
        """
        # 1. Arrange: Configurar el mock para simular el escenario exitoso.
        mock_repositorio.horario_existe.return_value = True
        mock_repositorio.hay_cupo.return_value = True
        
        payload = {
            'actividad': 'Jardineria',
            'cantidadPersonas': 2,
            'horario': '15:00 GMT-3',
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

        # 2. Act: Llamar a la función bajo prueba.
        resultado = inscribirse_a_actividad(payload)

        # 3. Assert: Verificar el resultado exitoso.
        self.assertIsInstance(resultado, str, "La función debe devolver un string con formato JSON")

        try:
            parsed = json.loads(resultado)
        except json.JSONDecodeError:
            self.fail("La respuesta no tiene un formato JSON válido")

        self.assertTrue(parsed.get('exito'), "La inscripción debería haber sido exitosa.")
        self.assertEqual(parsed.get('mensaje'), "Inscripción exitosa")
        self.assertIn('idInscripcion', parsed, "Debe incluir la clave 'idInscripcion' en caso de éxito")
        self.assertIsNotNone(parsed.get('idInscripcion'), "Se debe generar un 'idInscripcion' válido.")

        # 4. Assert de Interacciones: Verificar que se llamó a la base de datos como se esperaba.
        self.assertEqual(
            mock_repositorio.agregar_inscripcion.call_count,
            payload['cantidadPersonas'],
            "Se esperaba una llamada a agregar_inscripcion por cada persona"
        )
        mock_repositorio.descontar_cupo.assert_called_once_with(
            'Jardineria', '15:00 GMT-3', 2
        )

if __name__ == "__main__":
    unittest.main()
    
