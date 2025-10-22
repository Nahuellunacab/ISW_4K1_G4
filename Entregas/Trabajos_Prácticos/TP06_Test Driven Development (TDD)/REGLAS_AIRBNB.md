# Guía de Estilo Airbnb para JavaScript/TypeScript

## Introducción

La guía de estilo de Airbnb es una de las más populares y ampliamente adoptadas para JavaScript y TypeScript. Establece convenciones para escribir código limpio, consistente y mantenible.

---

## 1. Declaración de Variables

**Regla:** Usar `const` para valores que no cambian, `let` para valores mutables. Evitar `var`.

### ✅ Ejemplo Correcto (adaptado del proyecto)
```javascript
// Constantes de configuración
const ACTIVIDADES_CON_VESTIMENTA = ['Palestra', 'Tirolesa'];
const TALLES_VALIDOS = ['XS', 'S', 'M', 'L', 'XL', 'XXL'];
const HORA_APERTURA_PARQUE = '09:00';
const HORA_CIERRE_PARQUE = '19:00';

// Variable que puede cambiar
let cuposDisponibles = 10;
let edadPersona = 21;
```

### ❌ Ejemplo Incorrecto
```javascript
var ACTIVIDADES_CON_VESTIMENTA = ['Palestra', 'Tirolesa'];  // Usar const
var cuposDisponibles = 10;  // Usar let
```

---

## 2. Objetos

**Regla:** Usar sintaxis literal para crear objetos. Usar shorthand para propiedades y métodos.

### ✅ Ejemplo Correcto (adaptado del proyecto)
```javascript
// Literal de objeto
const payload = {
  actividad: 'Palestra',
  cantidadPersonas: 1,
  horario: '09:30 GMT-3',
  personas: [],
  aceptoTerminosYCondiciones: true
};

// Property shorthand
const nombre = 'Julian';
const edad = 21;
const dni = '44152639';

const persona = {
  nombre,
  edad,
  dni,
  tallaVestimenta: 'M'
};

// Method shorthand
const resultado = {
  exito: true,
  mensaje: 'Inscripción exitosa',
  
  toJSON() {  // En lugar de toJSON: function()
    return JSON.stringify(this);
  }
};
```

### ❌ Ejemplo Incorrecto
```javascript
const payload = new Object();  // No usar new Object()

const persona = {
  nombre: nombre,  // No usar redundancia, usar shorthand
  edad: edad
};

const resultado = {
  toJSON: function() {  // Usar method shorthand
    return JSON.stringify(this);
  }
};
```

---

## 3. Arrays

**Regla:** Usar sintaxis literal para crear arrays. Usar métodos de array (map, filter, reduce).

### ✅ Ejemplo Correcto (adaptado del proyecto)
```javascript
// Literal de array
const validaciones = [
  validarTerminosCondiciones,
  validarTallaVestimenta,
  validarEdadMinima,
  validarHorarioParque
];

// Métodos de array
const personas = payload.personas;
const tallasValidas = personas
  .map(persona => persona.tallaVestimenta)
  .filter(talla => talla !== null);

// Encontrar persona con edad inválida
const personaMenor = personas.find(persona => 
  persona.edad < LIMITES_EDAD[actividad]
);

// Verificar si todas las personas tienen talla
const todasTienenTalla = personas.every(persona => 
  persona.tallaVestimenta !== null
);
```

### ❌ Ejemplo Incorrecto
```javascript
const validaciones = new Array();  // Usar literal []

// Usar for loop en lugar de métodos de array
const tallasValidas = [];
for (let i = 0; i < personas.length; i++) {
  if (personas[i].tallaVestimenta !== null) {
    tallasValidas.push(personas[i].tallaVestimenta);
  }
}
```

---

## 4. Desestructuración

**Regla:** Usar desestructuración para acceder a propiedades de objetos y arrays.

