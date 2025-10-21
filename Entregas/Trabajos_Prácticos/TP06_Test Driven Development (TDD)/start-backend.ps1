# Script para iniciar el backend Flask
# Ejecutar desde la carpeta raíz del proyecto

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  Iniciando Backend Flask" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si existe el entorno virtual
if (-Not (Test-Path "venv")) {
    Write-Host "[INFO] Creando entorno virtual..." -ForegroundColor Yellow
    python -m venv venv
}

# Activar entorno virtual
Write-Host "[INFO] Activando entorno virtual..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Instalar dependencias
Write-Host "[INFO] Instalando dependencias..." -ForegroundColor Yellow
Set-Location backend
pip install -r requirements.txt --quiet

# Ejecutar servidor
Write-Host ""
Write-Host "[SUCCESS] Backend iniciado en http://localhost:5000" -ForegroundColor Green
Write-Host "[INFO] Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

python app.py
