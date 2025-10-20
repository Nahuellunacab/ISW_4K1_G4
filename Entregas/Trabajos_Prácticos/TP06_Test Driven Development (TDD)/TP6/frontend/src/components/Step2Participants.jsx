import React, { useMemo } from 'react'
import { activitiesData } from '../constants/activities'

export default function Step2Participants({ selectedActivity, selectedSlot, cantidad, participants, onCantidadChange, onParticipantsChange, onPrev, onNext }) {
  const requiresTalla = selectedActivity ? activitiesData[selectedActivity].requiresTalla : false
  const available = selectedSlot ? (selectedSlot.total - selectedSlot.booked) : 0

  const handleCantidad = (e) => {
    const v = parseInt(e.target.value, 10)
    if (Number.isFinite(v) && v > 0 && v <= available) onCantidadChange(v)
  }

  const update = (i, patch) => {
    const copy = [...participants]
    copy[i] = { ...(copy[i]||{}), ...patch }
    onParticipantsChange(copy)
  }

  const forms = useMemo(() => {
    const arr = []
    for (let i=0;i<cantidad;i++) {
      const p = participants[i] || {}
      arr.push(
        <div key={i} className="border border-stone-200 p-4 rounded-lg">
          <h4 className="font-bold mb-3">Participante {i+1}</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-stone-700">Nombre Completo</label>
              <input value={p.nombre||''} onChange={(e)=>update(i,{nombre:e.target.value})}
                     className="mt-1 block w-full p-2 border border-stone-300 rounded-md focus:ring-green-500 focus:border-green-500"/>
            </div>
            <div>
              <label className="block text-sm font-medium text-stone-700">DNI</label>
              <input value={p.dni||''} onChange={(e)=>update(i,{dni:e.target.value})}
                     className="mt-1 block w-full p-2 border border-stone-300 rounded-md focus:ring-green-500 focus:border-green-500"/>
            </div>
            <div>
              <label className="block text-sm font-medium text-stone-700">Edad</label>
              <input type="number" value={p.edad||''} onChange={(e)=>update(i,{edad:e.target.value})}
                     className="mt-1 block w-full p-2 border border-stone-300 rounded-md focus:ring-green-500 focus:border-green-500"/>
            </div>
            {requiresTalla && (
              <div>
                <label className="block text-sm font-medium text-stone-700">Talla de Vestimenta</label>
                <select value={p.tallaVestimenta||''} onChange={(e)=>update(i,{tallaVestimenta:e.target.value})}
                        className="mt-1 block w-full p-2 border border-stone-300 rounded-md focus:ring-green-500 focus:border-green-500">
                  <option value="">Seleccionar...</option>
                  <option>XS</option><option>S</option><option>M</option><option>L</option><option>XL</option>
                </select>
              </div>
            )}
          </div>
        </div>
      )
    }
    return arr
  }, [cantidad, participants, requiresTalla])

  return (
    <section>
      <h2 className="text-2xl font-bold mb-2 text-green-700">Paso 2: Datos de los Participantes</h2>
      <p className="text-stone-500 mb-6">Ingresa la información de cada persona que asistirá.</p>

      <div>
        <label className="block text-sm font-medium text-stone-700 mb-1">Cantidad de Personas:</label>
        <input type="number" min="1" max={available} value={cantidad} onChange={handleCantidad}
               className="w-24 p-2 border border-stone-300 rounded-md focus:ring-green-500 focus:border-green-500"/>
        <p className="text-xs text-stone-500 mt-1">Cupo disponible: {available}</p>
      </div>

      <div className="mt-6 space-y-6">{forms}</div>

      <div className="flex justify-between mt-8">
        <button onClick={onPrev} className="bg-stone-200 text-stone-700 font-bold py-2 px-6 rounded-lg hover:bg-stone-300 transition">Anterior</button>
        <button onClick={onNext} className="bg-green-700 text-white font-bold py-2 px-6 rounded-lg hover:bg-green-800 transition">Siguiente</button>
      </div>
    </section>
  )
}
