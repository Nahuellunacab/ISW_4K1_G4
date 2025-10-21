# Estrategia de Pruebas y Documentación de Tests

Siguiendo la metodología **Test-Driven Development (TDD)**, los tests se constituyen como un componente esencial del sistema, tanto para garantizar la calidad del software como para actuar como documentación viva del comportamiento esperado. En este proyecto, la funcionalidad central de **inscripción a actividades** fue diseñada a partir de la redacción previa de casos de prueba, que luego guiaron la implementación de la lógica en el backend.

Cada test implementado representa un escenario derivado de la User Story **“Inscribirme a actividad”**, en el cual se valida un requisito específico. Los tests están desarrollados con el framework estándar `unittest` de Python, lo que asegura la facilidad de ejecución, integración en pipelines de CI/CD y legibilidad para futuros mantenedores. Además, todas las respuestas de la función `inscribirse_a_actividad` se validan en formato **JSON**, lo cual asegura consistencia en la comunicación entre el backend y el frontend.

---

## Historia de Usuario

**Inscribirme a actividad**  
COMO visitante QUIERO inscribirme a una actividad PARA reservar mi lugar en la misma.

---

## Criterios de Aceptación

- Debe requerir seleccionar una actividad del conjunto de actividades disponibles (Tirolesa, Safari, Palestra y Jardinería), siempre y cuando tengan cupos disponibles en el horario elegido.  
- Debe requerir seleccionar el horario dentro de los disponibles.  
- Debe indicar la cantidad de personas que participarán de la actividad.  
- Para cada persona que participa, debe ingresar los datos del visitante: nombre, DNI, edad y talla de vestimenta si la actividad lo demanda.  
- Debe requerir aceptar los términos y condiciones específicos de la actividad.  

---

## Relación entre criterios y pruebas

Los tests fueron diseñados siguiendo **TDD** y se derivan directamente de los criterios de aceptación y pruebas de usuario definidas. Cada prueba implementada valida un requisito específico de la historia de usuario:

### 1. Inscripción exitosa con todos los datos correctos  
- **Test:** `test_inscribirse_exitosamente_con_todos_los_datos_correctos`  
- **Valida:** Selección de actividad, horario válido, datos completos, aceptación de términos.  
- **Resultado esperado:** `exito = True`, mensaje = “Inscripción exitosa”, con `idInscripcion`.  

### 2. Inscripción sin cupo disponible  
- **Test:** `test_inscribirse_sin_cupo_en_horario_seleccionado_debe_fallar`  
- **Valida:** Requisito de cupo.  
- **Resultado esperado:** `exito = False`, mensaje indicando falta de disponibilidad.  

### 3. Inscripción sin requerir talle de vestimenta  
- **Test:** `test_inscribirse_a_actividad_sin_requerir_vestimenta`  
- **Valida:** Actividades que no exigen vestimenta (Safari, Jardinería).  
- **Resultado esperado:** `exito = True`, mensaje = “Inscripción exitosa”, con `idInscripcion`.  

### 4. Inscripción sin aceptar términos y condiciones  
- **Test:** `test_inscribirse_sin_aceptar_terminos_debe_fallar`  
- **Valida:** Aceptación obligatoria de términos.  
- **Resultado esperado:** `exito = False`, mensaje = “Debe aceptar Términos y Condiciones”.  

### 5. Inscripción sin talle de vestimenta requerido  
- **Test:** `test_inscribirse_sin_talle_requerido`  
- **Valida:** Exigencia de talla en Palestra y Tirolesa.  
- **Resultado esperado:** `exito = False`, mensaje mencionando la falta de talla.  

### 6. Inscripción en horario no disponible  
- **Test:** `test_inscribirse_en_horario_no_disponible_debe_fallar`  
- **Valida:** Restricción de horarios válidos.  
- **Resultado esperado:** `exito = False`, mensaje indicando indisponibilidad.  

### 7. Inscripción con múltiples personas válidas  
- **Test:** `test_inscribirse_con_multiples_personas_validas`  
- **Valida:** Inscripción de más de un participante con cupo suficiente.  
- **Resultado esperado:** `exito = True`, mensaje = “Inscripción exitosa”, con `idInscripcion`.  

### 8. Inscripción con edad menor al límite  
- **Test:** `test_inscribirse_con_edad_menor_al_limite_debe_fallar`  
- **Valida:** Restricciones por edad mínima (Palestra 12 años, Tirolesa 8 años).  
- **Resultado esperado:** `exito = False`, mensaje mencionando la edad, sin `idInscripcion`.  

---
## Ejecución de las pruebas

Las pruebas se pueden correr de dos maneras:

1. **Desde la consola**, utilizando el siguiente comando:
   ```bash
   python -m unittest discover -s tests
2. **Desde Visual Studio Code**
    presionando el botón de (play) que aparece en la parte superior de cada archivo de test.