### ✅ Ejemplo Correcto (adaptado del proyecto)
```javascript
// Desestructuración de objetos
const { actividad, horario, personas, aceptoTerminosYCondiciones } = payload;
const { nombre, edad, dni, tallaVestimenta } = personas[0];

// Con valores por defecto
const { cantidadPersonas = 1 } = payload;

// Desestructuración en parámetros
function validarEdadMinima({ actividad, personas }) {
  const limiteEdad = LIMITES_EDAD[actividad];
  // ...
}

// Desestructuración de arrays
const [primerPersona, segundaPersona] = personas;
```

### ❌ Ejemplo Incorrecto
```javascript
const actividad = payload.actividad;
const horario = payload.horario;
const personas = payload.personas;

function validarEdadMinima(payload) {
  const actividad = payload.actividad;
  const personas = payload.personas;
  // ...
}
```

---

## 5. Strings

**Regla:** Usar template strings (backticks) para interpolación y strings multilínea.

### ✅ Ejemplo Correcto (adaptado del proyecto)
```javascript
// Template strings para interpolación
const MSG_ERROR_EDAD_INSUFICIENTE = (limite) => 
  `Edad insuficiente para la actividad. Mínimo requerido: ${limite} años`;

const mensajeError = `No hay cupos disponibles para ${actividad} a las ${horario}`;

// Strings multilínea
const query = `
  SELECT cupos_disponibles
  FROM horarios
  JOIN actividades ON horarios.actividad_id = actividades.id
  WHERE actividades.nombre = ? AND horarios.hora = ?
`;

// Logging descriptivo
console.log(`Inscribiendo a ${personas.length} personas en ${actividad}`);
```

### ❌ Ejemplo Incorrecto
```javascript
const mensajeError = 'No hay cupos disponibles para ' + actividad + 
                     ' a las ' + horario;  // Usar template strings

const query = 'SELECT cupos_disponibles' +
              'FROM horarios' +
              'WHERE actividades.nombre = ?';  // Usar template strings
```

---

## 6. Funciones

**Regla:** Usar arrow functions para funciones anónimas. Nombrar funciones expresivas.

### ✅ Ejemplo Correcto (adaptado del proyecto)
```javascript
// Arrow functions
const validarTerminosCondiciones = (payload) => {
  if (!payload.aceptoTerminosYCondiciones) {
    return { exito: false, mensaje: MSG_ERROR_TERMINOS };
  }
  return null;
};

// Arrow function con retorno implícito
const obtenerLimiteEdad = (actividad) => LIMITES_EDAD[actividad] || 0;

// Usar arrow function en callbacks
const errores = validaciones
  .map(validacion => validacion(payload))
  .filter(resultado => resultado !== null);

// Funciones con nombres descriptivos
const inscribirseAActividad = (payload) => {
  const validaciones = [
    validarTerminosCondiciones,
    validarTallaVestimenta,
    validarEdadMinima
  ];
  
  for (const validacion of validaciones) {
    const error = validacion(payload);
    if (error) return error;
  }
  
  return { exito: true, mensaje: 'Inscripción exitosa' };
};
```

### ❌ Ejemplo Incorrecto
```javascript
// No usar function para funciones simples
const validar = function(payload) {
  return payload.aceptoTerminosYCondiciones;
};

// Función mal nombrada
const f = (p) => {  // Nombres no descriptivos
  return p.edad > 18;
};
```

---

## 7. Arrow Functions y 'this'

**Regla:** Usar arrow functions para preservar el contexto de `this`.

### ✅ Ejemplo Correcto (adaptado del proyecto)
```javascript
class ResultadoInscripcion {
  constructor(exito, mensaje, idInscripcion = null) {
    this.exito = exito;
    this.mensaje = mensaje;
    this.idInscripcion = idInscripcion;
  }
  
  toJSON() {
    return JSON.stringify({
      exito: this.exito,
      mensaje: this.mensaje,
      idInscripcion: this.idInscripcion
    });
  }
  
  validarYProcesar() {
    // Arrow function preserva 'this'
    setTimeout(() => {
      console.log(this.mensaje);
    }, 1000);
  }
}
```

