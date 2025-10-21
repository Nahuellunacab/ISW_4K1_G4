# Estrategia de Pruebas y Documentación de Tests

Siguiendo la metodología **Test-Driven Development (TDD)**, los tests se constituyen como un componente esencial del sistema, tanto para garantizar la calidad del software como para actuar como documentación viva del comportamiento esperado. En este proyecto, la funcionalidad central de **inscripción a actividades** fue diseñada a partir de la redacción previa de casos de prueba, que luego guiaron la implementación de la lógica en el backend.

Cada test implementado representa un escenario derivado de la User Story **“Inscribirme a actividad”**, en el cual se valida un requisito específico. Los tests están desarrollados con el framework estándar `unittest` de Python, lo que asegura la facilidad de ejecución, integración en pipelines de CI/CD y legibilidad para futuros mantenedores. Además, todas las respuestas de la función `inscribirse_a_actividad` se validan en formato **JSON**, lo cual asegura consistencia en la comunicación entre el backend y el frontend.

En cuanto a la **cobertura de pruebas**, se abordaron múltiples dimensiones de validación:

- **Condiciones contractuales:** Se verifica que no se permita la inscripción cuando el usuario no acepta los términos y condiciones.  
- **Requisitos de vestimenta:** En actividades que requieren un talle de vestimenta (ej. Palestra o Tirolesa), el test asegura que el campo sea obligatorio y que la inscripción falle si no se completa.  
- **Gestión de cupos:** Se incluyen casos en los que la inscripción debe fallar por falta de disponibilidad en un horario determinado.  
- **Restricciones por edad:** Se valida que no se permita la inscripción de menores cuando la actividad define un límite mínimo de edad.  
- **Disponibilidad horaria:** Se contemplan casos donde el parque está cerrado o el horario seleccionado no corresponde a la actividad, esperando un rechazo adecuado.  
- **Éxito de inscripción:** Se desarrollaron pruebas positivas en las que todos los datos son correctos y la inscripción debe ser exitosa, generando un identificador único de inscripción (`idInscripcion`).  
- **Múltiples participantes:** Se comprueba la inscripción de más de una persona en actividades con cupo suficiente.  

La implementación de estos tests asegura que tanto los **escenarios de error** como los **escenarios de éxito** estén cubiertos, garantizando así la robustez de la funcionalidad. Cada test cuenta con precondiciones claras (payload de entrada), una acción (ejecución de la función) y un conjunto de aserciones (validación del resultado), lo cual no solo comprueba el funcionamiento correcto del sistema sino que también documenta, en código ejecutable, las reglas de negocio de la aplicación.

En términos de ejecución, las pruebas se pueden correr mediante el siguiente comando:

```bash
python -m unittest discover -s tests
