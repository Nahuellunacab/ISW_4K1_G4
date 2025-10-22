# Guía de Estilo PEP-8 para Python

## Introducción

PEP-8 es la guía de estilo oficial para escribir código Python. Establece convenciones para mejorar la legibilidad y consistencia del código.

---

## 1. Indentación

**Regla:** Usar 4 espacios por nivel de indentación.

### ✅ Ejemplo Correcto (del proyecto)
```python
def inscribirse_a_actividad(payload: Dict[str, Any]) -> str:
    """
    Procesa la inscripción a una actividad del parque.
    """
    validaciones = [
        _validar_terminos_condiciones,
        _validar_talla_vestimenta,
        _validar_edad_minima,
    ]
    
    for validacion in validaciones:
        error = validacion(payload)
        if error:
            return error.to_json()
```

### ❌ Ejemplo Incorrecto
```python
def inscribirse_a_actividad(payload):
  # Solo 2 espacios
  validaciones = [
      _validar_terminos_condiciones,
  ]
```

---

## 2. Longitud de Línea

**Regla:** Limitar las líneas a 79 caracteres para código y 72 para docstrings.

### ✅ Ejemplo Correcto (del proyecto)
```python
def agregar_inscripcion(
    self, actividad: str, horario: str, persona: Dict[str, Any]
):
    query = """
    INSERT INTO inscripciones (actividad_id, horario_id, 
                               nombre_persona, talla_vestimenta, edad, dni)
    VALUES (...)
    """
```

### ❌ Ejemplo Incorrecto
```python
def agregar_inscripcion(self, actividad: str, horario: str, persona: Dict[str, Any]):
    # Línea demasiado larga (más de 79 caracteres)
```

---

## 3. Líneas en Blanco

**Regla:** 
- 2 líneas en blanco entre funciones de nivel superior y definiciones de clases
- 1 línea en blanco entre métodos dentro de una clase

### ✅ Ejemplo Correcto (del proyecto)
```python
# =============================
# Constantes de configuración
# =============================
ACTIVIDADES_CON_VESTIMENTA = ['Palestra', 'Tirolesa']
TALLES_VALIDOS = ['XS', 'S', 'M', 'L', 'XL', 'XXL']


# =============================
# Clase Resultado
# =============================
class ResultadoInscripcion:
    """Clase para encapsular el resultado de una inscripción."""

    def __init__(self, exito: bool, mensaje: str, id_inscripcion: str = None):
        self.exito = exito
        self.mensaje = mensaje
        self.id_inscripcion = id_inscripcion

    def to_json(self) -> str:
        """Convierte el resultado a formato JSON."""
        return json.dumps({
            "exito": self.exito,
            "mensaje": self.mensaje,
            "idInscripcion": self.id_inscripcion
        })
```

---

## 4. Importaciones

**Reglas:**
- Importaciones en líneas separadas
- Orden: biblioteca estándar, terceros, locales
- Agrupar por tipo y separar con línea en blanco

### ✅ Ejemplo Correcto (del proyecto)
```python
import json
import sqlite3
from typing import Dict, Any, List
from datetime import datetime, time
```

### ❌ Ejemplo Incorrecto
```python
import json, sqlite3  # Múltiples importaciones en una línea
from datetime import *  # Evitar importaciones con *
```

---

## 5. Espacios en Blanco

**Regla:** Evitar espacios extraños alrededor de paréntesis, corchetes y antes de comas.

### ✅ Ejemplo Correcto (del proyecto)
```python
LIMITES_EDAD = {
    'Palestra': 12,
    'Tirolesa': 8,
    'Safari': 0,
    'Jardineria': 0
}

personas = payload.get('personas', [])
```

### ❌ Ejemplo Incorrecto
```python
LIMITES_EDAD = { 'Palestra' : 12 , 'Tirolesa' : 8 }
personas = payload.get( 'personas' , [ ] )
```