---

## 8. Clases y Constructores

**Regla:** Usar sintaxis de `class` para programación orientada a objetos.

### ✅ Ejemplo Correcto (adaptado del proyecto)
```javascript
class RepositorioActividadesSQLite {
  constructor(dbPath = 'actividades.db') {
    this.dbPath = dbPath;
    this.crearTablas();
    this.precargarDatosIniciales();
  }
  
  crearTablas() {
    // Lógica para crear tablas
  }
  
  obtenerCupos(actividad, horario) {
    // Query a la base de datos
    return cupos;
  }
  
  hayCupo(actividad, horario, cantidad) {
    const cupos = this.obtenerCupos(actividad, horario);
    return cupos >= cantidad;
  }
  
  descontarCupo(actividad, horario, cantidad) {
    // Actualizar cupos
  }
}

// Instancia de la clase
const repositorio = new RepositorioActividadesSQLite();
```

### ❌ Ejemplo Incorrecto
```javascript
// No usar funciones constructoras antiguas
function Repositorio(dbPath) {
  this.dbPath = dbPath;
}

Repositorio.prototype.obtenerCupos = function() {
  // ...
};
```

---

## 9. Módulos

**Regla:** Usar sintaxis ES6 de import/export.

### ✅ Ejemplo Correcto (adaptado del proyecto)
```javascript
// inscribirse_actividad.js

// Named exports
export const ACTIVIDADES_CON_VESTIMENTA = ['Palestra', 'Tirolesa'];
export const TALLES_VALIDOS = ['XS', 'S', 'M', 'L', 'XL', 'XXL'];

export class ResultadoInscripcion {
  // ...
}

export const validarTerminosCondiciones = (payload) => {
  // ...
};

// Default export
export default function inscribirseAActividad(payload) {
  // ...
}

// test_inscribirse_actividad.js
import inscribirseAActividad, { 
  ResultadoInscripcion,
  ACTIVIDADES_CON_VESTIMENTA 
} from './inscribirse_actividad';
```

### ❌ Ejemplo Incorrecto
```javascript
// No usar require (CommonJS)
const inscribirseAActividad = require('./inscribirse_actividad');
module.exports = inscribirseAActividad;
```

---

## 10. Comparaciones

**Regla:** Usar `===` y `!==` en lugar de `==` y `!=`.

### ✅ Ejemplo Correcto (adaptado del proyecto)
```javascript
if (payload.aceptoTerminosYCondiciones === false) {
  return { exito: false, mensaje: MSG_ERROR_TERMINOS };
}

if (talla !== null && talla !== undefined) {
  // Validar talla
}

if (limiteEdad === 0) {
  return null;  // Sin límite de edad
}
```

### ❌ Ejemplo Incorrecto
```javascript
if (payload.aceptoTerminosYCondiciones == false) {  // Usar ===
  // ...
}

if (talla != null) {  // Usar !==
  // ...
}
```

---

## 11. Naming Conventions

**Regla:** camelCase para variables y funciones, PascalCase para clases, UPPER_CASE para constantes.

### ✅ Ejemplo Correcto (adaptado del proyecto)
```javascript
// Constantes: UPPER_CASE con guiones bajos
const ACTIVIDADES_CON_VESTIMENTA = ['Palestra', 'Tirolesa'];
const MSG_ERROR_TERMINOS = 'Debe aceptar Términos y Condiciones';
const HORA_APERTURA_PARQUE = '09:00';

// Clases: PascalCase
class ResultadoInscripcion {
  // ...
}

class RepositorioActividadesSQLite {
  // ...
}

// Funciones y variables: camelCase
const inscribirseAActividad = (payload) => {
  const cantidadPersonas = payload.cantidadPersonas;
  const limiteEdad = LIMITES_EDAD[actividad];
  const hayCupoDisponible = repositorio.hayCupo(actividad, horario, cantidad);
  
  return validarInscripcion(payload);
};
```

