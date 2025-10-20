import React from 'react';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import { InscripcionProvider, useInscripcion } from './context/inscripcionContext';
import Step1Page from './pages/Step1Page';
import Step2Page from './pages/Step2Page';
import Step3Page from './pages/Step3Page';
import Modal from './components/Modal';

function Shell({ children }) {
  const { modal, setModal, resetToFirst } = useInscripcion();
  return (
    <div className="container mx-auto p-4 md:p-8 max-w-4xl">
      <header className="text-center mb-8">
        <h1 className="text-4xl md:text-5xl font-bold text-green-800">Inscripción a Actividades</h1>
        <p className="text-stone-600 mt-2 text-lg">EcoHarmony Park</p>
      </header>

      <main className="bg-white p-6 md:p-8 rounded-2xl shadow-lg">{children}</main>

      <Modal
        open={modal.open}
        title={modal.title}
        message={modal.message}
        success={modal.success}
        onClose={() => {
          const wasSuccess = modal.success;
          setModal({ open: false, title: '', message: '', success: false });
          if (wasSuccess) resetToFirst();
        }}
      />
    </div>
  );
}

export default function App() {
  return (
    <InscripcionProvider>
      <Router>
        <Shell>
          <Routes>
            <Route path="/" element={<Step1Page />} />
            <Route path="/participantes" element={<Step2Page />} />
            <Route path="/confirmacion" element={<Step3Page />} />
            {/* opcional: 404 simple */}
            <Route path="*" element={<Step1Page />} />
          </Routes>
        </Shell>
      </Router>
    </InscripcionProvider>
  );
}
