import React from 'react';
import { useNavigate } from 'react-router-dom';
import Step1Select from '../components/Step1Select';
import { useInscripcion } from '../context/inscripcionContext';

export default function Step1Page() {
  const navigate = useNavigate();
  const {
    selectedActivity, setSelectedActivity,
    selectedSlot, setSelectedSlot,
  } = useInscripcion();

  return (
    <Step1Select
      selectedActivity={selectedActivity}
      selectedSlot={selectedSlot}
      onSelectActivity={(name) => { setSelectedActivity(name); setSelectedSlot(null); }}
      onSelectSlot={setSelectedSlot}
      onNext={() => navigate('/participantes')}
    />
  );
}