### ❌ Ejemplo Incorrecto
```javascript
const ActividadesConVestimenta = [];  // Debería ser UPPER_CASE
const MSGerrorTerminos = '';  // Inconsistente

class resultadoInscripcion {  // Debería ser PascalCase
  // ...
}

const InscribirseAActividad = () => {};  // Debería ser camelCase
const cantidad_personas = 5;  // Debería ser camelCase, no snake_case
```

---

## 12. Comentarios

**Regla:** Escribir comentarios claros y útiles. Usar JSDoc para documentar funciones.

### ✅ Ejemplo Correcto (adaptado del proyecto)
```javascript
/**
 * Valida que las personas cumplan con la edad mínima requerida.
 * 
 * Límites según Product Owner:
 * - Palestra: 12 años mínimo
 * - Tirolesa: 8 años mínimo
 * - Safari y Jardinería: sin límite de edad
 * 
 * @param {Object} payload - Datos de la inscripción
 * @param {string} payload.actividad - Nombre de la actividad
 * @param {Array} payload.personas - Lista de personas a inscribir
 * @returns {Object|null} Resultado con error si hay problemas, null si todo está bien
 */
const validarEdadMinima = (payload) => {
  const { actividad, personas } = payload;
  const limiteEdad = LIMITES_EDAD[actividad] || 0;
  
  // Si no hay límite de edad, no validar
  if (limiteEdad === 0) {
    return null;
  }
  
  for (const persona of personas) {
    const { edad } = persona;
    
    // Validar que la edad sea un número válido
    if (typeof edad !== 'number' || edad < 0) {
      return { exito: false, mensaje: MSG_ERROR_EDAD_INVALIDA };
    }
    
    if (edad < limiteEdad) {
      return {
        exito: false,
        mensaje: `Edad insuficiente. Mínimo requerido: ${limiteEdad} años`
      };
    }
  }
  
  return null;
};
```

---

## 13. Manejo de Errores

**Regla:** Usar try-catch para manejar errores de forma apropiada.

### ✅ Ejemplo Correcto (adaptado del proyecto)
```javascript
const validarHorarioParque = (payload) => {
  try {
    const horarioStr = payload.horario.split(' ')[0];
    if (!horarioStr) {
      return null;
    }
    
    const horarioInscripcion = new Date(`1970-01-01T${horarioStr}`);
    const horaApertura = new Date(`1970-01-01T${HORA_APERTURA_PARQUE}`);
    const horaCierre = new Date(`1970-01-01T${HORA_CIERRE_ACTIVIDADES}`);
    
    if (horarioInscripcion < horaApertura || horarioInscripcion >= horaCierre) {
      return { exito: false, mensaje: MSG_ERROR_FUERA_DE_HORARIO };
    }
    
    return null;
  } catch (error) {
    // Manejo específico del error
    console.error('Error al validar horario:', error.message);
    return { exito: false, mensaje: 'Formato de horario inválido' };
  }
};
```

---

## 14. Operador Ternario

**Regla:** Usar operador ternario para asignaciones simples, evitar anidamientos complejos.

### ✅ Ejemplo Correcto (adaptado del proyecto)
```javascript
// Operador ternario simple
const limiteEdad = LIMITES_EDAD[actividad] || 0;
const mensaje = exito ? 'Inscripción exitosa' : 'Error en inscripción';
const idInscripcion = exito ? generarId() : null;

// Valor por defecto
const cantidadPersonas = payload.cantidadPersonas || 1;
const talla = persona.tallaVestimenta || 'No especificada';
```

### ❌ Ejemplo Incorrecto
```javascript
// Ternario anidado complejo (difícil de leer)
const mensaje = exito 
  ? cantidadPersonas > 1 
    ? 'Inscripciones exitosas' 
    : 'Inscripción exitosa'
  : edadInsuficiente 
    ? 'Edad insuficiente' 
    : 'Error desconocido';  // Mejor usar if-else
```