---

## 6. Nombres de Variables y Funciones

**Regla:** Usar snake_case para funciones y variables, PascalCase para clases.

### ✅ Ejemplo Correcto (del proyecto)
```python
# Clases: PascalCase
class ResultadoInscripcion:
    pass

class RepositorioActividadesSQLite:
    pass

# Funciones y variables: snake_case
def inscribirse_a_actividad(payload):
    pass

def _validar_terminos_condiciones(payload):
    pass

cantidad_personas = payload.get('cantidadPersonas', 1)
limite_edad = LIMITES_EDAD.get(actividad, 0)
```

### ❌ Ejemplo Incorrecto
```python
# Nombres no convencionales
class resultadoInscripcion:  # Debería ser PascalCase
    pass

def InscribirseActividad(payload):  # Debería ser snake_case
    pass

CantidadPersonas = 5  # Variables deberían usar snake_case
```

---

## 7. Constantes

**Regla:** Usar MAYÚSCULAS_CON_GUIONES_BAJOS para constantes.

### ✅ Ejemplo Correcto (del proyecto)
```python
ACTIVIDADES_CON_VESTIMENTA = ['Palestra', 'Tirolesa']
TALLES_VALIDOS = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
HORA_APERTURA_PARQUE = time(9, 0)
HORA_CIERRE_PARQUE = time(19, 0)
MSG_ERROR_TERMINOS = "Debe aceptar Términos y Condiciones"
MSG_ERROR_TALLA_REQUERIDA = "La actividad requiere talla de vestimenta"
```

---

## 8. Docstrings

**Regla:** Usar docstrings para documentar módulos, clases, funciones y métodos.

### ✅ Ejemplo Correcto (del proyecto)
```python
def inscribirse_a_actividad(payload: Dict[str, Any]) -> str:
    """
    Procesa la inscripción a una actividad del parque.
    """
    pass

class ResultadoInscripcion:
    """Clase para encapsular el resultado de una inscripción."""
    
    def to_json(self) -> str:
        """Convierte el resultado a formato JSON."""
        pass
```

### ❌ Ejemplo Incorrecto
```python
def inscribirse_a_actividad(payload):
    # Solo comentario, no docstring
    pass
```

---

## 9. Anotaciones de Tipo (Type Hints)

**Regla:** Usar anotaciones de tipo para mejorar la legibilidad y detección de errores.

### ✅ Ejemplo Correcto (del proyecto)
```python
def __init__(self, exito: bool, mensaje: str, id_inscripcion: str = None):
    self.exito = exito
    self.mensaje = mensaje
    self.id_inscripcion = id_inscripcion

def to_json(self) -> str:
    """Convierte el resultado a formato JSON."""
    return json.dumps({...})

def obtener_cupos(self, actividad: str, horario: str) -> int:
    query = "..."
    return row[0] if row else 0

def hay_cupo(self, actividad: str, horario: str, cantidad: int) -> bool:
    cupos = self.obtener_cupos(actividad, horario)
    return cupos >= cantidad
```

---

## 10. Operadores

**Regla:** Rodear operadores binarios con un espacio a cada lado.

### ✅ Ejemplo Correcto (del proyecto)
```python
if not payload.get('aceptoTerminosYCondiciones', False):
    return ResultadoInscripcion(False, MSG_ERROR_TERMINOS)

if edad < limite_edad:
    return ResultadoInscripcion(False, mensaje_error)

return cupos >= cantidad
```

### ❌ Ejemplo Incorrecto
```python
if edad<limite_edad:  # Falta espacio
    pass

return cupos>=cantidad  # Falta espacio
```

---

## 11. Comentarios

**Regla:** Los comentarios deben ser frases completas y estar actualizados.

