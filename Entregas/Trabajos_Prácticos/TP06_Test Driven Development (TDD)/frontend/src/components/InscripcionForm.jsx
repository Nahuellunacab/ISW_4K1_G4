import {
  useState,
  useEffect,
  useCallback,
  useRef,
} from 'react';

import {
  obtenerActividades,
  obtenerHorarios,
  crearInscripcion,
} from '../services/api';

import { TERMINOS_Y_CONDICIONES } from '../constants/terminos';
import PersonaForm from './PersonaForm';
import './InscripcionForm.css';


function InscripcionForm({ onVolver }) {
  // =========================
  // Estado
  // =========================
  const [actividades, setActividades] = useState([]);
  const [actividadSeleccionada, setActividadSeleccionada] = useState('');
  const [horarios, setHorarios] = useState([]);
  const [horarioSeleccionado, setHorarioSeleccionado] = useState('');
  const [cantidadPersonas, setCantidadPersonas] = useState(1);
  const [personas, setPersonas] = useState([
    { id: 1, nombre: '', tallaVestimenta: '', edad: '', DNI: '' },
  ]);
  const [personasErrores, setPersonasErrores] = useState([{}]);
  const [aceptoTerminos, setAceptoTerminos] = useState(false);
  const [mostrarTerminos, setMostrarTerminos] = useState(false);
  const [cargando, setCargando] = useState(false);
  const [mensaje, setMensaje] = useState(null); // { tipo: 'error' | 'exito', texto: string }
  const [paso, setPaso] = useState(1);

  // Regex compilados una sola vez
  const nombreRegexRef = useRef(/^[A-Za-zÀ-ÿ\s\-']+$/);
  const dniRegexRef = useRef(/^\d{6,10}$/);

  // =========================
  // Carga inicial de actividades
  // =========================
  useEffect(() => {
    let cancelado = false;
    (async () => {
      try {
        const resp = await obtenerActividades();
        if (!cancelado && resp?.exito && Array.isArray(resp.actividades)) {
          setActividades(resp.actividades);
        }
      } catch {
        if (!cancelado) {
          setMensaje({ tipo: 'error', texto: 'Error al cargar actividades' });
        }
      }
    })();
    return () => {
      cancelado = true;
    };
  }, []);

  // =========================
  // Carga de horarios cuando cambia la actividad
  // =========================
  const cargarHorarios = useCallback(async (nombreActividad, signal) => {
    const vaciar = () => {
      setHorarios([]);
      setHorarioSeleccionado('');
    };
    if (!nombreActividad) {
      vaciar();
      return;
    }
    try {
      const resp = await obtenerHorarios(nombreActividad, { signal });
      if (resp?.exito && Array.isArray(resp.horarios)) {
        setHorarios(resp.horarios);
      } else {
        vaciar();
      }
    } catch (e) {
      if (e?.name !== 'AbortError') {
        setMensaje({ tipo: 'error', texto: 'Error al cargar horarios' });
        vaciar();
      }
    }
  }, []);

  useEffect(() => {
    const ctrl = new AbortController();
    cargarHorarios(actividadSeleccionada, ctrl.signal);
    // al cambiar de actividad, volvemos a paso 1 y reseteamos selección de horario & cantidad
    setPaso(1);
    setHorarioSeleccionado('');
    setCantidadPersonas(1);
    return () => ctrl.abort();
  }, [actividadSeleccionada, cargarHorarios]);

  // =========================
  // Mantener largo de arrays personas/errores = cantidadPersonas
  // =========================
  useEffect(() => {
    setPersonas((prev) => {
      const next = Array.from({ length: cantidadPersonas }, (_, i) => ({
        id: i + 1,
        nombre: prev[i]?.nombre ?? '',
        tallaVestimenta: prev[i]?.tallaVestimenta ?? '',
        edad: prev[i]?.edad ?? '',
        DNI: prev[i]?.DNI ?? '',
      }));
      return next;
    });
    setPersonasErrores((prev) =>
      Array.from({ length: cantidadPersonas }, (_, i) => prev?.[i] || {})
    );
  }, [cantidadPersonas]);

  // =========================
  // Utilidades de validación
  // =========================
  const actividadRequiereVestimenta = useCallback(
    (actividad = actividadSeleccionada) => {
      const actividadObj = actividades.find((a) => a.nombre === actividad);
      return Boolean(actividadObj?.requiereVestimenta);
    },
    [actividades, actividadSeleccionada]
  );

  const validarPersona = useCallback(
    (persona) => {
      const errores = {};
      const nombre = (persona?.nombre || '').toString().trim();
      if (!nombre || !nombreRegexRef.current.test(nombre)) {
        errores.nombre = 'Nombre inválido (solo letras, espacios y guiones)';
      }
      const dni = (persona?.DNI || '').toString().trim();
      if (!dni || !dniRegexRef.current.test(dni)) {
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
    },
    [actividadRequiereVestimenta]
  );

  const validarDuplicadosDNI = useCallback((lista) => {
    const dnis = lista.map((p) => String(p?.DNI || '').trim()).filter(Boolean);
    const repetidos = dnis.filter((dni, i, arr) => arr.indexOf(dni) !== i);
    return new Set(repetidos);
  }, []);

  // =========================
  // Handlers
  // =========================
  const handleActividadChange = (e) => {
    setActividadSeleccionada(e.target.value);
    setMensaje(null);
  };

  const handlePersonaChange = (index, campo, valor) => {
    const nuevas = [...personas];
    // normalizo espacios en blanco para strings
    const valNorm =
      typeof valor === 'string' ? valor.replace(/\s{2,}/g, ' ').trimStart() : valor;
    nuevas[index] = { ...(nuevas[index] || {}), [campo]: valNorm };
    setPersonas(nuevas);

    // validación en caliente
    const errs = [...(personasErrores || [])];
    errs[index] = validarPersona(nuevas[index]);
    const repetidos = validarDuplicadosDNI(nuevas);
    errs.forEach((e, i) => {
      const dniActual = String(nuevas[i]?.DNI || '').trim();
      if (dniActual && repetidos.has(dniActual)) {
        errs[i] = { ...(errs[i] || {}), DNI: 'DNI duplicado en el formulario' };
      } else if (errs[i]?.DNI === 'DNI duplicado en el formulario' && !repetidos.has(dniActual)) {
        const c = { ...(errs[i] || {}) };
        delete c.DNI;
        errs[i] = c;
      }
    });
    setPersonasErrores(errs);
  };

  const obtenerCuposDisponibles = useCallback(() => {
    const h = horarios.find((x) => x.horario === horarioSeleccionado);
    return Number(h?.cuposDisponibles) || 0;
  }, [horarios, horarioSeleccionado]);

  const validarFormulario = () => {
    if (!actividadSeleccionada) {
      setMensaje({ tipo: 'error', texto: 'Debe seleccionar una actividad' });
      return false;
    }
    if (!horarioSeleccionado) {
      setMensaje({ tipo: 'error', texto: 'Debe seleccionar un horario' });
      return false;
    }

    const errs = personas.map((p) => validarPersona(p));
    const repetidos = validarDuplicadosDNI(personas);
    errs.forEach((e, i) => {
      const dni = String(personas[i]?.DNI || '').trim();
      if (dni && repetidos.has(dni)) {
        errs[i] = { ...(e || {}), DNI: 'DNI duplicado en el formulario' };
      }
    });
    setPersonasErrores(errs);

    const hayErrores = errs.some((e) => e && Object.keys(e).length > 0);
    if (hayErrores) {
      const resumen = errs
        .map((err, i) => {
          if (!err || Object.keys(err).length === 0) return null;
          const nombre = (personas[i]?.nombre || `Persona ${i + 1}`).toString().trim();
          const detalles = Object.values(err).join(', ');
          return `${i + 1}) ${nombre} — ${detalles}`;
        })
        .filter(Boolean)
        .join('; ');
      setMensaje({
        tipo: 'error',
        texto: resumen
          ? `Errores en los participantes: ${resumen}`
          : 'Corrija los errores en los datos de las personas',
      });
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

  const avanzarPaso = () => {
    if (paso === 1) {
      if (!actividadSeleccionada || !horarioSeleccionado) {
        setMensaje({ tipo: 'error', texto: 'Seleccione actividad y horario' });
        return;
      }
      if (!cantidadPersonas || cantidadPersonas < 1) {
        setMensaje({ tipo: 'error', texto: 'Debe ingresar al menos 1 persona' });
        return;
      }
      const cupos = obtenerCuposDisponibles();
      if (cantidadPersonas > cupos) {
        setMensaje({
          tipo: 'error',
          texto: `No hay suficientes cupos. Disponibles: ${cupos}`,
        });
        return;
      }
    }

    if (paso === 2) {
      const errs = personas.map((p) => validarPersona(p));
      const repetidos = validarDuplicadosDNI(personas);
      errs.forEach((e, i) => {
        const dni = String(personas[i]?.DNI || '').trim();
        if (dni && repetidos.has(dni)) {
          errs[i] = { ...(e || {}), DNI: 'DNI duplicado en el formulario' };
        }
      });
      setPersonasErrores(errs);

      const hayErrores = errs.some((e) => e && Object.keys(e).length > 0);
      if (hayErrores) {
        const resumen = errs
          .map((err, i) => {
            if (!err || Object.keys(err).length === 0) return null;
            const nombre = (personas[i]?.nombre || `Persona ${i + 1}`).toString().trim();
            const detalles = Object.values(err).join(', ');
            return `${i + 1}) ${nombre} — ${detalles}`;
          })
          .filter(Boolean)
          .join('; ');
        setMensaje({
          tipo: 'error',
          texto: resumen
            ? `Corrija los errores en participantes: ${resumen}`
            : 'Corrija los errores en los datos de las personas',
        });
        return;
      }
    }

    setPaso((p) => p + 1);
    setMensaje(null);
  };

  const retrocederPaso = () => {
    setPaso((p) => Math.max(1, p - 1));
    setMensaje(null);
  };

  const resetFormulario = () => {
    setActividadSeleccionada('');
    setHorarioSeleccionado('');
    setCantidadPersonas(1);
    setPersonas([{ id: 1, nombre: '', tallaVestimenta: '', edad: '', DNI: '' }]);
    setPersonasErrores([{}]);
    setAceptoTerminos(false);
    setPaso(1);
    setMensaje(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validarFormulario()) return;

    setCargando(true);
    setMensaje(null);

    try {
      const payload = {
        actividad: actividadSeleccionada,
        cantidadPersonas,
        horario: horarioSeleccionado,
        personas: personas.map((p) => ({
          nombre: (p.nombre || '').toString().trim(),
          tallaVestimenta: p.tallaVestimenta || null,
          edad: parseInt(p.edad, 10),
          DNI: (p.DNI || '').toString().trim(),
        })),
        aceptoTerminosYCondiciones: aceptoTerminos,
      };

      const resp = await crearInscripcion(payload);

      if (resp?.exito) {
        setMensaje({
          tipo: 'exito',
          texto: `¡Inscripción exitosa! ID: ${resp.idInscripcion}`,
        });
        // Limpiar tras unos segundos
        setTimeout(() => {
          resetFormulario();
        }, 2500);
      } else {
        setMensaje({ tipo: 'error', texto: resp?.mensaje || 'No se pudo completar la inscripción' });
      }
    } catch (error) {
      setMensaje({
        tipo: 'error',
        texto: error?.response?.data?.mensaje || 'Error al procesar la inscripción',
      });
    } finally {
      setCargando(false);
    }
  };

  // =========================
  // Render
  // =========================
  const cuposDisponibles = horarioSeleccionado ? obtenerCuposDisponibles() : 0;
  const maxCantidadInput = horarioSeleccionado ? Math.max(1, cuposDisponibles) : 10;

  return (
    <div className="inscripcion-form">
      <div className="form-header">
        <button type="button" className="btn-volver" onClick={onVolver} aria-label="Volver">
          ← Volver
        </button>
        <h2>Formulario de Inscripción</h2>
        <div className="pasos" aria-label="Progreso">
          <span className={paso === 1 ? 'paso-activo' : ''}>1. Actividad</span>
          <span className={paso === 2 ? 'paso-activo' : ''}>2. Personas</span>
          <span className={paso === 3 ? 'paso-activo' : ''}>3. Confirmar</span>
        </div>
      </div>

      {mensaje && (
        <div
          className={`mensaje mensaje-${mensaje.tipo}`}
          role={mensaje.tipo === 'error' ? 'alert' : 'status'}
          aria-live="polite"
        >
          {mensaje.texto}
        </div>
      )}

      <form onSubmit={handleSubmit} noValidate>
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
                      {actividad.requiereVestimenta ? ' (requiere talla)' : ''}
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
                  onChange={(e) => {
                    setHorarioSeleccionado(e.target.value);
                    setMensaje(null);
                  }}
                  disabled={!actividadSeleccionada}
                  required
                >
                  <option value="">Seleccione un horario</option>
                  {horarios.map((h) => {
                    const sinCupos = !h.cuposDisponibles || h.cuposDisponibles === 0;
                    const value = h.horario;
                    return (
                      <option
                        key={`${value}__${h.cuposDisponibles}`}
                        value={value}
                        disabled={sinCupos}
                        className={sinCupos ? 'opcion-sin-cupos' : ''}
                        title={
                          sinCupos ? 'Sin cupos disponibles' : `${h.cuposDisponibles} cupos disponibles`
                        }
                      >
                        {h.horario} ({h.cuposDisponibles} cupos)
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
                  min={1}
                  max={maxCantidadInput}
                  value={cantidadPersonas}
                  onChange={(e) => {
                    const n = Number(e.target.value);
                    if (Number.isNaN(n)) return;
                    const bounded = Math.min(Math.max(1, n), maxCantidadInput);
                    setCantidadPersonas(bounded);
                  }}
                  disabled={!horarioSeleccionado}
                  required
                  inputMode="numeric"
                />
                {horarioSeleccionado && (
                  <small className="helper-text">Cupos disponibles: {cuposDisponibles}</small>
                )}
              </label>
            </div>

            <button
              type="button"
              className="btn-siguiente"
              onClick={avanzarPaso}
              disabled={!actividadSeleccionada || !horarioSeleccionado}
            >
              Siguiente →
            </button>
          </div>
        )}

        {paso === 2 && (
          <div className="paso-content">
            <h3>Datos de los Participantes ({cantidadPersonas})</h3>
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
                <strong>Actividad:</strong> {actividadSeleccionada}
              </div>
              <div className="resumen-item">
                <strong>Horario:</strong> {horarioSeleccionado}
              </div>
              <div className="resumen-item">
                <strong>Cantidad de personas:</strong> {cantidadPersonas}
              </div>
            </div>

            <div className="terminos-section">
              <button
                type="button"
                className="btn-ver-terminos"
                onClick={() => setMostrarTerminos((v) => !v)}
                aria-expanded={mostrarTerminos}
                aria-controls="terminos-contenido"
              >
                {mostrarTerminos ? '▼' : '▶'} Ver Términos y Condiciones
              </button>

              {mostrarTerminos && (
                <div className="terminos-contenido" id="terminos-contenido">
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
                  />{' '}
                  <span>
                    He leído y acepto los <strong>Términos y Condiciones</strong> *
                  </span>
                </label>
              </div>
            </div>

            <div className="form-actions">
              <button type="button" className="btn-anterior" onClick={retrocederPaso}>
                ← Anterior
              </button>
              <button type="submit" className="btn-confirmar" disabled={cargando || !aceptoTerminos}>
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
