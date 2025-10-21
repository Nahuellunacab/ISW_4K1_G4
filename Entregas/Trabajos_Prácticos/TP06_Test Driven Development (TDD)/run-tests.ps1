# Script para ejecutar los tests
# Ejecutar desde la carpeta raíz del proyecto

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  Ejecutando Tests" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si existe el entorno virtual
if (-Not (Test-Path "venv")) {
    Write-Host "[ERROR] Entorno virtual no encontrado. Ejecuta start-backend.ps1 primero" -ForegroundColor Red
    exit 1
}

# Activar entorno virtual
Write-Host "[INFO] Activando entorno virtual..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Ejecutar tests
Write-Host "[INFO] Ejecutando tests..." -ForegroundColor Yellow
Write-Host ""

python -m unittest tests/test_inscribirse_actividad.py -v

Write-Host ""
Write-Host "[INFO] Tests completados" -ForegroundColor Green
