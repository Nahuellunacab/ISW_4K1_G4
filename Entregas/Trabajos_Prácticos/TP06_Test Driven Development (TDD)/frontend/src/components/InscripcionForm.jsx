import { useState, useEffect } from 'react';
import {
  obtenerActividades,
  obtenerHorarios,
  crearInscripcion,
} from '../services/api';
import PersonaForm from './PersonaForm';
import './InscripcionForm.css';

function InscripcionForm({ onVolver }) {
  const [actividades, setActividades] = useState([]);
  const [actividadSeleccionada, setActividadSeleccionada] = useState('');
  const [horarios, setHorarios] = useState([]);
  const [horarioSeleccionado, setHorarioSeleccionado] = useState('');
  const [cantidadPersonas, setCantidadPersonas] = useState(1);
  const [personas, setPersonas] = useState([]);
  const [aceptoTerminos, setAceptoTerminos] = useState(false);
  const [cargando, setCargando] = useState(false);
  const [mensaje, setMensaje] = useState(null);
  const [paso, setPaso] = useState(1);

  useEffect(() => {
    cargarActividades();
  }, []);

  useEffect(() => {
    if (actividadSeleccionada) {
      cargarHorarios(actividadSeleccionada);
    }
  }, [actividadSeleccionada]);

  useEffect(() => {
    const nuevasPersonas = Array.from({ length: cantidadPersonas }, (_, i) => ({
      id: i + 1,
      nombre: personas[i]?.nombre || '',
      tallaVestimenta: personas[i]?.tallaVestimenta || '',
      edad: personas[i]?.edad || '',
      DNI: personas[i]?.DNI || '',
    }));
    setPersonas(nuevasPersonas);
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

  const handlePersonaChange = (index, campo, valor) => {
    const nuevasPersonas = [...personas];
    nuevasPersonas[index][campo] = valor;
    setPersonas(nuevasPersonas);
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

    // eslint-disable-next-line no-restricted-syntax
    for (const persona of personas) {
      if (!persona.nombre || !persona.edad || !persona.DNI) {
        setMensaje({
          tipo: 'error',
          texto: 'Complete todos los datos de las personas',
        });
        return false;
      }
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

  const actividadRequiereVestimenta = () => {
    const actividad = actividades.find((a) => a.nombre === actividadSeleccionada);
    return actividad?.requiereVestimenta || false;
  };

  const avanzarPaso = () => {
    if (paso === 1 && (!actividadSeleccionada || !horarioSeleccionado)) {
      setMensaje({
        tipo: 'error',
        texto: 'Seleccione actividad y horario',
      });
      return;
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
                  {horarios.map((horario) => (
                    <option key={horario.horario} value={horario.horario}>
                      {horario.horario}
                      {' '}
                      (
                      {horario.cuposDisponibles}
                      {' '}
                      cupos)
                    </option>
                  ))}
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
                  max="10"
                  value={cantidadPersonas}
                  onChange={(e) => setCantidadPersonas(parseInt(e.target.value, 10))}
                  required
                />
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

            <div className="form-group terminos">
              <label htmlFor="terminos">
                <input
                  id="terminos"
                  type="checkbox"
                  checked={aceptoTerminos}
                  onChange={(e) => setAceptoTerminos(e.target.checked)}
                  required
                />
                {' '}
                Acepto los términos y condiciones *
              </label>
            </div>

            <div className="form-actions">
              <button type="button" className="btn-anterior" onClick={retrocederPaso}>
                ← Anterior
              </button>
              <button
                type="submit"
                className="btn-confirmar"
                disabled={cargando}
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
