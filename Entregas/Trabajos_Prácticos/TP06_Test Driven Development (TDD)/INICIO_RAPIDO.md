# Guía Rápida de Inicio

## 🚀 Inicio Rápido (Opción 1 - Scripts Automáticos)

### 1. Iniciar Backend
Abrir PowerShell en la carpeta del proyecto y ejecutar:
```powershell
.\start-backend.ps1
```

### 2. Iniciar Frontend
Abrir OTRA PowerShell en la carpeta del proyecto y ejecutar:
```powershell
.\start-frontend.ps1
```

### 3. Acceder a la aplicación
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

---

## 📝 Inicio Manual (Opción 2)

### Backend:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend (nueva terminal):
```powershell
cd frontend
npm install
npm run dev
```

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

## ❓ Problemas Comunes

### "No se puede ejecutar scripts en este sistema"
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Puerto ocupado
- Backend: Cambiar puerto en `backend/app.py` (línea final)
- Frontend: Cambiar puerto en `frontend/vite.config.js`

### Error de CORS
Verificar que el backend esté corriendo en http://localhost:5000

---

Para más detalles, consultar **README_PROYECTO.md**
