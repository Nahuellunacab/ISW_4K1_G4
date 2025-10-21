# Sistema de Inscripción a Actividades - EcoHarmony Park

Aplicación full-stack para gestionar inscripciones a actividades del parque EcoHarmony Park.

## 🏗️ Arquitectura del Proyecto

### Backend
- **Framework**: Flask 3.0.0
- **Base de datos**: SQLite3
- **Estilo de código**: PEP8
- **API REST**: Flask-CORS para comunicación con frontend

### Frontend
- **Framework**: React 18.2.0
- **Build tool**: Vite 5.0.8
- **Estilo de código**: Airbnb JavaScript Style Guide
- **Gestor de paquetes**: npm/Node.js

### Base de Datos
- **SQLite3** (actividades.db)
- Tablas: actividades, horarios, inscripciones

## 📁 Estructura del Proyecto

```
TP06_Test Driven Development (TDD)/
├── backend/
│   ├── app.py                    # API REST con Flask
│   ├── requirements.txt          # Dependencias Python
│   └── .flaskenv                 # Variables de entorno Flask
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── InscripcionForm.jsx
│   │   │   ├── InscripcionForm.css
│   │   │   ├── PersonaForm.jsx
│   │   │   └── PersonaForm.css
│   │   ├── services/
│   │   │   └── api.js           # Cliente API
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── main.jsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── .eslintrc.json           # Configuración Airbnb
├── src/
│   └── inscribirse_actividad.py  # Lógica de negocio (PEP8)
├── tests/
│   └── test_inscribirse_actividad.py
├── actividades.db                # Base de datos SQLite
└── README_PROYECTO.md            # Esta documentación
```

## 🚀 Instalación y Ejecución

### Requisitos Previos

- **Python 3.8+**
- **Node.js 18+** y **npm**
- **Git** (opcional)

### 1. Configurar Backend (Flask)

#### Windows PowerShell:

```powershell
# Navegar a la carpeta del proyecto
cd "d:\NICO\Desktop\ISW\ISW_4K1_G4\Entregas\Trabajos_Prácticos\TP06_Test Driven Development (TDD)"

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Instalar dependencias
cd backend
pip install -r requirements.txt

# Ejecutar servidor Flask
python app.py
```

El backend estará disponible en: **http://localhost:5000**

### 2. Configurar Frontend (React + Vite)

Abrir una **nueva terminal** PowerShell:

```powershell
# Navegar a la carpeta frontend
cd "d:\NICO\Desktop\ISW\ISW_4K1_G4\Entregas\Trabajos_Prácticos\TP06_Test Driven Development (TDD)\frontend"

# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm run dev
```

El frontend estará disponible en: **http://localhost:3000**

### 3. Verificar Base de Datos

La base de datos SQLite (`actividades.db`) se crea automáticamente al iniciar el backend por primera vez.

Para verificar que existe:

```powershell
# Desde la carpeta raíz del proyecto
ls actividades.db
```

## 🧪 Ejecutar Tests

Los tests unitarios están implementados con `unittest`:

```powershell
# Activar entorno virtual (si no está activo)
.\venv\Scripts\Activate.ps1

# Ejecutar tests
python -m pytest tests/ -v
# O con unittest:
python -m unittest tests/test_inscribirse_actividad.py
```

## 📡 API Endpoints

### GET `/api/actividades`
Obtiene todas las actividades disponibles.

**Respuesta:**
```json
{
  "exito": true,
  "actividades": [
    {
      "nombre": "Tirolesa",
      "requiereVestimenta": true
    },
    {
      "nombre": "Palestra",
      "requiereVestimenta": true
    },
    {
      "nombre": "Safari",
      "requiereVestimenta": false
    },
    {
      "nombre": "Jardineria",
      "requiereVestimenta": false
    }
  ]
}
```

### GET `/api/actividades/{nombre}/horarios`
Obtiene los horarios disponibles para una actividad.

**Respuesta:**
```json
{
  "exito": true,
  "horarios": [
    {
      "horario": "10:00 GMT-3",
      "cuposDisponibles": 10
    }
  ]
}
```

### POST `/api/inscripciones`
Crea una nueva inscripción.

**Request Body:**
```json
{
  "actividad": "Tirolesa",
  "cantidadPersonas": 1,
  "horario": "10:00 GMT-3",
  "personas": [
    {
      "nombre": "Julian",
      "tallaVestimenta": "M",
      "edad": 21,
      "DNI": "44152639"
    }
  ],
  "aceptoTerminosYCondiciones": true
}
```

**Respuesta (Éxito):**
```json
{
  "exito": true,
  "mensaje": "Inscripción exitosa",
  "idInscripcion": "INS-001"
}
```

**Respuesta (Error):**
```json
{
  "exito": false,
  "mensaje": "Debe aceptar Términos y Condiciones",
  "idInscripcion": null
}
```

## ✅ Validaciones Implementadas

Según los criterios de aceptación de la User Story:

1. ✅ **Actividades válidas**: Solo Tirolesa, Safari, Palestra y Jardinería
2. ✅ **Horarios disponibles**: Verificación de cupos disponibles
3. ✅ **Cantidad de personas**: Especificada en el formulario
4. ✅ **Datos requeridos**: Nombre, DNI, edad (y talla si aplica)
5. ✅ **Talla de vestimenta**: Obligatoria para Palestra y Tirolesa
6. ✅ **Términos y condiciones**: Aceptación obligatoria
7. ✅ **Edad mínima**: Palestra (12 años), Tirolesa (8 años)
8. ✅ **Horarios válidos**: 9:00 - 18:00 hs

## 🎨 Estándares de Código

### Backend (PEP8)
- Longitud máxima de línea: 79 caracteres
- Docstrings en funciones y clases
- Type hints en funciones
- Imports organizados

Verificar con:
```powershell
flake8 src/ backend/
```

### Frontend (Airbnb)
- ESLint configurado con `eslint-config-airbnb`
- Componentes funcionales con hooks
- Props validation deshabilitada (configuración personalizada)

Verificar con:
```powershell
cd frontend
npm run lint
```

## 🔧 Solución de Problemas

### Backend no inicia
- Verificar que el entorno virtual esté activado
- Verificar que Flask esté instalado: `pip list | grep Flask`
- Puerto 5000 ocupado: Cambiar en `app.py`

### Frontend no inicia
- Limpiar caché de npm: `npm cache clean --force`
- Reinstalar dependencias: `rm -rf node_modules; npm install`
- Puerto 3000 ocupado: Cambiar en `vite.config.js`

### Error de CORS
- Verificar que Flask-CORS esté instalado
- Verificar que el backend esté corriendo en puerto 5000

### Base de datos no se crea
- Verificar permisos de escritura en la carpeta
- Eliminar `actividades.db` y reiniciar el backend

## 👥 Autores

**Grupo 4 - ISW 4K1**

- Bailey, Julian Eduardo
- Cufre, Ángel Hugo
- Carrió, Tomás Ezequiel
- Espósito, Nicolás
- Fernandez, Pablo
- Luna, Ángel Nahuel
- Longo Prudencio, Máximo
- Patolsky, Daniel
- Titón, Máximo
- Uliana, Agustín

## 📄 Licencia

Proyecto académico - Universidad Tecnológica Nacional (UTN)
