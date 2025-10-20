import React, { useMemo } from 'react'
import { activitiesData } from '../constants/activities'
import { termsHtml } from '../constants/terms'

export default function Step3Confirm({ state, onPrev, onConfirm }) {
  const requiresTalla = activitiesData[state.selectedActivity]?.requiresTalla
  const valid = useMemo(() => {
    if (!state.acepta) return false
    if (!state.selectedActivity || !state.selectedSlot) return false
    const available = state.selectedSlot.total - state.selectedSlot.booked
    if (state.cantidadPersonas < 1 || state.cantidadPersonas > available) return false
    for (const p of state.participants) {
      if (!p?.nombre || !p?.dni || !p?.edad) return false
      if (requiresTalla && !p?.tallaVestimenta) return false
    }
    return true
  }, [state, requiresTalla])

  return (
    <section>
      <h2 className="text-2xl font-bold mb-2 text-green-700">Paso 3: Resumen y Confirmación</h2>
      <p className="text-stone-500 mb-6">Por favor, revisa tu selección y acepta los términos para finalizar.</p>

      <div className="bg-lime-50 p-4 rounded-lg border border-lime-200 mb-6 space-y-2">
        <p><strong>Actividad:</strong> {state.selectedActivity}</p>
        <p><strong>Horario:</strong> {state.selectedSlot?.time}</p>
        <p><strong>Cantidad de Personas:</strong> {state.cantidadPersonas}</p>
      </div>

      <div className="mb-6">
        <h3 className="text-lg font-bold mb-2">Términos y Condiciones de la Actividad</h3>
        <div className="h-48 overflow-y-auto border border-stone-200 rounded-md p-4 bg-stone-50 text-sm" dangerouslySetInnerHTML={{ __html: termsHtml }} />
      </div>

      <div className="flex items-center">
        <input id="terms-checkbox" type="checkbox" checked={state.acepta} onChange={e=>state.setAcepta(e.target.checked)}
               className="h-4 w-4 text-green-600 focus:ring-green-500 border-stone-300 rounded"/>
        <label htmlFor="terms-checkbox" className="ml-2 block text-sm text-stone-900">He leído y acepto los Términos y Condiciones.</label>
      </div>

      <div className="flex justify-between mt-8">
        <button onClick={onPrev} className="bg-stone-200 text-stone-700 font-bold py-2 px-6 rounded-lg hover:bg-stone-300 transition">Anterior</button>
        <button disabled={!valid} onClick={onConfirm}
                className="bg-green-700 text-white font-bold py-2 px-6 rounded-lg hover:bg-green-800 transition disabled:bg-stone-300 disabled:cursor-not-allowed">
          Confirmar Inscripción
        </button>
      </div>
    </section>
  )
}
