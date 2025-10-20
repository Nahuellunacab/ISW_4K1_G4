import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Step2Participants from '../components/Step2Participants';
import { useInscripcion } from '../context/inscripcionContext';

export default function Step2Page() {
  const navigate = useNavigate();
  const {
    selectedActivity, selectedSlot,
    cantidad, setCantidad,
    participants, setParticipants,
  } = useInscripcion();

  // Guard: si no hay actividad/horario, volver al paso 1
  useEffect(() => {
    if (!selectedActivity || !selectedSlot) navigate('/');
  }, [selectedActivity, selectedSlot, navigate]);

  return (
    <Step2Participants
      selectedActivity={selectedActivity}
      selectedSlot={selectedSlot}
      cantidad={cantidad}
      participants={participants}
      onCantidadChange={setCantidad}
      onParticipantsChange={setParticipants}
      onPrev={() => navigate('/')}
      onNext={() => navigate('/confirmacion')}
    />
  );
}
