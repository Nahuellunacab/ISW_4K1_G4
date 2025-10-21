# TP6 - Test Driven Development (TDD)
## Grupo 4 Ingeniería y Calidad de Software - ISW 4K1

### Integrantes

- [Bailey, Julian Eduardo - 96032](https://github.com/Shadow987654)
- [Cufre, Ángel Hugo - 94490](https://github.com/AngelHCufre)
- [Carrió, Tomás Ezequiel - 94763](https://github.com/TomiiC73)
- [Espósito, Nicolás - 90203](https://github.com/NicolasEsposito10)
- [Fernandez, Pablo - 95695](https://github.com/FernandezPabloGabriel)
- [Luna, Ángel Nahuel - 89627](https://github.com/Nahuellunacab)
- [Longo Prudencio, Máximo - 97101](https://github.com/MaximoLongo)
- [Patolsky, Daniel - 92847](https://github.com/DanielPatolsky)
- [Titón, Máximo - 98175](https://github.com/maxiTiton)
- [Uliana, Agustín - 97828](https://github.com/AgustinUliana97828)

---

## 📋 User Story: Inscribirme a actividad

**Como** visitante **QUIERO** inscribirme a una actividad **PARA** reservar mi lugar en la misma.

---

## 🚀 Aplicación Full-Stack

Este proyecto implementa una aplicación completa con:

- **Backend**: Flask + Python (PEP8)
- **Frontend**: React + Vite (Airbnb Style Guide)
- **Base de Datos**: SQLite3
- **Tests**: unittest (TDD)

---

## 📖 Inicio Rápido

### Opción 1: Scripts Automáticos (Recomendado)

#### 1. Iniciar Backend
```powershell
.\start-backend.ps1
```

#### 2. Iniciar Frontend (nueva terminal)
```powershell
.\start-frontend.ps1
```

#### 3. Acceder a la aplicación
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000

### Opción 2: Manual

Ver **[INICIO_RAPIDO.md](./INICIO_RAPIDO.md)** para instrucciones detalladas.

---

## 🧪 Ejecutar Tests

```powershell
.\run-tests.ps1
```

O manualmente:
```powershell
.\venv\Scripts\Activate.ps1
python -m unittest tests/test_inscribirse_actividad.py -v
```

---

## 📚 Documentación Completa

- **[README_PROYECTO.md](./README_PROYECTO.md)** - Documentación técnica completa
- **[INICIO_RAPIDO.md](./INICIO_RAPIDO.md)** - Guía de inicio rápido
- **Tests**: `tests/test_inscribirse_actividad.py`
- **Lógica de negocio**: `src/inscribirse_actividad.py`

---

## 🎯 Criterios de Aceptación Implementados

✅ Selección de actividad (Tirolesa, Safari, Palestra, Jardinería)  
✅ Selección de horario con cupos disponibles  
✅ Indicación de cantidad de personas  
✅ Ingreso de datos: nombre, DNI, edad, talla (si aplica)  
✅ Aceptación de términos y condiciones  
✅ Validación de edad mínima por actividad  
✅ Validación de talla requerida para actividades específicas  

---

## 🛠️ Tecnologías

| Área | Tecnología |
|------|-----------|
| Backend | Flask 3.0.0, Python 3.8+ |
| Frontend | React 18.2, Vite 5.0, Node.js |
| Base de Datos | SQLite3 |
| Testing | unittest, pytest |
| Estilos | PEP8 (Python), Airbnb (JavaScript) |

---

## 📁 Estructura del Proyecto

```
TP06_Test Driven Development (TDD)/
├── backend/              # API REST Flask
├── frontend/             # Aplicación React
├── src/                  # Lógica de negocio
├── tests/                # Tests unitarios
├── actividades.db        # Base de datos SQLite
└── *.ps1                 # Scripts de ejecución
```

---

## ❓ Soporte

Para problemas o dudas, consultar:
1. [README_PROYECTO.md](./README_PROYECTO.md) - Sección "Solución de Problemas"
2. [INICIO_RAPIDO.md](./INICIO_RAPIDO.md) - Problemas comunes

---

**© 2025 Grupo 4 - ISW 4K1 - UTN**

