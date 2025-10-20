import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Step3Confirm from '../components/Step3Confirm';
import { useInscripcion } from '../context/inscripcionContext';

export default function Step3Page() {
  const navigate = useNavigate();
  const {
    selectedActivity, selectedSlot, cantidad, participants,
    acepta, setAcepta,
    simularInscripcion, setModal,
  } = useInscripcion();

  // Guard: si no completó paso 2, volver
  useEffect(() => {
    if (!selectedActivity || !selectedSlot) navigate('/');
  }, [selectedActivity, selectedSlot, navigate]);

  const onConfirm = () => {
    const r = simularInscripcion();
    setModal({ open: true, title: r.exito ? '¡Inscripción Exitosa!' : 'Error en la Inscripción', message: r.mensaje, success: r.exito });
  };

  return (
    <Step3Confirm
      state={{ selectedActivity, selectedSlot, cantidadPersonas: cantidad, participants, acepta, setAcepta }}
      onPrev={() => navigate('/participantes')}
      onConfirm={onConfirm}
    />
  );
}
