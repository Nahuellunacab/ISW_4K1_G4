import { useState, useEffect } from 'react';
import InscripcionForm from './components/InscripcionForm';
import './App.css';

function App() {
  const [mostrarFormulario, setMostrarFormulario] = useState(false);

  return (
    <div className="app">
      <header className="app-header">
        <h1>🌿 EcoHarmony Park</h1>
        <p>Sistema de Inscripción a Actividades</p>
      </header>

      <main className="app-main">
        {!mostrarFormulario ? (
          <div className="welcome-section">
            <h2>Bienvenido al Parque EcoHarmony</h2>
            <p>
              Inscríbete en nuestras emocionantes actividades:
              Tirolesa, Palestra, Safari y Jardinería
            </p>
            <button
              type="button"
              className="btn-primary"
              onClick={() => setMostrarFormulario(true)}
            >
              Comenzar Inscripción
            </button>
          </div>
        ) : (
          <InscripcionForm onVolver={() => setMostrarFormulario(false)} />
        )}
      </main>

      <footer className="app-footer">
        <p>© 2025 EcoHarmony Park - Grupo 4 ISW 4K1</p>
      </footer>
    </div>
  );
}

export default App;
