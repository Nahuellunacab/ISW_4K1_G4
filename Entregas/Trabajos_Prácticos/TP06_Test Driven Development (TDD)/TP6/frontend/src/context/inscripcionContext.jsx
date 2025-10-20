import React, { createContext, useContext, useMemo, useState } from 'react';
import { activitiesData } from '../constants/activities';

const InscripcionCtx = createContext(null);

export function InscripcionProvider({ children }) {
  const [step, setStep] = useState(1);
  const [selectedActivity, setSelectedActivity] = useState(null);
  const [selectedSlot, setSelectedSlot] = useState(null);
  const [cantidad, setCantidad] = useState(1);
  const [participants, setParticipants] = useState([]);
  const [acepta, setAcepta] = useState(false);
  const [modal, setModal] = useState({ open: false, title: '', message: '', success: false });

  const availableSpots = useMemo(() => {
    if (!selectedSlot) return 0;
    return Math.max(0, (selectedSlot.total || 0) - (selectedSlot.booked || 0));
  }, [selectedSlot]);

  const resetToFirst = () => {
    setStep(1);
    setSelectedActivity(null);
    setSelectedSlot(null);
    setCantidad(1);
    setParticipants([]);
    setAcepta(false);
  };

  const simularInscripcion = () => {
    const payload = {
      actividad: selectedActivity,
      cantidadPersonas: cantidad,
      horario: selectedSlot.time,
      personas: participants,
      aceptoTerminosYCondiciones: acepta,
    };

    if (!payload.aceptoTerminosYCondiciones) {
      return { exito: false, mensaje: 'Debe aceptar los Términos y Condiciones para continuar.' };
    }
    const available = selectedSlot.total - selectedSlot.booked;
    if (payload.cantidadPersonas > available) {
      return { exito: false, mensaje: 'No hay cupo disponible para el número de personas seleccionado.' };
    }
    const activityRequiresTalla = activitiesData[payload.actividad].requiresTalla;
    for (const persona of payload.personas) {
      if (!persona?.nombre || !persona?.dni || !persona?.edad) {
        return { exito: false, mensaje: 'Debe completar todos los datos de los participantes (Nombre, DNI, Edad).' };
      }
      if (activityRequiresTalla && !persona?.tallaVestimenta) {
        return { exito: false, mensaje: 'Esta actividad requiere que seleccione una talla de vestimenta para cada participante.' };
      }
    }
    const idInscripcion = `ECO-${Date.now()}-${Math.random().toString(36).substr(2, 5).toUpperCase()}`;
    return { exito: true, mensaje: `¡Su lugar ha sido reservado! Su código de inscripción es: ${idInscripcion}`, id: idInscripcion };
  };

  const value = {
    // state
    step, setStep,
    selectedActivity, setSelectedActivity,
    selectedSlot, setSelectedSlot,
    cantidad, setCantidad,
    participants, setParticipants,
    acepta, setAcepta,
    modal, setModal,
    availableSpots,

    // actions
    resetToFirst,
    simularInscripcion,
  };

  return <InscripcionCtx.Provider value={value}>{children}</InscripcionCtx.Provider>;
}

export function useInscripcion() {
  const ctx = useContext(InscripcionCtx);
  if (!ctx) throw new Error('useInscripcion must be used inside <InscripcionProvider>');
  return ctx;
}
