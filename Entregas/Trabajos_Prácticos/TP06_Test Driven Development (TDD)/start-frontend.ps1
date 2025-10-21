# Script para iniciar el frontend React
# Ejecutar desde la carpeta raíz del proyecto

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  Iniciando Frontend React" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Cambiar a carpeta frontend
Set-Location frontend

# Verificar si existen node_modules
if (-Not (Test-Path "node_modules")) {
    Write-Host "[INFO] Instalando dependencias de npm..." -ForegroundColor Yellow
    npm install
} else {
    Write-Host "[INFO] Dependencias ya instaladas" -ForegroundColor Yellow
}

# Ejecutar servidor de desarrollo
Write-Host ""
Write-Host "[SUCCESS] Frontend iniciado en http://localhost:3000" -ForegroundColor Green
Write-Host "[INFO] Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

npm run dev