---

## 15. Async/Await

**Regla:** Usar async/await para código asíncrono en lugar de callbacks o then().

### ✅ Ejemplo Correcto (adaptado del proyecto)
```javascript
// Función asíncrona para obtener cupos
const obtenerCuposAsync = async (actividad, horario) => {
  try {
    const query = `
      SELECT cupos_disponibles
      FROM horarios
      WHERE actividades.nombre = ? AND horarios.hora = ?
    `;
    
    const resultado = await db.query(query, [actividad, horario]);
    return resultado.rows[0]?.cupos_disponibles || 0;
  } catch (error) {
    console.error('Error al obtener cupos:', error);
    throw new Error('No se pudieron obtener los cupos disponibles');
  }
};

// Usar async/await en la función principal
const inscribirseAActividadAsync = async (payload) => {
  const validaciones = [
    validarTerminosCondiciones,
    validarTallaVestimenta,
    validarEdadMinima
  ];
  
  for (const validacion of validaciones) {
    const error = validacion(payload);
    if (error) return error;
  }
  
  // Operación asíncrona
  const cuposDisponibles = await obtenerCuposAsync(
    payload.actividad, 
    payload.horario
  );
  
  if (cuposDisponibles < payload.cantidadPersonas) {
    return { exito: false, mensaje: MSG_ERROR_SIN_CUPO };
  }
  
  await registrarInscripcion(payload);
  
  return {
    exito: true,
    mensaje: 'Inscripción exitosa',
    idInscripcion: generarId()
  };
};
```

---

## 16. Tests con Jest/Mocha

**Regla:** Tests descriptivos con estructura clara (Arrange, Act, Assert).

### ✅ Ejemplo Correcto (adaptado del proyecto)
```javascript
describe('InscripcionActividad', () => {
  describe('validarTerminosCondiciones', () => {
    test('debe fallar si no se aceptan términos y condiciones', () => {
      // Arrange - Precondiciones
      const payload = {
        actividad: 'Palestra',
        cantidadPersonas: 1,
        horario: '09:30 GMT-3',
        personas: [
          {
            nombre: 'Julian',
            tallaVestimenta: 'M',
            edad: 21,
            dni: '44152639'
          }
        ],
        aceptoTerminosYCondiciones: false
      };
      
      // Act - Ejecutar función
      const resultado = inscribirseAActividad(payload);
      
      // Assert - Verificar resultado
      expect(resultado.exito).toBe(false);
      expect(resultado.mensaje).toBe('Debe aceptar Términos y Condiciones');
      expect(resultado.idInscripcion).toBeNull();
    });
    
    test('debe permitir inscripción con términos aceptados', () => {
      const payload = {
        actividad: 'Tirolesa',
        cantidadPersonas: 1,
        horario: '10:00 GMT-3',
        personas: [{ nombre: 'Julian', tallaVestimenta: 'M', edad: 21 }],
        aceptoTerminosYCondiciones: true
      };
      
      const resultado = inscribirseAActividad(payload);
      
      expect(resultado.exito).toBe(true);
      expect(resultado.mensaje).toBe('Inscripción exitosa');
      expect(resultado.idInscripcion).not.toBeNull();
    });
  });
});
```

---

## Resumen de Beneficios

1. **Consistencia:** Código uniforme en todo el proyecto
2. **Legibilidad:** Más fácil de leer y entender
3. **Mantenibilidad:** Simplifica actualizaciones y correcciones
4. **Colaboración:** Facilita el trabajo en equipo
5. **Calidad:** Reduce errores comunes y bugs
6. **Escalabilidad:** Código preparado para crecer

---

## Referencias

- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- [Airbnb React/JSX Style Guide](https://github.com/airbnb/javascript/tree/master/react)
- [ESLint Airbnb Config](https://www.npmjs.com/package/eslint-config-airbnb)
