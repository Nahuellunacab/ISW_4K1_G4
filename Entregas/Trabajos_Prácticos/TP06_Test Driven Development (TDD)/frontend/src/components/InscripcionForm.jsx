import { useState, useEffect } from 'react';
import {
  obtenerActividades,
  obtenerHorarios,
  crearInscripcion,
} from '../services/api';
import { TERMINOS_Y_CONDICIONES } from '../constants/terminos';
import PersonaForm from './PersonaForm';
import './InscripcionForm.css';

function InscripcionForm({ onVolver }) {
  const [actividades, setActividades] = useState([]);
  const [actividadSeleccionada, setActividadSeleccionada] = useState('');
  const [horarios, setHorarios] = useState([]);
  const [horarioSeleccionado, setHorarioSeleccionado] = useState('');
  const [cantidadPersonas, setCantidadPersonas] = useState(1);
  const [personas, setPersonas] = useState([]);
  const [personasErrores, setPersonasErrores] = useState([]);
  const [aceptoTerminos, setAceptoTerminos] = useState(false);
  const [mostrarTerminos, setMostrarTerminos] = useState(false);
  const [cargando, setCargando] = useState(false);
  const [mensaje, setMensaje] = useState(null);
  const [paso, setPaso] = useState(1);
  const nombreRegex = /^[A-Za-zÀ-ÿ\s\-']+$/;
  const dniRegex = /^\d{6,10}$/;

  useEffect(() => {
    cargarActividades();
  }, []);

  useEffect(() => {
    if (actividadSeleccionada) {
      cargarHorarios(actividadSeleccionada);
    }
  }, [actividadSeleccionada]);

  useEffect(() => {
    // Asegurar que el array de personas siempre tenga la longitud solicitada
    setPersonas((prevPersonas) => {
      const nuevasPersonas = Array.from({ length: cantidadPersonas }, (_, i) => ({
        id: i + 1,
        nombre: prevPersonas[i]?.nombre || '',
        tallaVestimenta: prevPersonas[i]?.tallaVestimenta || '',
        edad: prevPersonas[i]?.edad || '',
        DNI: prevPersonas[i]?.DNI || '',
      }));
      return nuevasPersonas;
    });
    // Mantener array de errores en la misma longitud
    setPersonasErrores((prev) => {
      const arr = Array.from({ length: cantidadPersonas }, (_, i) => prev?.[i] || {});
      return arr;
    });
  }, [cantidadPersonas]);

  const cargarActividades = async () => {
    try {
      const response = await obtenerActividades();
      if (response.exito) {
        setActividades(response.actividades);
      }
    } catch (error) {
      setMensaje({
        tipo: 'error',
        texto: 'Error al cargar actividades',
      });
    }
  };

  const cargarHorarios = async (nombreActividad) => {
    try {
      const response = await obtenerHorarios(nombreActividad);
      if (response.exito) {
        setHorarios(response.horarios);
      }
    } catch (error) {
      setMensaje({
        tipo: 'error',
        texto: 'Error al cargar horarios',
      });
    }
  };

  const handleActividadChange = (e) => {
    const actividad = e.target.value;
    setActividadSeleccionada(actividad);
    setHorarioSeleccionado('');
  };

  const actividadRequiereVestimenta = (actividad = actividadSeleccionada) => {
    const actividadObj = actividades.find((a) => a.nombre === actividad);
    return actividadObj?.requiereVestimenta || false;
  };

  const validarPersona = (persona) => {
    const errores = {};
    const nombre = (persona?.nombre || '').toString().trim();
    if (!nombre || !nombreRegex.test(nombre)) {
      errores.nombre = 'Nombre inválido (solo letras, espacios y guiones)';
    }
    const dni = (persona?.DNI || '').toString().trim();
    if (!dni || !dniRegex.test(dni)) {
      errores.DNI = 'DNI inválido (6 a 10 dígitos)';
    }
    const edadVal = persona?.edad === '' ? null : Number(persona?.edad);
    if (edadVal === null || Number.isNaN(edadVal)) {
      errores.edad = 'Edad inválida';
    } else if (edadVal <= 0) {
      errores.edad = 'La edad debe ser mayor a 0';
    }
    if (actividadRequiereVestimenta() && !persona?.tallaVestimenta) {
      errores.tallaVestimenta = 'La actividad requiere talla de vestimenta';
    }
    return errores;
  };

  const validarDuplicadosDNI = (listaPersonas) => {
    const dnis = listaPersonas.map((p) => String(p?.DNI || '').trim());
    const repetidos = dnis.filter((dni, i) => dni && dnis.indexOf(dni) !== i);
    return new Set(repetidos);
  };

  const handlePersonaChange = (index, campo, valor) => {
    const nuevasPersonas = [...personas];
    nuevasPersonas[index] = { ...(nuevasPersonas[index] || {}), [campo]: valor };
    setPersonas(nuevasPersonas);
    // validar en caliente y actualizar errores
    const errores = [...(personasErrores || [])];
    errores[index] = validarPersona(nuevasPersonas[index]);
    const repetidos = validarDuplicadosDNI(nuevasPersonas);
    errores.forEach((e, i) => {
      if (repetidos.has(String(nuevasPersonas[i].DNI).trim()) && nuevasPersonas[i].DNI) {
        errores[i] = { ...(errores[i] || {}), DNI: 'DNI duplicado en el formulario' };
      } else if (errores[i]?.DNI === 'DNI duplicado en el formulario' && !repetidos.has(String(nuevasPersonas[i].DNI).trim())) {
        const copy = { ...(errores[i] || {}) };
        delete copy.DNI;
        errores[i] = copy;
      }
    });
    setPersonasErrores(errores);
  };

  const validarFormulario = () => {
    if (!actividadSeleccionada) {
      setMensaje({ tipo: 'error', texto: 'Debe seleccionar una actividad' });
      return false;
    }

    if (!horarioSeleccionado) {
      setMensaje({ tipo: 'error', texto: 'Debe seleccionar un horario' });
      return false;
    }

    // validar todas las personas con las mismas reglas que el backend
    const errores = personas.map((p) => validarPersona(p));
    const repetidos = validarDuplicadosDNI(personas);
    errores.forEach((err, i) => {
      if (repetidos.has(String(personas[i].DNI).trim()) && personas[i].DNI) {
        errores[i] = { ...(err || {}), DNI: 'DNI duplicado en el formulario' };
      }
    });
    setPersonasErrores(errores);
    const hayErrores = errores.some((e) => e && Object.keys(e).length > 0);
    if (hayErrores) {
      // Construir mensaje representativo por persona
      const resumen = errores
        .map((err, i) => {
          if (!err || Object.keys(err).length === 0) return null;
          const nombre = (personas[i]?.nombre || `Persona ${i + 1}`).toString().trim();
          const detalles = Object.values(err).join(', ');
          return `${i + 1}) ${nombre} — ${detalles}`;
        })
        .filter(Boolean)
        .join('; ');

      const texto = resumen
        ? `Errores en los participantes: ${resumen}`
        : 'Corrija los errores en los datos de las personas';

      setMensaje({ tipo: 'error', texto });
      return false;
    }

    if (!aceptoTerminos) {
      setMensaje({
        tipo: 'error',
        texto: 'Debe aceptar los términos y condiciones',
      });
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validarFormulario()) {
      return;
    }

    setCargando(true);
    setMensaje(null);

    try {
      const datosInscripcion = {
        actividad: actividadSeleccionada,
        cantidadPersonas,
        horario: horarioSeleccionado,
        personas: personas.map((p) => ({
          nombre: p.nombre,
          tallaVestimenta: p.tallaVestimenta || null,
          edad: parseInt(p.edad, 10),
          DNI: p.DNI,
        })),
        aceptoTerminosYCondiciones: aceptoTerminos,
      };

      const response = await crearInscripcion(datosInscripcion);

      if (response.exito) {
        setMensaje({
          tipo: 'exito',
          texto: `¡Inscripción exitosa! ID: ${response.idInscripcion}`,
        });
        // Limpiar formulario después de 3 segundos
        setTimeout(() => {
          resetFormulario();
        }, 3000);
      } else {
        setMensaje({
          tipo: 'error',
          texto: response.mensaje,
        });
      }
    } catch (error) {
      setMensaje({
        tipo: 'error',
        texto: error.response?.data?.mensaje || 'Error al procesar la inscripción',
      });
    } finally {
      setCargando(false);
    }
  };

  const resetFormulario = () => {
    setActividadSeleccionada('');
    setHorarioSeleccionado('');
    setCantidadPersonas(1);
    setPersonas([]);
    setAceptoTerminos(false);
    setPaso(1);
    setMensaje(null);
  };

  const obtenerCuposDisponibles = () => {
    const horario = horarios.find((h) => h.horario === horarioSeleccionado);
    return horario?.cuposDisponibles || 0;
  };

  const avanzarPaso = () => {
    if (paso === 1) {
      if (!actividadSeleccionada || !horarioSeleccionado) {
        setMensaje({
          tipo: 'error',
          texto: 'Seleccione actividad y horario',
        });
        return;
      }

      // Validar cantidad de personas
      if (!cantidadPersonas || cantidadPersonas === 0) {
        setMensaje({
          tipo: 'error',
          texto: 'Debe ingresar al menos 1 persona',
        });
        return;
      }

      const cuposDisponibles = obtenerCuposDisponibles();
      if (cantidadPersonas > cuposDisponibles) {
        setMensaje({
          tipo: 'error',
          texto: `No hay suficientes cupos. Disponibles: ${cuposDisponibles}`,
        });
        return;
      }
    }
    // Si avanzamos desde paso 2 validar los datos de personas antes de permitir paso 3
    if (paso === 2) {
      const errores = personas.map((p) => validarPersona(p));
      const repetidos = validarDuplicadosDNI(personas);
      errores.forEach((err, i) => {
        if (repetidos.has(String(personas[i].DNI).trim()) && personas[i].DNI) {
          errores[i] = { ...(err || {}), DNI: 'DNI duplicado en el formulario' };
        }
      });
      setPersonasErrores(errores);
      const hayErrores = errores.some((e) => e && Object.keys(e).length > 0);
      if (hayErrores) {
        const resumen = errores
          .map((err, i) => {
            if (!err || Object.keys(err).length === 0) return null;
            const nombre = (personas[i]?.nombre || `Persona ${i + 1}`).toString().trim();
            const detalles = Object.values(err).join(', ');
            return `${i + 1}) ${nombre} — ${detalles}`;
          })
          .filter(Boolean)
          .join('; ');

        const texto = resumen
          ? `Corrija los errores en participantes: ${resumen}`
          : 'Corrija los errores en los datos de las personas';

        setMensaje({ tipo: 'error', texto });
        return;
      }
    }

    setPaso(paso + 1);
    setMensaje(null);
  };

  const retrocederPaso = () => {
    setPaso(paso - 1);
    setMensaje(null);
  };

  return (
    <div className="inscripcion-form">
      <div className="form-header">
        <button type="button" className="btn-volver" onClick={onVolver}>
          ← Volver
        </button>
        <h2>Formulario de Inscripción</h2>
        <div className="pasos">
          <span className={paso === 1 ? 'paso-activo' : ''}>
            1. Actividad
          </span>
          <span className={paso === 2 ? 'paso-activo' : ''}>
            2. Personas
          </span>
          <span className={paso === 3 ? 'paso-activo' : ''}>
            3. Confirmar
          </span>
        </div>
      </div>

      {mensaje && (
        <div className={`mensaje mensaje-${mensaje.tipo}`}>
          {mensaje.texto}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        {paso === 1 && (
          <div className="paso-content">
            <div className="form-group">
              <label htmlFor="actividad">
                Actividad *
                <select
                  id="actividad"
                  value={actividadSeleccionada}
                  onChange={handleActividadChange}
                  required
                >
                  <option value="">Seleccione una actividad</option>
                  {actividades.map((actividad) => (
                    <option key={actividad.nombre} value={actividad.nombre}>
                      {actividad.nombre}
                      {actividad.requiereVestimenta && ' (requiere talla)'}
                    </option>
                  ))}
                </select>
              </label>
            </div>

            <div className="form-group">
              <label htmlFor="horario">
                Horario *
                <select
                  id="horario"
                  value={horarioSeleccionado}
                  onChange={(e) => setHorarioSeleccionado(e.target.value)}
                  disabled={!actividadSeleccionada}
                  required
                >
                  <option value="">Seleccione un horario</option>
                  {horarios.map((horario) => {
                    const sinCupos = !horario.cuposDisponibles || horario.cuposDisponibles === 0;
                    return (
                      <option
                        key={horario.horario}
                        value={horario.horario}
                        disabled={sinCupos}
                        className={sinCupos ? 'opcion-sin-cupos' : ''}
                        title={sinCupos ? 'Sin cupos disponibles' : `${horario.cuposDisponibles} cupos disponibles`}
                      >
                        {horario.horario} ({horario.cuposDisponibles} cupos)
                      </option>
                    );
                  })}
                </select>
              </label>
            </div>

            <div className="form-group">
              <label htmlFor="cantidadPersonas">
                Cantidad de Personas *
                <input
                  id="cantidadPersonas"
                  type="number"
                  min="1"
                  max={horarioSeleccionado ? obtenerCuposDisponibles() : 10}
                  value={cantidadPersonas}
                  onChange={(e) => {
                    const valor = parseInt(e.target.value, 10);
                    if (valor >= 1) {
                      setCantidadPersonas(valor);
                    }
                  }}
                  disabled={!horarioSeleccionado}
                  required
                />
                {horarioSeleccionado && (
                  <small className="helper-text">
                    Cupos disponibles: {obtenerCuposDisponibles()}
                  </small>
                )}
              </label>
            </div>

            <button type="button" className="btn-siguiente" onClick={avanzarPaso}>
              Siguiente →
            </button>
          </div>
        )}

        {paso === 2 && (
          <div className="paso-content">
            <h3>
              Datos de los Participantes (
              {cantidadPersonas}
              )
            </h3>
            {personas.map((persona, index) => (
              <PersonaForm
                key={persona.id}
                persona={persona}
                index={index}
                requiereVestimenta={actividadRequiereVestimenta()}
                onChange={handlePersonaChange}
                errores={personasErrores[index] || {}}
              />
            ))}

            <div className="form-actions">
              <button type="button" className="btn-anterior" onClick={retrocederPaso}>
                ← Anterior
              </button>
              <button type="button" className="btn-siguiente" onClick={avanzarPaso}>
                Siguiente →
              </button>
            </div>
          </div>
        )}

        {paso === 3 && (
          <div className="paso-content">
            <h3>Confirmar Inscripción</h3>

            <div className="resumen">
              <div className="resumen-item">
                <strong>Actividad:</strong>
                {' '}
                {actividadSeleccionada}
              </div>
              <div className="resumen-item">
                <strong>Horario:</strong>
                {' '}
                {horarioSeleccionado}
              </div>
              <div className="resumen-item">
                <strong>Cantidad de personas:</strong>
                {' '}
                {cantidadPersonas}
              </div>
            </div>

            <div className="terminos-section">
              <button
                type="button"
                className="btn-ver-terminos"
                onClick={() => setMostrarTerminos(!mostrarTerminos)}
              >
                {mostrarTerminos ? '▼' : '▶'}
                {' '}
                Ver Términos y Condiciones
              </button>

              {mostrarTerminos && (
                <div className="terminos-contenido">
                  <pre>{TERMINOS_Y_CONDICIONES}</pre>
                </div>
              )}

              <div className="form-group terminos-checkbox">
                <label htmlFor="terminos">
                  <input
                    id="terminos"
                    type="checkbox"
                    checked={aceptoTerminos}
                    onChange={(e) => setAceptoTerminos(e.target.checked)}
                    required
                  />
                  {' '}
                  <span>
                    He leído y acepto los
                    {' '}
                    <strong>Términos y Condiciones</strong>
                    {' '}
                    *
                  </span>
                </label>
              </div>
            </div>

            <div className="form-actions">
              <button type="button" className="btn-anterior" onClick={retrocederPaso}>
                ← Anterior
              </button>
              <button
                type="submit"
                className="btn-confirmar"
                disabled={cargando || !aceptoTerminos}
              >
                {cargando ? 'Procesando...' : 'Confirmar Inscripción'}
              </button>
            </div>
          </div>
        )}
      </form>
    </div>
  );
}

export default InscripcionForm;
