import React from 'react'
import { activitiesData } from '../constants/activities'

export default function Step1Select({ selectedActivity, selectedSlot, onSelectActivity, onSelectSlot, onNext }) {
  const activity = selectedActivity ? activitiesData[selectedActivity] : null
  const canContinue = Boolean(selectedActivity && selectedSlot)

  return (
    <section>
      <h2 className="text-2xl font-bold mb-2 text-green-700">Elige tu Actividad y Horario</h2>
      <p className="text-stone-500 mb-6">Selecciona una de nuestras experiencias únicas.</p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {Object.entries(activitiesData).map(([name, a]) => (
          <div
            key={name}
            className={`activity-card bg-lime-50 border-2 p-6 rounded-xl cursor-pointer ${selectedActivity === name ? 'selected border-lime-400' : 'border-lime-200'}`}
            onClick={() => onSelectActivity(name)}
          >
            <div className="text-4xl mb-3">{a.icon}</div>
            <h3 className="text-xl font-bold text-green-900">{name}</h3>
            <p className="text-stone-600 mt-1">{a.description}</p>
          </div>
        ))}
      </div>

      {activity && (
        <div className="mt-8">
          <h3 className="text-xl font-bold mb-4">Horarios Disponibles</h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
            {activity.slots.map(slot => {
              const available = slot.total - slot.booked
              const disabled = available <= 0
              const isSelected = selectedSlot && selectedSlot.time === slot.time
              return (
                <button
                  key={slot.time}
                  disabled={disabled}
                  onClick={() => !disabled && onSelectSlot(slot)}
                  className={`slot-btn p-2 border-2 rounded-lg transition text-sm
                    ${disabled ? 'border-stone-300 text-stone-400 bg-stone-100 cursor-not-allowed'
                              : 'border-green-600 text-green-700 hover:bg-green-100'}
                    ${isSelected ? 'selected' : ''}`}
                >
                  {slot.time} ({available} disp.)
                </button>
              )
            })}
          </div>
        </div>
      )}

      <div className="flex justify-end mt-8">
        <button
          onClick={onNext}
          disabled={!canContinue}
          className="bg-green-700 text-white font-bold py-2 px-6 rounded-lg hover:bg-green-800 transition disabled:bg-stone-300 disabled:cursor-not-allowed"
        >
          Siguiente
        </button>
      </div>
    </section>
  )
}
