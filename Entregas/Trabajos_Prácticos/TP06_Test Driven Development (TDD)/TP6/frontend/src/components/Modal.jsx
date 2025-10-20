import React from 'react'

export default function Modal({ open, title, message, success = false, onClose }) {
  if (!open) return null
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl p-8 max-w-md w-full text-center">
        <div className="text-6xl mb-4">{success ? '✅' : '❌'}</div>
        <h2 className={`text-2xl font-bold mb-2 ${success ? 'text-green-700' : 'text-red-600'}`}>{title}</h2>
        <p className="text-stone-600 mb-6">{message}</p>
        <button onClick={onClose} className="bg-stone-700 text-white font-bold py-2 px-8 rounded-lg hover:bg-stone-800 transition">
          Cerrar
        </button>
      </div>
    </div>
  )
}