### ✅ Ejemplo Correcto (del proyecto)
```python
# =============================
# Constantes de configuración
# =============================

# Horario del parque
HORA_APERTURA_PARQUE = time(9, 0)
HORA_CIERRE_PARQUE = time(19, 0)

# Actividades: de 9:00 a 18:00 hs, con turnos de 30 minutos

# Límites de edad según Product Owner
LIMITES_EDAD = {
    'Palestra': 12,
    'Tirolesa': 8,
    'Safari': 0,      # Sin límite
    'Jardineria': 0   # Sin límite
}
```

---

## 12. Manejo de Excepciones

**Regla:** Ser específico con las excepciones, evitar capturar todas.

### ✅ Ejemplo Correcto (del proyecto)
```python
def _validar_horario_parque(payload: Dict[str, Any]) -> ResultadoInscripcion:
    """Valida que la inscripción se realice dentro del horario de apertura."""
    try:
        horario_str = payload.get('horario', '').split(' ')[0]
        if not horario_str:
            return None
        horario_inscripcion = datetime.strptime(horario_str, '%H:%M').time()
    except ValueError:
        # Si el formato es inválido, otra validación podría encargarse
        return None
```

### ❌ Ejemplo Incorrecto
```python
try:
    horario_inscripcion = datetime.strptime(horario_str, '%H:%M').time()
except:  # Muy genérico, no especifica el tipo de excepción
    pass
```

---

## 13. Comparaciones

**Regla:** Usar `is` / `is not` para comparar con None, usar `not` para valores booleanos.

### ✅ Ejemplo Correcto (del proyecto)
```python
if not payload.get('aceptoTerminosYCondiciones', False):
    return ResultadoInscripcion(False, MSG_ERROR_TERMINOS)

talla = persona.get('tallaVestimenta')
if not talla:
    return ResultadoInscripcion(False, MSG_ERROR_TALLA_REQUERIDA)

if limite_edad == 0:
    return None
```

### ❌ Ejemplo Incorrecto
```python
if payload.get('aceptoTerminosYCondiciones') == False:  # Usar not
    pass

if talla == None:  # Usar is None
    pass
```

---

## 14. Estructuras de Datos

**Regla:** Usar comprensiones de listas cuando sea apropiado, mantener legibilidad.

### ✅ Ejemplo Correcto
```python
# Lista de validaciones clara y legible
validaciones = [
    _validar_terminos_condiciones,
    _validar_talla_vestimenta,
    _validar_edad_minima,
    _validar_horario_parque,
    _validar_horario_existente,
    _validar_cupo_disponible
]

# Iteración clara
for validacion in validaciones:
    error = validacion(payload)
    if error:
        return error.to_json()
```

---

## 15. Tests con Unittest

**Regla:** Nombres descriptivos de tests y uso apropiado de assertions.

### ✅ Ejemplo Correcto (del proyecto)
```python
class TestInscripcionActividad(unittest.TestCase):
    """Tests para verificar la funcionalidad de inscripción a actividades."""

    def test_inscribirse_sin_aceptar_terminos_debe_fallar(self):
        """
        Caso de prueba (TDD):
        Verificar que NO se permite la inscripción a una actividad
        si 'aceptoTerminosYCondiciones' es False.
        """
        # === PRECONDICIONES ===
        payload = {...}

        # === ACT ===
        resultado = inscribirse_a_actividad(payload)

        # === ASSERT ===
        self.assertIsInstance(resultado, str)
        self.assertFalse(parsed['exito'])
```

---

## Resumen de Beneficios

1. **Legibilidad:** Código más fácil de leer y entender
2. **Mantenibilidad:** Más sencillo de modificar y extender
3. **Colaboración:** Estilo consistente en todo el equipo
4. **Profesionalismo:** Código que sigue estándares de la industria
5. **Menos errores:** Buenas prácticas reducen bugs comunes

---

## Referencias

- [PEP 8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [PEP 257 - Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
- [PEP 484 - Type Hints](https://www.python.org/dev/peps/pep-0484/)
