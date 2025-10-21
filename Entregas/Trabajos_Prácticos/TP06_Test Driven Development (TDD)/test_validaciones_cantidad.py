"""Script de prueba para validar las nuevas restricciones de cantidad de personas."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from inscribirse_actividad import inscribirse_a_actividad
import json

print("=" * 80)
print("PRUEBA DE VALIDACIONES DE CANTIDAD DE PERSONAS")
print("=" * 80)

# Test 1: Cantidad = 0 (debe fallar)
print("\n1️⃣ Test: Cantidad = 0")
print("-" * 80)
payload_cero = {
    "actividad": "Safari",
    "horario": "14:00 GMT-3",
    "cantidadPersonas": 0,
    "aceptoTerminosYCondiciones": True,
    "personas": []
}
resultado = json.loads(inscribirse_a_actividad(payload_cero))
print(f"✓ Resultado: {resultado['exito']}")
print(f"  Mensaje: {resultado['mensaje']}")
assert not resultado['exito'], "❌ Debería fallar con cantidad 0"
print("✅ PASS: Rechazó correctamente cantidad 0\n")

# Test 2: Cantidad excede cupos disponibles (debe fallar)
print("2️⃣ Test: Cantidad excede cupos (Safari tiene 8 cupos)")
print("-" * 80)
payload_excede = {
    "actividad": "Safari",
    "horario": "14:00 GMT-3",
    "cantidadPersonas": 100,
    "aceptoTerminosYCondiciones": True,
    "personas": [{"nombre": f"Persona {i}", "edad": 20, "DNI": f"{i}"} for i in range(100)]
}
resultado = json.loads(inscribirse_a_actividad(payload_excede))
print(f"✓ Resultado: {resultado['exito']}")
print(f"  Mensaje: {resultado['mensaje']}")
assert not resultado['exito'], "❌ Debería fallar cuando excede cupos"
assert "excede" in resultado['mensaje'].lower() or "disponibles" in resultado['mensaje'].lower()
print("✅ PASS: Rechazó correctamente cuando excede cupos\n")

# Test 3: Cantidad válida dentro de cupos (debe funcionar)
print("3️⃣ Test: Cantidad válida (1 persona)")
print("-" * 80)
payload_valido = {
    "actividad": "Safari",
    "horario": "14:00 GMT-3",
    "cantidadPersonas": 1,
    "aceptoTerminosYCondiciones": True,
    "personas": [
        {
            "nombre": "Usuario Test",
            "edad": 25,
            "DNI": "12345678"
        }
    ]
}
resultado = json.loads(inscribirse_a_actividad(payload_valido))
print(f"✓ Resultado: {resultado['exito']}")
print(f"  Mensaje: {resultado['mensaje']}")
if resultado['exito']:
    print(f"  ID Inscripción: {resultado['idInscripcion']}")
assert resultado['exito'], "❌ Debería tener éxito con cantidad válida"
print("✅ PASS: Aceptó correctamente cantidad válida\n")

print("=" * 80)
print("✅ TODAS LAS VALIDACIONES PASARON CORRECTAMENTE")
print("=" * 80)
